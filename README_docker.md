## Estrutura do Projeto

### Arquivos Principais

### `app.py`
Inicializa a aplicação Flask, configura as rotas e métricas, e inicia o servidor Flask com suporte a proxy reverso (ProxyFix).

### `app_metrics.py`
Define contadores de métricas do Prometheus para monitorar requisições totais, erros e desempenho do cache.

### `inference_service.py`
Define o serviço de inferência que gera histórias usando modelos carregados com Transformers. Disponibiliza a rota `/generate` para geração de histórias com parâmetros personalizáveis.

### `logger.py`
Configura um logger padrão (`storIA_logger`) usando RotatingFileHandler para registrar eventos e erros, gravando logs em arquivo e stream (console).

### `metrics.py`
Implementa métricas adicionais de monitoramento do sistema (CPU, memória, disco, latência HTTP e GPU) usando Prometheus. Disponibiliza uma rota `/metrics` para exportar estas métricas.

### `redis_connection.py`
Estabelece e testa a conexão com o Redis utilizado para cache e filas de tarefas.

### `story.py`
Implementa a classe `StoryGenerator` que utiliza um modelo de linguagem pré-treinado (Hugging Face Transformers) para gerar textos personalizados.

### `tasks.py`
Define a função para enfileirar uma requisição ao serviço de inferência para gerar histórias, usando Redis Queue (RQ).

### `views.py`
Define todas as rotas principais do backend:
- `/`: Página inicial do app.
- `/submit`: Enfileira tarefas de geração de histórias, usando cache quando disponível.
- `/result/<job_id>`: Obtém o resultado da geração de histórias.
- `/health`: Verificação da saúde da aplicação.
- `/social` e `/members`: Outras páginas da aplicação.

### `worker.py`
Inicializa o worker que processa tarefas enfileiradas no Redis Queue (RQ).

---

## Docker

### Dependências

O projeto utiliza as dependências listadas em `requirements.txt`:

```
praw
pandas 
langdetect
flask
transformers
datasets
prometheus_client
torch
psutil
GPUtil
python-dotenv
gunicorn
gevent
redis
rq
pytest
pytest-cov 
requests
```

### Comandos Docker

```bash
# Precisa estar logado no Docker Hub e criar um repositório com o nome "tailmlops"
docker build -t tailmlops/api-service:staging . # pra usar production, trocar staging por production
docker push tailmlops/api-service:staging
```

---

## Kubernetes e Helm

### Inicialização do Ambiente Kubernetes

```bash
helm install storia-staging ./storia -f ./storia/values-staging.yaml

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.1/deploy/static/provider/cloud/deploy.yaml
kubectl get pods -n ingress-nginx

kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml 

kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.9.1/cert-manager.crds.yaml

kubectl create namespace cert-manager

helm repo add jetstack https://charts.jetstack.io/
helm repo update

helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace

kubectl apply -f k8s/configmap/
kubectl apply -f k8s/redis/
kubectl apply -f k8s/monitoring/
kubectl apply -f k8s/ingress/
kubectl apply -f k8s/grafana/
kubectl apply -f k8s/loki/
kubectl apply -f k8s/prometheus/
kubectl apply -f k8s/promtail/
kubectl apply -f k8s/locust/
kubectl apply -f k8s/cert-manager/

helm upgrade storia-staging ./storia -f ./storia/values-staging.yaml
```
### Docker desktop não deixa gerar certificado TLS para o metrics-server

```bash

kubectl edit deployment metrics-server -n kube-system

append em args:
        - --kubelet-insecure-tls ## append this argument to the args list

# mais detalhes aqui: https://www.zeng.dev/post/2023-kubeadm-enable-kubelet-serving-certs/
```

### Configurações YAML adicionais

Os arquivos YAML incluem configurações detalhadas para:

- **Grafana** (Deployment, Service, Secret e ConfigMap)
- **Loki** (ConfigMap)
- **Prometheus e Promtail** (Para coleta e exportação de métricas e logs)
- **Locust** (Para testes de carga)
- **Ingress** (Configuração de roteamento com SSL)
- **Redis e Redis Exporter** (Deployments e Services para cache e coleta de métricas)

### Acesso à aplicação

Após instalação e configuração, acesse a aplicação em:

```
staging.127.0.0.1.nip.io
```

---

