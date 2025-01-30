from prometheus_client import Counter

# --- Contadores Prometheus da Aplicação ---
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

CACHE_HITS = Counter(
    'flask_app_cache_hits_total',
    'Total de acertos no cache'
)

CACHE_MISSES = Counter(
    'flask_app_cache_misses_total',
    'Total de faltas no cache'
)