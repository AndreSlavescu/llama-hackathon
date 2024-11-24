from transformers import AutoTokenizer, AutoModelForCausalLM
from liger_kernel.transformers import apply_liger_kernel_to_llama

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
        self.model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
        self.model = self.model.cuda()
    
    def generate(self, prompt: str) -> str:
        """
        Generate text using the Llama model
        
        Args:
            prompt (str): Input text to generate from
        
        Returns:
            str: Generated text output
        """
        tokens = self.tokenizer(prompt, return_tensors="pt")
        tokens = {k: v.cuda() for k, v in tokens.items()}
        
        output = self.model.generate(**tokens, max_length=100)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

if __name__ == "__main__":
    generator = TextGenerator()
    print(generator.generate("What is AI?"))
    print(generator.generate("What is the capital of France?"))
    print(generator.generate("What is the capital of Italy?"))