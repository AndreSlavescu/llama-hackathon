from transformers import AutoTokenizer, AutoModelForCausalLM
from liger_kernel.transformers import apply_liger_kernel_to_llama

apply_liger_kernel_to_llama(
  rope=True,
  swiglu=True,
  cross_entropy=True,
  fused_linear_cross_entropy=False,
  rms_norm=False
)

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
model = model.cuda()

input_text = "Hello, world!"
tokens = tokenizer(input_text, return_tensors="pt")
tokens = {k: v.cuda() for k, v in tokens.items()}

output = model(**tokens)
print(f"Decoded tokens: {tokenizer.decode(tokens['input_ids'][0])}")