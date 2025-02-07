from flask import Flask, request, jsonify
from app.story import StoryGenerator
from app.logger import storia_logger

app = Flask(__name__)

# Carrega o modelo apenas uma vez quando o serviço inicia
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
        return jsonify({"story": story})
    except Exception as e:
        storia_logger.error(f"Erro na geração de história: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
