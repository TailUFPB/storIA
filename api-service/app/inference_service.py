import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from flask import Flask, request, jsonify
from app.story import StoryGenerator
from app.logger import storia_logger
from app.metrics import start_metrics  

app = Flask(__name__)

# Inicia a instrumentação de métricas
start_metrics(app)

storia_logger.info("Carregando modelo no serviço de inferência...")
generator = StoryGenerator()
storia_logger.info("Modelo carregado no serviço de inferência.")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    input_text = data.get("text")
    size = data.get("size", 100)
    temperature = data.get("temperature", 1.0)
    try:
        story = generator.generate_story(input_text, int(size), float(temperature))
        storia_logger.info(f"História gerada: {story}")
        return jsonify({"story": story})
    except Exception as e:
        storia_logger.error(f"Erro na geração de história: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    host = os.environ.get("INFERENCE_HOST", "0.0.0.0")
    port = int(os.environ.get("INFERENCE_PORT", 6000))
    app.run(host=host, port=port)
