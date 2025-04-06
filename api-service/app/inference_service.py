from flask import Flask, request, jsonify
from app.story import StoryGenerator
from app.logger import storia_logger

# Inicializa a aplicação Flask
app = Flask(__name__)

# Carrega o modelo uma única vez ao iniciar o serviço
storia_logger.info("Carregando modelo no serviço de inferência...")
generator = StoryGenerator()  # Instância global do gerador
storia_logger.info("Modelo carregado no serviço de inferência.")

@app.route("/generate", methods=["POST"])
def generate():
    """
    Endpoint POST que gera histórias com base nos parâmetros fornecidos.
    
    Corpo da Requisição (JSON):
    {
        "text": "Contexto opcional",  # (string, opcional)
        "title": "Título opcional",   # (string, opcional)
        "size": 250,                  # (int, opcional, padrão=250)
        "temperature": 1.0            # (float, opcional, padrão=1.0)
    }

    Retorno (JSON):
    - Sucesso (200): {"story": "Texto da história gerada"}
    - Erro (500): {"error": "Mensagem de erro"}
    """
    data = request.get_json()  # Lê os dados JSON da requisição
    
    # Extrai parâmetros com valores padrão
    context = data.get("text", "")          # Contexto inicial
    if not context:
        return jsonify({"error": "Contexto vazio"}), 400
    # Verifica se o contexto é muito longo
    if len(context) > 2048:
        return jsonify({"error": "Contexto muito longo"}), 400
    title = data.get("title", "")           # Título (opcional)
    size = data.get("size", 250)            # Tamanho em tokens (padrão: 250)
    temperature = data.get("temperature", 1.0)  # Criatividade (padrão: 1.0)

    try:
        story = generator.generate_story(
            context=context,
            title=title,
            max_tokens=int(size),
            temperature=float(temperature)
        )
        return jsonify({"story": story})  # Retorna sucesso (200)

    except Exception as e:
        storia_logger.error(f"Erro na geração de história: {e}")
        return jsonify({"error": str(e)}), 500  # Retorna erro (500)

if __name__ == "__main__":
    # Inicia o servidor Flask
    app.run(host="0.0.0.0", port=6000)