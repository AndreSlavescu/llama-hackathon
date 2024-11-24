from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    StoppingCriteria,
    StoppingCriteriaList,
)
import torch
import gc
from liger_kernel.transformers import apply_liger_kernel_to_llama
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import re


@dataclass
class Message:
    role: str
    content: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


class ConversationHistory:
    def __init__(self, max_messages: int = 10):
        self.messages: List[Message] = []
        self.max_messages = max_messages

    def add_message(self, role: str, content: str) -> None:
        """Add a new message to the conversation history"""
        message = Message(role=role, content=content)
        self.messages.append(message)

        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages :]

    def get_messages(self) -> List[Dict[str, str]]:
        """Get messages in format suitable for the model"""
        return [msg.to_dict() for msg in self.messages]

    def clear(self) -> None:
        """Clear the conversation history"""
        self.messages = []


class StopOnTokens(StoppingCriteria):
    def __init__(self, stop_token_ids):
        self.stop_token_ids = stop_token_ids

    def __call__(self, input_ids, scores, **kwargs) -> bool:
        for stop_id in self.stop_token_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False


class TextGenerator:
    def __init__(self):
        """Initialize the Llama model with Liger kernel optimizations"""
        apply_liger_kernel_to_llama(
            rope=True,
            swiglu=True,
            cross_entropy=False,
            fused_linear_cross_entropy=True,
            rms_norm=True,
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            "meta-llama/Llama-3.1-8B-Instruct"
        )
        self.tokenizer.pad_token = self.tokenizer.eos_token

        self.model = AutoModelForCausalLM.from_pretrained(
            "meta-llama/Llama-3.1-8B-Instruct", trust_remote_code=True
        ).cuda()

        self.conversations: Dict[str, ConversationHistory] = {}

    def get_or_create_conversation(
        self, session_id: str, max_messages: int = 5
    ) -> ConversationHistory:
        """Get an existing conversation or create a new one"""
        if session_id not in self.conversations:
            self.conversations[session_id] = ConversationHistory(
                max_messages=max_messages
            )
        return self.conversations[session_id]

    def clear_history(self, session_id: str) -> None:
        """Clear conversation history for a specific session"""
        if session_id in self.conversations:
            self.conversations[session_id].clear()

    def get_history(self, session_id: str) -> List[Message]:
        """Get conversation history for a specific session"""
        if session_id in self.conversations:
            return self.conversations[session_id].messages
        return []

    def generate(
        self, prompt: str, conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate a response based on conversation history or a prompt with mixed precision

        Args:
            prompt: Input text to generate from
            conversation_history: List of message dictionaries with 'role' and 'content'

        Returns:
            str: Generated response or text output
        """
        if conversation_history is None:
            messages = [{"role": "user", "content": prompt}]
        else:
            messages = conversation_history

        formatted_prompt = self.tokenizer.apply_chat_template(messages, tokenize=False)

        formatted_prompt = (
            "You are a helpful AI assistant. Provide clear, direct answers without including "
            "system messages or dates. Respond naturally as if in a real conversation.\n\n"
            + formatted_prompt
        )

        tokens = self.tokenizer(formatted_prompt, return_tensors="pt")
        tokens = {k: v.cuda() for k, v in tokens.items()}

        stop_words = ["\nHuman:", "\nUser:", "\nAssistant:", "<|end|>"]
        stop_ids = [
            self.tokenizer.encode(word, add_special_tokens=False)[0]
            for word in stop_words
        ]
        stopping_criteria = StoppingCriteriaList([StopOnTokens(stop_ids)])

        output = self.model.generate(
            **tokens,
            max_length=8192,
            min_length=32,
            do_sample=True,
            temperature=0.8,
            top_p=0.95,
            pad_token_id=self.tokenizer.pad_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            stopping_criteria=stopping_criteria,
            repetition_penalty=1.2,
            no_repeat_ngram_size=3,
        )

        result = self.tokenizer.decode(output[0], skip_special_tokens=True)

        response = result.split("Assistant:")[-1] if "Assistant:" in result else result
        response = response.split("Human:")[0] if "Human:" in response else response

        cleanup_patterns = [
            r"Cutting Knowledge Date:.*?\n",
            r"Today Date:.*?\n",
            r"system\n",
            r"user\n",
            r"assistant\n",
            r"assistant$",
            r"^\s*(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\s*\n*",
            r"^\s*\d{1,2}\s+[A-Za-z]+\s+\d{4}\s*\n*",
        ]

        for pattern in cleanup_patterns:
            response = re.sub(pattern, "", response, flags=re.MULTILINE)

        response = re.sub(r"\n\s*\n", "\n\n", response)
        response = response.strip()

        gc.collect()
        torch.cuda.empty_cache()

        return response

    def chat(self, message: str, session_id: str) -> str:
        """
        Chat with history tracking

        Args:
            message: User's message
            session_id: Session identifier for conversation tracking

        Returns:
            str: Generated response
        """
        conv = self.get_or_create_conversation(session_id)
        conv.add_message("user", message)
        response = self.generate(message, conv.get_messages())
        conv.add_message("assistant", response)

        return response


if __name__ == "__main__":
    generator = TextGenerator()

    # Example 1: Single prompt without history (text generation)
    print("Without history:", generator.generate("What is AI?"))

    # Example 2: Chat with history (simulating Lex Fridman AI podcast)
    session_id = "lex_podcast"
    print("\nLex Fridman AI Podcast Simulation:")
    print(
        "Lex: Let's start with a fundamental question - what is consciousness and how does it relate to artificial intelligence?"
    )
    print(
        "Assistant:",
        generator.chat(
            "Let's start with a fundamental question - what is consciousness and how does it relate to artificial intelligence?",
            session_id,
        ),
    )
    print(
        "\nLex: That's fascinating. When you think about the development of AGI, what are the key ethical considerations we need to keep in mind?"
    )
    print(
        "Assistant:",
        generator.chat(
            "That's fascinating. When you think about the development of AGI, what are the key ethical considerations we need to keep in mind?",
            session_id,
        ),
    )
    print(
        "\nLex: You mentioned alignment. How do we ensure AI systems remain aligned with human values as they become more capable?"
    )
    print(
        "Assistant:",
        generator.chat(
            "You mentioned alignment. How do we ensure AI systems remain aligned with human values as they become more capable?",
            session_id,
        ),
    )

    # Print conversation history
    print("\nConversation History:")
    for msg in generator.get_history(session_id):
        print(f"{msg.role}: {msg.content}")
