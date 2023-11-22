from transformers import GPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

input_ids = tokenizer.encode("can you talk me what is AI.", return_tensors="pt")
output = model.generate(input_ids, max_length=50, num_return_sequences=5, temperature=0.7, do_sample=True)

for i, token_ids in enumerate(output):
    print(f"Sample {i+1}: {tokenizer.decode(token_ids)}")
