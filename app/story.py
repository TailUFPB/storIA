import random
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, set_seed

class Story_generator:
    def __init__(self):
        self.model_path = "Felipehonorato/storIA"
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path)
        self.model = self.model.to('cpu')

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        set_seed(random.randint(0, 999))

    def clean_text(self, text) -> str:
        """
        Params: Input text
        Returns: Treated input text (without spaces on the end, lower cased and with start token)
        """
        restart = True

        while restart:
            if text[-1] != " ":
                restart = False
            else:
                text = text[:-1]

        text = text.lower()
        
        return text
    
    def format_text(self, text) -> str:
        """
        Params: Input text
        Returns: Text formatted with capital letters and correct spacing
        """
        text = ' '.join(text.split())
        sentences = [sentence.strip().capitalize() for sentence in text.split('.')]
        formatted_text = '. '.join(sentences)
        
        return formatted_text

    def generate_story(self, text, size, temperature) -> str:
        """
        Params: Input text, max size and temperature
        Returns: generated story
        """
        if text != "":
            text = self.clean_text(text)

        input_length = len(text.split())

        writer = pipeline('text-generation', model=self.model, tokenizer=self.tokenizer)

        story = writer(
            text, max_length=input_length + size, 
            temperature=float(temperature), 
            repetition_penalty=float(1.2),
            num_beams=5,
            no_repeat_ngram_size=3,
            truncation=True
        )
        
        story = story[0].get('generated_text')
        story = self.format_text(story)

        return story