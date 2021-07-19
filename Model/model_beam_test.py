from transformers import GPT2Tokenizer, GPT2LMHeadModel
from transformers import pipeline, set_seed
import random

model_path = "Model\Models\V-2.0\checkpoint-53705"

set_seed(random.randint(0, 999))

tokenizer = GPT2Tokenizer.from_pretrained(
            'gpt2', bos_token='<|startoftext|>', eos_token='<|endoftext|>')

model = GPT2LMHeadModel.from_pretrained(
            model_path, eos_token_id=tokenizer.eos_token_id, 
            bos_token_id=tokenizer.bos_token_id)
        
model.resize_token_embeddings(len(tokenizer))

model = model.to('cpu')

inputs = "<|startoftext|> I was a always alone, i had no friends"

input_ids = tokenizer.encode(inputs, return_tensors='pt')


input_length = len(inputs.split())

escritor = pipeline('text-generation', tokenizer= tokenizer, model = model)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

beam_outputs = model.generate(
    input_ids, 
    num_beams=5, 
    max_length = input_length + 100,
    min_length = input_length + 50,
    no_repeat_ngram_size=2, 
    num_return_sequences=1,
    reptition_penalty = float(1),
    temperature = float(1),
    early_stopping=True
)

storia_tres = tokenizer.decode(beam_outputs[0], skip_special_tokens=True)

print("\n" *2)
print("STORY WITH GENERATE (Beam_search) / TEMP: 1.5 / Rep_Pen: 1.5")

print("-"*100)
print(storia_tres)
print("-"*100)
print("\n" *2)