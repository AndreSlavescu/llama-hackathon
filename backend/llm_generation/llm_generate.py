from transformers import AutoTokenizer, AutoModelForCausalLM, StoppingCriteria, StoppingCriteriaList
import torch
import gc
from liger_kernel.transformers import apply_liger_kernel_to_llama

class StopOnTokens(StoppingCriteria):
    def __init__(self, stop_token_ids):
        self.stop_token_ids = stop_token_ids

    def __call__(self, input_ids, scores, **kwargs):
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
            rms_norm=True
        )

        self.tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.model = AutoModelForCausalLM.from_pretrained(
            "meta-llama/Llama-3.1-8B-Instruct",
            trust_remote_code=True
        ).cuda()
    
    def generate(self, prompt: str) -> str:
        """
        Generate text using the Llama model with mixed precision
        
        Args:
            prompt (str): Input text to generate from
        
        Returns:
            str: Generated text output
        """
        tokens = self.tokenizer(prompt, return_tensors="pt")
        tokens = {k: v.cuda() for k, v in tokens.items()}
        
        stop_words = [".", "\n", "?\n"]
        stop_ids = [self.tokenizer.encode(word, add_special_tokens=False)[0] for word in stop_words]
        stopping_criteria = StoppingCriteriaList([StopOnTokens(stop_ids)])
        
        output = self.model.generate(
            **tokens,
            max_length=200,
            min_length=30,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=self.tokenizer.pad_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            stopping_criteria=stopping_criteria,
            repetition_penalty=1.2
        )
        
        result = self.tokenizer.decode(output[0], skip_special_tokens=True)
        result = result.strip()
        
        gc.collect()
        torch.cuda.empty_cache()
        return result

if __name__ == "__main__":
    generator = TextGenerator()
    print(generator.generate("What is AI?"))
    print(generator.generate("What is the capital of France?"))
    print(generator.generate("What is the capital of Italy?"))