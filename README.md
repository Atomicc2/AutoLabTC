# AutoLab-TC

Plataforma web para construção, transformação e manipulação de autômatos finitos, com integração a arquivos `.jff` do JFLAP.

A aplicação permite enviar um autômato finito, selecionar uma operação e baixar o resultado no formato `.jff`.

## Funcionalidades

- Importação de autômatos via arquivos `.jff`;
- Listagem das operações disponíveis na API;
- Operações sobre autômatos finitos (atualmente: **complemento**);
- Exportação do resultado em `.jff` para uso no JFLAP.

## Tecnologias

- **Backend:** Python 3.12 + FastAPI + Uvicorn;
- **Frontend:** React 19 + TypeScript + Vite;
- **Testes:** Pytest (backend);
- **Lint:** Ruff (backend) e Oxlint (frontend).

## Estrutura

```text
AutoLabTC/
├── backend/            # API FastAPI
│   ├── app/
│   │   ├── entidades/  # Estado, Transição, Autômato Finito
│   │   ├── rotas/      # Endpoints HTTP
│   │   ├── servicos/   # Regras de negócio / operações
│   │   └── utilitarios/# Leitura e escrita de arquivos .jff
│   ├── testes/         # Testes automatizados
│   └── requirements*.txt
└── frontend/           # Interface React + Vite
    └── src/
```

## Pré-requisitos

- Python 3.12+
- Node.js 20+ e npm

## Como executar em ambiente de desenvolvimento

Os comandos do backend devem ser executados a partir da **raiz do projeto**.

### 1. Backend (API)

Crie e ative o ambiente virtual, instale as dependências e suba o servidor:

```bash
python3 -m venv backend/.venv
source backend/.venv/bin/activate
pip install -r backend/requirements-dev.txt
uvicorn backend.app.main:app --reload --port 8000
```

A API ficará disponível em `http://localhost:8000` (documentação interativa em `http://localhost:8000/docs`).

### 2. Frontend (interface)

Em outro terminal, instale as dependências e suba o servidor de desenvolvimento:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

O frontend ficará disponível em `http://localhost:5173`.

> Por padrão o frontend consome a API em `http://localhost:8000`, configurável pela variável `VITE_API_URL` no arquivo `frontend/.env`.

## Testes

Backend (a partir da raiz do projeto, com o ambiente virtual ativado):

```bash
pytest
```

Lint do frontend:

```bash
cd frontend
npm run lint
```

## Endpoints

| Método | Rota                 | Descrição                              |
| ------ | -------------------- | -------------------------------------- |
| GET    | `/operacoes`         | Lista as operações disponíveis         |
| POST   | `/operacoes/{nome}`  | Executa uma operação sobre um `.jff`   |

## Projeto

Projeto de pesquisa do Departamento de Sistemas de Informação — UFS.

**AutoLab-TC — 2026.2–2027.1**
