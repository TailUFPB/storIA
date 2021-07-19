from transformers import GPT2Tokenizer, GPT2LMHeadModel
from transformers import set_seed
import random
from re import sub

class Story_generator:

    def __init__(self):
        self.model_path = "Model\Models\V-3.0\checkpoint-53705"

        set_seed(random.randint(0, 999))

        self.tokenizer = GPT2Tokenizer.from_pretrained(
            'gpt2', bos_token='<|startoftext|>', eos_token='<|endoftext|>')

        self.model = GPT2LMHeadModel.from_pretrained(
                    self.model_path, eos_token_id=self.tokenizer.eos_token_id, 
                    bos_token_id=self.tokenizer.bos_token_id)
                
        self.model.resize_token_embeddings(len(self.tokenizer))

        self.model = self.model.to('cpu')


    def clean_text(self, text) -> str:
        """
        Params: Input text
        Returns: treated input text (whithout spaces on the end, lower cased and with start token)
        """
        restart = True

        while(restart):
            if text[-1] != " ":
                restart = False
            else:
                text = text[:-1]

        text = text.lower()
        
        return "<|startoftext|> " + text


    def generate_story(self, text, size, temperature) -> str:
        """
        Params: Input text, max size and temperature
        Returns: generated story
        """
        
        text = self.clean_text(text)

        input_ids = self.tokenizer.encode(text, return_tensors='pt')

        input_length = len(text.split())

        beam_outputs = self.model.generate(
            input_ids, 
            num_beams=5, 
            max_length = input_length + size,
            min_length = input_length + size - 10,
            no_repeat_ngram_size=2, 
            num_return_sequences=1,
            reptition_penalty = float(1),
            temperature = float(temperature),
            early_stopping=True
        )

        story = self.tokenizer.decode(beam_outputs[0], skip_special_tokens=False)

        story = sub("<|startoftext|>", "", story)
        story = sub("<|endoftext|>", "", story)

        return story

story = Story_generator()

example = story.generate_story("I was alone ", 100, 1.2 )

print(example)