import requests
from app.logger import storia_logger

def generate_story_job(input_text, size, temperature):
    inference_url = "http://ingress-nginx-controller.ingress-nginx.svc.cluster.local/generate"  # ajuste conforme o hostname e porta do serviço de inferência
    payload = {
        "text": input_text,
        "size": size,
        "temperature": temperature
    }
    try:
        response = requests.post(inference_url, json=payload, timeout=600)
        response.raise_for_status()
        data = response.json()
        if "story" in data:
            return data["story"]
        else:
            raise Exception("Resposta inválida do serviço de inferência: " + str(data))
    except Exception as e:
        storia_logger.error(f"Erro ao chamar o serviço de inferência: {e}")
        raise e