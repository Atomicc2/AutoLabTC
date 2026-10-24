# AutoLab-TC

Plataforma computacional para construção, transformação e manipulação de autômatos finitos, integrada ao JFLAP.

## Status

**Em fase de planejamento e definição da arquitetura.**

Neste momento, o projeto ainda não possui implementação completa. A equipe está discutindo a arquitetura, tecnologias, módulos e fluxo de funcionamento da aplicação.

## Objetivo

Desenvolver uma ferramenta web voltada ao estudo de Linguagens Formais e Teoria da Computação, permitindo trabalhar com:

- Expressões Regulares (ER);
- Autômatos Finitos Não Determinísticos (AFN);
- Autômatos Finitos Determinísticos (AFD);
- Arquivos `.jff` do JFLAP;
- Operações e transformações sobre autômatos;
- Visualização dos algoritmos passo a passo.

Um dos principais objetivos é permitir que o usuário acompanhe as **etapas intermediárias dos algoritmos**, e não apenas o resultado final.

## Arquitetura em camadas

O projeto é dividido em duas partes principais: **backend** (FastAPI em Python) e **frontend** (React com TypeScript e Vite). Cada lado segue uma organização simples de pastas, com nomes em português.

```
AutoLabTC/
├── backend/
│   ├── api/
│   │   ├── main.py              # ponto de entrada (inicia o FastAPI)
│   │   ├── rotas/               # camada de apresentação (endpoints)
│   │   │   └── automatos.py
│   │   ├── servicos/            # camada de negócio (regras da aplicação)
│   │   │   └── automato_service.py
│   │   └── nucleo/              # classes gerais (configurações, exceções)
│   │       ├── configuracao.py
│   │       └── excecoes.py
│   ├── testes/
│   ├── requisitos.txt           # dependências de produção
│   ├── requisitos-dev.txt       # dependências de desenvolvimento
│   └── .env                     # variáveis de ambiente
├── frontend/
│   └── src/
│       ├── main.tsx             # ponto de entrada do React
│       ├── App.tsx              # componente raiz
│       ├── App.css
│       ├── index.css
│       ├── assets/              # recursos e imagens
│       ├── servicos/            # chamadas HTTP ao backend
│       │   └── automatoApi.ts
│       ├── componentes/         # componentes de tela
│       │   └── automatos/
│       ├── paginas/             # páginas/rotas da aplicação
│       │   ├── Inicio.tsx
│       │   └── Automatos.tsx
│       ├── tipos/               # interfaces TypeScript
│       │   └── automato.ts
└── README.md
```

### Como as camadas se comunicam

O fluxo de dados segue este caminho:

1. **React (páginas e componentes)** → interage com o usuário.
3. **Serviços (servicos)** → fazem chamadas HTTP para o backend.
4. **Rotas (api/rotas)** → recebem as requisições no backend.
5. **Serviços (api/servicos)** → aplicam as regras de negócio.
6. **Núcleo (api/nucleo)** → fornece configurações e exceções gerais.

## Tecnologias

- **Frontend:** React 19 + TypeScript + Vite
- **Backend:** FastAPI + Python 3.12
- **PDF:** Python + LaTeX, conforme necessidade definida no projeto
- **Integração:** JFLAP / arquivos `.jff`

## Principais funcionalidades planejadas

- Importação de autômatos através de arquivos `.jff`;
- Conversão de Expressões Regulares para AFN;
- Operações sobre autômatos;
- Conversão AFN → AFD;
- Minimização de AFD;
- Exportação para `.jff`;
- Registro das etapas intermediárias dos algoritmos;
- Visualização passo a passo;
- Possível geração de PDF com as etapas do processo.

## Como clonar o repositório

Abra o terminal e execute:

```bash
git clone https://github.com/Atomicc2/AutoLabTC
cd AutoLabTC
```

## Como instalar e iniciar o backend

O backend está na pasta `backend/` e utiliza o FastAPI.

### 1. Entre na pasta do backend

```bash
cd backend
```

### 2. Crie um ambiente virtual

Um ambiente virtual isola as dependências do projeto do restante do seu sistema.

```bash
python -m venv .venv
```

### 3. Ative o ambiente virtual

No Linux ou Mac:

```bash
source .venv/bin/activate
```

No Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

No Windows (CMD):

```cmd
.venv\Scripts\activate.bat
```

Quando ativado, você verá `(.venv)` no início da linha de comando do terminal.

### 4. Instale as dependências de produção

```bash
pip install -r requisitos.txt
```

### 5. Instale as dependências de desenvolvimento (opcional)

Útil se você for rodar testes ou formatar o código:

```bash
pip install -r requisitos-dev.txt
```

### 6. Configure as variáveis de ambiente

Crie um arquivo chamado `.env` dentro da pasta `backend/` com o seguinte conteúdo:

```env
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
```

Você pode ajustar esses valores conforme necessário.

### 7. Inicie o servidor backend

```bash
uvicorn api.main:app --reload
```

O parâmetro `--reload` faz com que o servidor reinicie automaticamente sempre que você salvar alterações nos arquivos.

### 8. Acesse o backend

Abra o navegador e acesse:

- Página inicial: `http://localhost:8000`
- Documentação automática da API (Swagger): `http://localhost:8000/docs`

## Como instalar e iniciar o frontend

O frontend está na pasta `frontend/` e utiliza React com TypeScript e Vite.

### 1. Entre na pasta do frontend

```bash
cd frontend
```

### 2. Instale as dependências

```bash
npm install
```

Isso baixará todas as bibliotecas listadas no `package.json` e criará a pasta `node_modules/`.

### 3. Inicie o servidor de desenvolvimento

```bash
npm run dev
```

### 4. Acesse o frontend

O terminal mostrará algo como:

```
  VITE v6.x  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

Abra o navegador e acesse o endereço indicado (geralmente `http://localhost:5173`).

## Como rodar o projeto completo

Para ter o backend e o frontend funcionando ao mesmo tempo, você precisa de dois terminais abertos:

**Terminal 1 — Backend:**

```bash
cd AutoLabTC/backend
source .venv/bin/activate        # ou .venv\Scripts\activate no Windows
uvicorn api.main:app --reload
```

**Terminal 2 — Frontend:**

```bash
cd AutoLabTC/frontend
npm install                      # apenas na primeira vez
npm run dev
```

Com ambos rodando, o frontend (React) fará chamadas HTTP para o backend (FastAPI) e a aplicação estará completa.

## Comandos úteis

### Backend

| Comando | Descrição |
|---------|-----------|
| `uvicorn api.main:app --reload` | Inicia o servidor com recarregamento automático |
| `pytest` | Executa os testes (requer `requisitos-dev.txt`) |
| `ruff check .` | Verifica problemas de estilo no código |
| `black .` | Formata automaticamente o código Python |

### Frontend

| Comando | Descrição |
|---------|-----------|
| `npm run dev` | Inicia o servidor de desenvolvimento |
| `npm run build` | Gera a versão para produção |
| `npm run lint` | Verifica problemas de estilo no código |
| `npm run preview` | Pré-visualiza a build de produção localmente |

## Projeto

Projeto de pesquisa do Departamento de Sistemas de Informação — UFS.

**AutoLab-TC — 2026.2–2027.1**
