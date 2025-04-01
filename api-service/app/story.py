import random
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, set_seed

class StoryGenerator:
    def __init__(self) -> None:
        self.model_path = "Felipehonorato/storIA"
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path)
        self.model = self.model.to('cpu')

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        set_seed(random.randint(0, 999))
        
        # Inicializa o pipeline uma vez para reutilização
        self.generator = pipeline('text-generation', model=self.model, tokenizer=self.tokenizer)

    def clean_text(self, text: str) -> str:
        """
        Remove espaços finais e converte o texto para minúsculas.
        """
        return text.rstrip().lower()
    
    def format_text(self, text: str) -> str:
        """
        Formata o texto corrigindo espaços e capitalizando as sentenças.
        """
        text = ' '.join(text.split())
        sentences = [sentence.strip().capitalize() for sentence in text.split('.') if sentence.strip()]
        formatted_text = '. '.join(sentences)
        return formatted_text

    def generate_story(self, text: str, size: int, temperature: float) -> str:
        """
        Gera uma história a partir do texto de entrada, tamanho e temperatura.
        """
        if text:
            text = self.clean_text(text)

        input_length = len(text.split())

        output = self.generator(
            text, max_length=input_length + size, 
            temperature=temperature, 
            repetition_penalty=1.2,
            num_beams=5,
            no_repeat_ngram_size=3,
            truncation=True
        )
        
        story = output[0].get('generated_text', '')
        story = self.format_text(story)
        return story
