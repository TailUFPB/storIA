"""  from transformers import GPT2Tokenizer, GPT2LMHeadModel
from transformers import set_seed
import random
from transformers import pipeline

class Story_generator:

    def __init__(self):
        self.model_path = "model\checkpoint-53705"

        set_seed(random.randint(0, 999))

        self.tokenizer = GPT2Tokenizer.from_pretrained(
            'gpt2', bos_token='<|startoftext|>', eos_token='<|endoftext|>', add_prefix_space = False)

        self.model = GPT2LMHeadModel.from_pretrained(
                    self.model_path, eos_token_id=self.tokenizer.eos_token_id, 
                    bos_token_id=self.tokenizer.bos_token_id)
                
        self.model.resize_token_embeddings(len(self.tokenizer))

        self.model = self.model.to('cpu')


    def clean_text(self, text) -> str:

        Params: Input text
        Returns: treated input text (whithout spaces on the end, lower cased and with start token)

        restart = True

        while(restart):
            if text[-1] != " ":
                restart = False
            else:
                text = text[:-1]

        text = text.lower()
        
        return "<|startoftext|> " + text


    def generate_story(self, text, size, temperature) -> str:
      
        Params: Input text, max size and temperature
        Returns: generated story
      

        if text != "":
            text = self.clean_text(text)

        input_length = len(text.split())

        writer = pipeline('text-generation', model = self.model, tokenizer = self.tokenizer)

        story = writer(
                text, max_length = input_length + size, 
                temperature = float(temperature), 
                repetition_penalty = float(1.2),
                num_beams = 5,
                no_repeat_ngram_size = 3)
            
        story = story[0].get('generated_text')

        story = story.replace('<|startoftext|>', "")
        story = story.replace('<|endoftext|>', "")

        return story

story = Story_generator()

example = story.generate_story("", 50, 1.2 )

print("\n" +example+ "\n" """