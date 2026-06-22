# Finance API

API de Controle de Gastos Pessoais, desenvolvida para o Trabalho Prático 1 da
disciplina de Gerência de Configuração e Evolução de Software (PUC Minas).

## Domínio

A aplicação permite que usuários cadastrem contas (carteira, conta corrente etc.),
registrem transações (receitas e despesas) categorizadas, e consultem o saldo
atual e relatórios de gastos por categoria.

**Entidades:** `User`, `Account`, `Category`, `Transaction`

## Stack utilizada

- **Linguagem:** Python 3.11
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Banco de dados:** SQLite
- **Testes:** Pytest + TestClient (FastAPI)
- **Containerização:** Docker
- **CI/CD:** Semaphore CI
- **Deploy:** Render (free tier)

## Estrutura do projeto

```
app/
  models/         # Entidades (SQLAlchemy)
  repositories/    # Acesso a dados
  services/        # Regras de negócio
  routers/          # Endpoints REST (controllers)
  schemas.py        # Validação de entrada/saída (Pydantic)
  database.py       # Configuração do banco
  main.py            # Ponto de entrada da aplicação
tests/
  test_unit_services.py        # Testes de unidade
  test_integration_api.py      # Testes de integração
  test_acceptance.py            # Teste de aceitação E2E
.github/workflows/ci-cd.yml     # Pipeline de CI/CD
Dockerfile
requirements.txt
```

## Como rodar localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar a aplicação
uvicorn app.main:app --reload

# Acessar a documentação interativa
# http://localhost:8000/docs
```

## Como rodar os testes

```bash
# Todos os testes
pytest -v

# Apenas testes de unidade
pytest tests/test_unit_services.py -v

# Apenas testes de integração
pytest tests/test_integration_api.py -v

# Apenas teste de aceitação
pytest tests/test_acceptance.py -v
```

## Como rodar com Docker

```bash
docker build -t finance-api .
docker run -p 8000:8000 finance-api
```

## Pipeline de CI/CD

O pipeline é executado no **Semaphore CI**, dividido em duas pipelines conectadas
por *promotion* (padrão recomendado pelo Semaphore para separar CI de CD):

**`.semaphore/semaphore.yml`** — disparada em todo push:
1. **Commit Stage:** build da aplicação + testes de unidade e integração
2. **Acceptance Stage:** teste de aceitação end-to-end

**`.semaphore/deploy.yml`** — promovida automaticamente apenas quando o push é
na branch `main` e as etapas anteriores passam:

3. **Release Stage:** build da imagem Docker, push para o Docker Hub e disparo
   do deploy no Render

### Configuração necessária no Semaphore

1. Conectar o repositório do GitHub à organização no Semaphore CI
2. Criar os secrets (Organization > Secrets):
   - `dockerhub-credentials` com as variáveis `DOCKERHUB_USERNAME` e `DOCKERHUB_TOKEN`
   - `render-deploy-hook` com a variável `RENDER_DEPLOY_HOOK_URL`
3. O Semaphore detecta automaticamente o arquivo `.semaphore/semaphore.yml` a
   cada push e dispara o pipeline

## Endpoints principais

| Método | Rota | Descrição |
|---|---|---|
| POST | `/users/` | Criar usuário |
| POST | `/accounts/` | Criar conta |
| GET | `/accounts/{id}/balance` | Consultar saldo |
| POST | `/categories/` | Criar categoria |
| POST | `/transactions/` | Registrar transação |
| GET | `/transactions/report/{account_id}` | Relatório por categoria |
| GET | `/health` | Healthcheck |

<!-- Pipeline Trigger -->
