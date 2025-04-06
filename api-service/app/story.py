import os
import time
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from app.logger import storia_logger

class StoryGenerator:
    def __init__(self):
        """
        Inicializa o gerador de histórias:
        - Define configurações do modelo.
        - Baixa o modelo do Hugging Face Hub.
        - Carrega o modelo na memória.
        """
        self.repo_id = "TailMLOps/storIA"  # Repositório do Hugging Face
        self.model_file = "model/storIA_q5_k_s.gguf"  # Arquivo do modelo GGUF
        self.n_ctx = 2048  # Tamanho máximo do contexto (em tokens)
        self.n_threads = max(1, os.cpu_count() - 2)  # Threads CPU (reserva 2 cores)

        try:
            # Baixa o modelo do Hugging Face Hub (armazena em cache local)
            storia_logger.info(f"Baixando modelo {self.model_file}...")
            self.model_path = hf_hub_download(
                repo_id=self.repo_id,
                filename=self.model_file,
                cache_dir="models"  # Pasta local para cache
            )

            # Configuração do modelo Llama.cpp
            storia_logger.info("Configurando modelo...")
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=self.n_ctx,  # Contexto de 2048 tokens
                n_threads=self.n_threads,  # Otimização para CPU
                n_gpu_layers=0,  # 0 = CPU-only
                rope_freq_base=10000,  # Melhora coerência longa
                n_gqa=8,  # Grouped-Query Attention (eficiente)
                verbose=False  # Silencia logs do Llama
            )
            storia_logger.info(f"Modelo carregado! Contexto: {self.n_ctx} tokens")

        except Exception as e:
            storia_logger.error(f"Falha ao carregar modelo: {e}")
            raise RuntimeError(f"Erro na inicialização: {e}")

    def clean_text(self, text: str) -> str:
        """
        Remove espaços finais e normaliza texto para minúsculas.
        
        Parâmetros:
            text (str): Texto de entrada (pode ser vazio).
        
        Retorna:
            str: Texto limpo ou string vazia se a entrada for None/empty.
        """
        if not text:
            return ""
        return text.rstrip().lower()

    def format_text(self, text: str) -> str:
        """
        Formata o texto para garantir:
        - Capitalização de sentenças.
        - Parágrafos preservados.
        - Pontuação final (.!?) garantida.
        
        Parâmetros:
            text (str): Texto bruto (ex: saída do modelo).
        
        Retorna:
            str: Texto formatado pronto para exibição.
        """
        lines = text.splitlines()
        normalized_lines = []
        last_was_empty = False

        for line in lines:
            stripped = line.strip()
            if not stripped:
                # Mantém apenas uma linha vazia entre parágrafos
                if not last_was_empty:
                    normalized_lines.append("")
                    last_was_empty = True
            else:
                # Capitaliza cada sentença
                sentences = []
                current = ""
                for char in stripped:
                    current += char
                    if char in '.!?':  # Fim de sentença
                        if current:
                            # Capitaliza primeira letra da sentença
                            for i, c in enumerate(current):
                                if c.isalpha():
                                    current = current[:i] + c.upper() + current[i+1:]
                                    break
                            sentences.append(current)
                            current = ""
                
                # Adiciona texto restante (se não terminou com pontuação)
                if current:
                    # Capitaliza início do texto residual
                    for i, c in enumerate(current):
                        if c.isalpha():
                            current = current[:i] + c.upper() + current[i+1:]
                            break
                    sentences.append(current)
                
                # Junta as sentenças formatadas
                formatted_line = ''.join(sentences)
                normalized_lines.append(formatted_line)
                last_was_empty = False

        formatted_text = '\n'.join(normalized_lines)

        # Garante que termina com pontuação
        if formatted_text and formatted_text[-1] not in '.!?':
            formatted_text += '.'

        return formatted_text

    def generate_prompt(self, context: str = "", title: str = "") -> str:
        """
        Constrói um prompt otimizado para geração de histórias de terror.
        
        Parâmetros:# Logger personalizado
            context (str): Contexto inicial (opcional).
            title (str): Título da história (opcional).
        
        Retorna:
            str: Prompt formatado para o modelo.
        """
        prompt_parts = ["Generate a complete horror story"]
        
        if title:
            prompt_parts.append(f"Title: {title.strip()}")
            
        if context:
            prompt_parts.append(f"Context: {self.clean_text(context)}")
            
        return "\n".join(prompt_parts)

    def generate_story(self, context: str = "", title: str = "", max_tokens: int = 500, temperature: float = 0.8) -> str:
        """
        Gera uma história de terror usando o modelo carregado.
        
        Parâmetros:
            context (str): Contexto inicial (opcional).
            title (str): Título da história (opcional).
            max_tokens (int): Número máximo de tokens a gerar (padrão: 500).
            temperature (float): Controla criatividade (0 = determinístico, 1 = aleatório).
        
        Retorna:
            str: História formatada e pronta para uso.
        
        Levanta:
            RuntimeError: Se a geração falhar.
        """
        try:
            start_time = time.time()
            prompt = self.generate_prompt(context, title)
            storia_logger.debug(f"Prompt gerado: {prompt}")

            # Parâmetros de geração ajustados para qualidade
            generation_params = {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 0.9,  # Amostragem em núcleo (90% melhores tokens)
                "top_k": 40,  # Limita opções a 40 tokens mais prováveis
                "repeat_penalty": 1.25,  # Penaliza repetição
                "stop": ["</s>"],  # Token de parada
                "stream": False,
                "echo": False,  # Não inclui o prompt na saída
            }
            storia_logger.info(f"Parâmetros: {generation_params}")

            # Executa o modelo
            output = self.llm.create_completion(**generation_params)
            raw_text = output['choices'][0]['text']
            storia_logger.debug(f"Texto bruto: {raw_text}")

            # Processa métricas
            elapsed = time.time() - start_time
            text = f"{context}{raw_text}"  # Combina contexto com saída
            formatted_text = self.format_text(text)
            
            # Log de desempenho
            storia_logger.info(
                f"Geração concluída em {elapsed:.2f}s | "
                f"Tokens usados: {output['usage']['completion_tokens']}"
            )
            
            return formatted_text
            
        except Exception as e:
            storia_logger.error(f"Erro na geração: {e}")
            raise RuntimeError(f"Falha ao gerar história: {e}")