from flask import Response, g
from prometheus_client import Gauge, generate_latest, REGISTRY
import psutil
import time
import threading
import GPUtil

# Contadores e medidores
CPU_USAGE = Gauge('system_cpu_usage', 'Porcentagem de uso da CPU')
MEMORY_USAGE = Gauge('system_memory_usage', 'Porcentagem de uso da memória')
DISK_USAGE = Gauge('system_disk_usage', 'Porcentagem de uso do disco')
REQUEST_LATENCY = Gauge('http_request_latency', 'Latência real das requisições HTTP em milissegundos')
GPU_USAGE = Gauge('system_gpu_usage', 'Porcentagem de uso da GPU (apenas se CUDA disponível)')

def collect_system_metrics():
    """Função para coletar métricas de sistema periodicamente"""
    while True:
        try:
            CPU_USAGE.set(psutil.cpu_percent(interval=1))
            MEMORY_USAGE.set(psutil.virtual_memory().percent)
            DISK_USAGE.set(psutil.disk_usage('/').percent)
            
            # Simulação do uso de GPU (Se necessário, use a biblioteca `nvidia-ml-py3` para GPU real)
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    GPU_USAGE.set(gpus[0].load * 100)
            except ImportError:
                pass

        except Exception as e:
            print(f"Erro ao coletar métricas do sistema: {e}")
        
        time.sleep(5)  # Coletar métricas a cada 5 segundos

def start_metrics(app):
    """Função para iniciar as métricas no Flask"""

    @app.before_request
    def start_timer():
        """Marca o início da requisição"""
        g.start_time = time.time()

    @app.after_request
    def log_latency(response):
        """Calcula a latência da requisição e armazena no Prometheus"""
        if hasattr(g, 'start_time'):
            elapsed_time = (time.time() - g.start_time) * 1000  # Converte para milissegundos
            REQUEST_LATENCY.set(elapsed_time)  # Define a latência no Gauge Prometheus
        return response

    @app.route("/metrics")
    def metrics():
        """Rota de métricas para Prometheus"""
        return Response(generate_latest(REGISTRY), mimetype='text/plain; charset=utf-8')

    # Iniciar a thread de métricas
    metrics_thread = threading.Thread(target=collect_system_metrics, daemon=True)
    metrics_thread.start()
