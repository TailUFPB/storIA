import random
<<<<<<< HEAD:api-service/app/story.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, set_seed
from app.logger import storia_logger 

class StoryGenerator:
    def __init__(self):
        self.model_path = "Felipehonorato/storIA"
        try:
            storia_logger.info(f"Carregando o modelo a partir de {self.model_path}")
            self.model = AutoModelForCausalLM.from_pretrained(self.model_path)
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
            self.model = self.model.to(self.device)

            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.tokenizer.pad_token = self.tokenizer.eos_token

            set_seed(random.randint(0, 999))

            self.writer = pipeline(
                'text-generation',
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == 'cuda' else -1
            )
            storia_logger.info(f"Modelo carregado e pipeline inicializada na device: {self.device}")
        except Exception as e:
            storia_logger.error(f"Erro ao inicializar o modelo: {e}")
            raise e  # Re-raise para que a aplicação saiba que houve falha

    def clean_text(self, text) -> str:
        """
        Remove espaços finais e converte para minúsculas.
=======
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
>>>>>>> development:app/story.py
        """
        restart = True

        while restart:
            if text[-1] != " ":
                restart = False
            else:
                text = text[:-1]

        text = text.lower()
<<<<<<< HEAD:api-service/app/story.py
        return text

    def format_text(self, text) -> str:
        """
        Formata o texto com letras maiúsculas e espaçamento correto.
=======
        
        return text
    
    def format_text(self, text) -> str:
        """
        Params: Input text
        Returns: Text formatted with capital letters and correct spacing
>>>>>>> development:app/story.py
        """
        text = ' '.join(text.split())
        sentences = [sentence.strip().capitalize() for sentence in text.split('.')]
        formatted_text = '. '.join(sentences)
<<<<<<< HEAD:api-service/app/story.py
=======
        
>>>>>>> development:app/story.py
        return formatted_text

    def generate_story(self, text, size, temperature) -> str:
        """
<<<<<<< HEAD:api-service/app/story.py
        Gera uma história com base no texto de entrada, tamanho e temperatura.
        """
        try:
            if text:
                text = self.clean_text(text)

            input_length = len(text.split())

            storia_logger.debug(f"Gerando história com input_length={input_length}, size={size}, temperature={temperature}")

            story = self.writer(
                text,
                max_length=input_length + size,
                temperature=float(temperature),
                repetition_penalty=1.2,
                num_beams=5,
                no_repeat_ngram_size=3,
                truncation=True
            )

            story = story[0].get('generated_text')
            story = self.format_text(story)

            storia_logger.info("História gerada com sucesso")
            return story
        except Exception as e:
            storia_logger.error(f"Erro ao gerar história: {e}")
            raise e
=======
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
>>>>>>> development:app/story.py
