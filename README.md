# 📊 Dashboard de Vendas Executivo com Python & Docker

Projeto desenvolvido para prática de containerização com **Docker**, **Docker Compose**, **Python (Streamlit, Pandas, Plotly)** e **PostgreSQL**.

## 🚀 Como Executar o Projeto

### Pré-requisitos
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e em execução.
- [Git](https://git-scm.com/) instalado.

### Passo a Passo

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/lbrambillacostao/dash_vendas_docker.git](https://github.com/lbrambillacostao/dash_vendas_docker.git)
   cd dash_vendas_docker

   ## ☸️ Testes com Kubernetes (Kind Cluster)

O projeto também conta com suporte para testes locais em cluster Kubernetes de múltiplos nós usando **Kind**.

### Subir o Cluster Local (1 Control-Plane + 2 Workers)

```bash
# Criar o cluster com a configuração de 3 nós
kind create cluster --config k8s/kind-config.yaml

# Verificar os nós ativos
kubectl get nodes

# Testar o balanceamento de carga entre os workers
kubectl create deployment meu-teste --image=nginx --replicas=6
kubectl get pods -o wide

# Testar resiliência e evacuação de um nó
kubectl drain desktop-worker2 --ignore-daemonsets --delete-emptydir-data

# Reativar o nó
kubectl uncordon desktop-worker2