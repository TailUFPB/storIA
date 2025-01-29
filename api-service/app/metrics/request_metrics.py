from prometheus_client import Counter

# Contadores reutilizáveis em múltiplos arquivos de rotas
REQUEST_COUNT = Counter(
    'flask_app_requests_total',
    'Total de requisições para o app',
    ['method', 'endpoint']
)

ERROR_COUNT = Counter(
    'flask_app_errors_total',
    'Total de erros',
    ['method', 'endpoint']
)