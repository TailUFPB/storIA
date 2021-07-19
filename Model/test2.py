from transformers import GPT2Tokenizer, GPT2LMHeadModel
from transformers import pipeline, set_seed
import random

model_path = "Model\Models\V-3.0\checkpoint-53705"

set_seed(random.randint(0, 999))

tokenizer = GPT2Tokenizer.from_pretrained(
            'gpt2', bos_token='<|startoftext|>', eos_token='<|endoftext|>')

model = GPT2LMHeadModel.from_pretrained(
            model_path, eos_token_id=tokenizer.eos_token_id, 
            bos_token_id=tokenizer.bos_token_id)
        
model.resize_token_embeddings(len(tokenizer))

model = model.to('cpu')

inputs = "<|startoftext|> me and my brother were lost in the dark florest. We should be going back home, after school, but in the way, my brother felt from a cliff, i went down so that i could help him"

input_ids = tokenizer.encode(inputs, return_tensors='pt')


input_length = len(inputs.split())

escritor = pipeline('text-generation', tokenizer= tokenizer, model = model)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

beam_outputs = model.generate(
    input_ids, 
    max_length = input_length + 100,
    min_length = input_length + 50,
    num_return_sequences=1,
    reptition_penalty = float(1),
    temperature = float(0.9),
)

storia_tres = tokenizer.decode(beam_outputs[0], skip_special_tokens=True)

print("\n" *2)
print("STORY WITH GENERATE (Beam_search) / TEMP: 1.5 / Rep_Pen: 1.5")

print("-"*300)
print(storia_tres)
print("-"*300)
print("\n" *2)