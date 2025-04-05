import os
import time
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from logger import storia_logger 

class StoryGenerator:
    def __init__(self):
        self.repo_id = "TailMLOps/storIA"
        self.model_file = "model/storIA_q5_k_s.gguf"
        self.n_ctx = 2048
        self.n_threads = max(1, os.cpu_count() - 2)
        
        try:
            storia_logger.info(f"Baixando modelo {self.model_file} do repositório {self.repo_id}")
            self.model_path = hf_hub_download(
                repo_id=self.repo_id,
                filename=self.model_file,
                cache_dir="models"
            )
            
            storia_logger.info("Configurando parâmetros para modelo fundido...")
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=self.n_ctx,
                n_threads=self.n_threads,
                n_gpu_layers=0,
                rope_freq_base=10000,
                n_gqa=8, 
                verbose=False
            )
            
            storia_logger.info(f"Modelo carregado com sucesso! Contexto: {self.n_ctx} tokens")
            
        except Exception as e:
            storia_logger.error(f"Falha ao carregar modelo: {str(e)}")
            raise RuntimeError(f"Erro na inicialização do modelo: {e}")

    def clean_text(self, text: str) -> str:
        """Remove espaços finais e normaliza texto"""
        if not text:
            return ""
        return text.rstrip().lower()

    def format_text(self, text: str) -> str:
        """Formatação do texto gerado"""
        if not text:
            return ""
            
        sentences = [s.strip().capitalize() for s in text.split('.') if s.strip()]
        formatted = '. '.join(sentences)
        
        if formatted and not formatted.endswith(('.', '!', '?')):
            formatted += '.'
            
        return formatted

    def generate_prompt(self, context: str = "", title: str = "") -> str:
        """Constroi prompt otimizado para geração de histórias"""
        prompt_parts = []
        
        if title:
            prompt_parts.append(f"Título: {title.strip()}")
            
        if context:
            prompt_parts.append(f"Contexto: {self.clean_text(context)}")
            
        prompt_parts.append("Gere uma história de terror completa:")
        return "\n".join(prompt_parts)

    def generate_story(self, context:str="", title:str="", max_tokens:int=500, temperature:float=0.8) -> str:
        """Gera história com ajustes para modelos fundidos"""
        try:
            start_time = time.time()
            prompt = self.generate_prompt(context, title)
            
            storia_logger.debug(f"Prompt: {prompt}")
            
            generation_params = {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 0.9,
                "repeat_penalty": 1.25,
                "rope_freq_scale": 0.95,
                "stop": ["\n\n", "###", "</s>"]
            }
            
            output = self.llm.create_completion(**generation_params)
            raw_text = output['choices'][0]['text']
            
            clean_text = self.format_text(raw_text)
            elapsed = time.time() - start_time
            
            storia_logger.info(f"Geração concluída em {elapsed:.2f}s | Tokens: {len(output['usage']['completion_tokens'])}")
            return clean_text
            
        except Exception as e:
            storia_logger.error(f"Erro na geração: {str(e)}")
            raise RuntimeError(f"Falha ao gerar história: {e}")

# Tira isso aqui depois
if __name__ == "__main__":
    try:
        generator = StoryGenerator()
        
        # Exemplo de uso
        story = generator.generate_story(
            context="Uma casa abandonada com relógios parados na meia-noite",
            title="O Sussurro nas Paredes",
            max_tokens=350
        )
        
        print("\n" + "="*50)
        print("HISTÓRIA GERADA:")
        print("="*50)
        print(story)
        
    except Exception as e:
        print(f"\nERRO: {str(e)}")
        storia_logger.critical(f"Falha crítica: {str(e)}")