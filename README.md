# AutoLab-TC

Plataforma computacional para construção, transformação e manipulação de autômatos finitos, integrada ao JFLAP.

## Status atual

O projeto possui um **MVP funcional da operação de complemento de AFD**, integrado do frontend ao backend:

- importação de autômatos a partir de arquivos `.jff`;
- cálculo do complemento de um AFD;
- registro das etapas intermediárias da operação;
- geração de relatório PDF com os diagramas de cada etapa;
- exportação do autômato resultante para `.jff`;
- download dos dois arquivos em um único `.zip`.

A operação de complemento é a única operação disponível no momento. As demais transformações sobre autômatos ainda não estão implementadas.

## Objetivo

Desenvolver uma ferramenta web voltada ao estudo de Linguagens Formais e Teoria da Computação, permitindo trabalhar com:

- Expressões Regulares (ER);
- Autômatos Finitos Não Determinísticos (AFN);
- Autômatos Finitos Determinísticos (AFD);
- arquivos `.jff` do JFLAP;
- operações e transformações sobre autômatos.

O diferencial do projeto é registrar as **etapas intermediárias dos algoritmos**. Em vez de entregar apenas o resultado final, o backend gera um relatório em PDF com o autômato em cada passo do processo, usando `pylatex` e TikZ.

## Funcionalidades disponíveis

| Funcionalidade | Situação |
|---|---|
| Importar autômato de um arquivo `.jff` | Disponível |
| Validar o formato `.jff` | Disponível |
| Calcular o complemento de um AFD | Disponível |
| Completar o AFD com estado sumidouro, quando necessário | Disponível |
| Inverter estados finais e não finais | Disponível |
| Registrar as etapas intermediárias da operação | Disponível |
| Gerar PDF com os diagramas das etapas (TikZ) | Disponível |
| Exportar o autômato resultante para `.jff` | Disponível |
| Empacotar `.jff` + `.pdf` em um `.zip` | Disponível |
| Interface web para importar, executar e baixar | Disponível |

> O complemento exige um **AFD**. Se o arquivo descrever um AFN, a API responde com erro `422`, pois ainda não existe conversão de AFN para AFD.

## Arquitetura em camadas

O projeto é dividido em **backend** (FastAPI + Python) e **frontend** (React + TypeScript + Vite).

O fluxo de uma requisição é:

```text
React (página/componentes)
    ↓ fetch multipart/form-data
POST /operacoes/complemento
    ↓
api/rotas/operacoes_rotas.py       (camada de apresentação)
    ↓
api/servicos/operacoes_servico.py  (regra de negócio)
    ↓
api/nucleo/                        (modelo e operações sobre autômatos)
    ↓
api/relatorios/                    (PDF, TikZ e escape de LaTeX)
    ↓
RespostaOperacao → arquivo .zip
```

O frontend nunca acessa o núcleo diretamente, e as rotas não implementam lógica de autômatos. As exceções de domínio são convertidas em respostas HTTP pelos tratadores globais em `api/rotas/tratadores.py`.

### Estrutura de pastas

```text
AutoLabTC/
├── AGENT.md                         # convenções e fluxo de trabalho da equipe
├── README.md
├── backend/
│   ├── api/
│   │   ├── main.py                  # ponto de entrada do FastAPI
│   │   ├── configuracoes/
│   │   │   └── configuracao.py      # variáveis de ambiente (.env)
│   │   ├── rotas/
│   │   │   ├── operacoes_rotas.py   # endpoints de operações
│   │   │   └── tratadores.py        # conversão de exceções em HTTP
│   │   ├── servicos/
│   │   │   └── operacoes_servico.py # orquestração das operações
│   │   ├── nucleo/
│   │   │   ├── automato_finito.py   # modelo do autômato
│   │   │   ├── estado.py
│   │   │   ├── transicao.py
│   │   │   ├── excecoes.py          # exceções de domínio
│   │   │   ├── dto/
│   │   │   │   ├── etapa.py
│   │   │   │   ├── resposta_operacao.py
│   │   │   │   └── resultado_operacao.py
│   │   │   ├── operacao/
│   │   │   │   └── complemento.py   # algoritmo de complemento
│   │   │   └── utilitario/
│   │   │       ├── utilitarios_jff.py
│   │   │       └── utilitarios_operacoes.py
│   │   └── relatorios/
│   │       ├── documento.py         # geração do PDF com pylatex
│   │       ├── diagrama.py          # autômato → TikZ
│   │       └── latex.py             # escape de caracteres especiais
│   ├── testes/                      # testes com pytest
│   ├── requisitos.txt               # dependências de produção
│   ├── requisitos-dev.txt           # dependências de desenvolvimento
│   ├── ruff.toml
│   ├── .env                         # local, não versionado
│   └── .venv/                       # local, não versionado
├── frontend/
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── componentes/
│   │   │   ├── botao-principal.tsx
│   │   │   ├── formulario-operacao.tsx
│   │   │   ├── importacao/
│   │   │   │   ├── botao-importar-jff.tsx
│   │   │   │   └── painel-importacao.tsx
│   │   │   └── selecao/
│   │   │       └── painel-selecao.tsx
│   │   ├── paginas/
│   │   │   └── pagina-inicial.tsx
│   │   └── assets/
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
└── .gitignore
```

## API

Base local: `http://localhost:8000`

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/` | Página inicial de teste da API |
| `POST` | `/operacoes/complemento` | Calcula o complemento de um AFD e retorna um `.zip` |

### `POST /operacoes/complemento`

- Conteúdo: `multipart/form-data`
- Campo obrigatório: `arquivo` — arquivo `.jff`
- Resposta de sucesso: `200 OK`, `application/zip`
- Nome do download: `complemento.zip`
- Conteúdo do `.zip`:
  - `complemento.jff` — autômato resultante;
  - `complemento.pdf` — relatório com as etapas intermediárias.

Exemplo com `curl`:

```bash
curl -X POST http://localhost:8000/operacoes/complemento \
  -F "arquivo=@meu-automato.jff" \
  --output complemento.zip
```

Exemplo de resposta de erro:

```json
{
  "detail": "A operação complemento exige um AFD. O autômato informado é não determinístico; converta-o para AFD antes."
}
```

| Código | Situação |
|---|---|
| `200` | Operação concluída; `.zip` retornado |
| `422` | `.jff` inválido, autômato inconsistente ou autômato não determinístico |
| `503` | Não foi possível gerar o PDF (por exemplo, `pdflatex` indisponível) |

## Tecnologias

- **Backend:** Python 3.12, FastAPI, Uvicorn
- **Frontend:** React 19, TypeScript, Vite
- **Leitura de `.jff`:** `defusedxml`
- **PDF:** `pylatex` + LaTeX (`pdflatex`) + TikZ
- **Testes:** `pytest`, `httpx`
- **Qualidade:** `ruff`, `black`, ESLint
- **Integração:** JFLAP / arquivos `.jff`

## Pré-requisitos

- Python 3.12
- Node.js 20.19+ ou 22.12+ (recomendado: versão LTS)
- npm
- LaTeX com `pdflatex` disponível no `PATH` (necessário para gerar o PDF)

> O `pylatex` é instalado pelo `pip`, mas **não inclui o LaTeX**. Ele apenas escreve o arquivo `.tex` e chama o `pdflatex`.

## Instalação do LaTeX

### Windows — MiKTeX (recomendado)

1. Verifique se o `pdflatex` já está instalado:

```powershell
pdflatex --version
```

2. Se não estiver, instale o MiKTeX pelo `winget`:

```powershell
winget install --id MiKTeX.MiKTeX -e --accept-package-agreements --accept-source-agreements
```

3. Feche e reabra o terminal para atualizar o `PATH` e confirme:

```powershell
pdflatex --version
```

4. Ative a instalação automática de pacotes ausentes:

```powershell
initexmf --set-config-value=[MPM]AutoInstall=1
```

5. Instale os pacotes usados pelo projeto:

```powershell
miktex packages install pgf lm
```

> Em uma instalação compartilhada, use `initexmf --admin --set-config-value=[MPM]AutoInstall=1` em um terminal como administrador.

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install texlive-latex-base texlive-fonts-recommended texlive-pictures lmodern
pdflatex --version
```

- `texlive-pictures` fornece o `pgf` e as bibliotecas TikZ.
- `lmodern` fornece a fonte Latin Modern.

### macOS

Instalação completa:

```bash
brew install --cask mactex-no-gui
```

Instalação mínima:

```bash
brew install --cask basictex
sudo tlmgr update --self
sudo tlmgr install pgf lm
```

## Como clonar o repositório

```bash
git clone https://github.com/Atomicc2/AutoLabTC
cd AutoLabTC
```

## Como instalar e iniciar o backend

O backend está em `backend/` e utiliza FastAPI.

### 1. Entre na pasta do backend

```bash
cd backend
```

### 2. Crie o ambiente virtual

```bash
python -m venv .venv
```

### 3. Ative o ambiente virtual

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

Windows (CMD):

```cmd
.venv\Scripts\activate.bat
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 4. Instale as dependências

Dependências de produção:

```bash
pip install -r requisitos.txt
```

Dependências de desenvolvimento (testes e formatação):

```bash
pip install -r requisitos-dev.txt
```

O `requisitos-dev.txt` já inclui o `requisitos.txt`.

### 5. Configure as variáveis de ambiente

Crie o arquivo `backend/.env`:

```env
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
```

O arquivo `.env` não deve ser versionado.

### 6. Inicie o servidor

```bash
uvicorn api.main:app --reload
```

O `--reload` reinicia o servidor automaticamente quando os arquivos são alterados.

### 7. Acesse

- API: `http://localhost:8000`
- Documentação Swagger: `http://localhost:8000/docs`

## Como instalar e iniciar o frontend

O frontend está em `frontend/` e utiliza React com TypeScript e Vite.

### 1. Entre na pasta do frontend

```bash
cd frontend
```

### 2. Instale as dependências

```bash
npm install
```

### 3. Inicie o servidor de desenvolvimento

```bash
npm run dev
```

### 4. Acesse

O terminal mostrará o endereço, geralmente `http://localhost:5173`.

Em desenvolvimento, o Vite encaminha as requisições para `/operacoes` ao backend em `http://localhost:8000`. Para usar outra porta, defina a variável `BACKEND_URL` antes de iniciar o frontend:

```powershell
$env:BACKEND_URL = "http://localhost:9000"
npm run dev
```

## Como rodar o projeto completo

Abra dois terminais.

**Terminal 1 — Backend:**

```bash
cd backend
# ative o ambiente virtual
uvicorn api.main:app --reload
```

**Terminal 2 — Frontend:**

```bash
cd frontend
npm install
npm run dev
```

## Como usar a aplicação

1. Acesse o frontend no navegador.
2. Selecione a operação **Complemento**.
3. Importe um arquivo `.jff` que represente um **AFD**.
   - O arquivo deve ter extensão `.jff` e no máximo 1 MB.
4. Clique em **Gerar Autômato**.
5. Aguarde o processamento.
6. Clique em **Baixar .zip** para baixar o resultado.

O `.zip` contém:

- o autômato resultante em `.jff`, que pode ser aberto no JFLAP;
- o relatório `.pdf` com o autômato original, a etapa de completagem (quando necessária) e o autômato complemento.

## Testes e qualidade

### Backend

Execute a partir de `backend/` com o ambiente virtual ativo:

| Comando | Descrição |
|---|---|
| `pytest` | Executa todos os testes |
| `ruff check .` | Verifica problemas de estilo |
| `black .` | Formata o código Python |
| `black --check .` | Apenas verifica a formatação |

Testes específicos:

```bash
pytest testes/test_complemento.py -v
pytest testes/test_operacoes_rotas.py -v
pytest testes/test_relatorio_pdf.py -v
```

Os testes que geram PDF usam `pytest.mark.skipif` e são automaticamente ignorados quando o `pdflatex` não está no `PATH`.

### Frontend

Execute a partir de `frontend/`:

| Comando | Descrição |
|---|---|
| `npm run lint` | Verifica problemas de estilo |
| `npm run build` | Gera a versão de produção |
| `npm run preview` | Pré-visualiza a build de produção |

## Fluxo de contribuição

- A branch `main` é protegida e recebe alterações via Pull Request com revisão.
- Cada tarefa gera uma branch no formato `tarefa/<id-trello>-descricao-resumida` ou `tarefa/descricao-resumida`.
- Atualize o card do Trello para “Em revisão” ao abrir o PR e para “Concluído” após o merge.
- Commits seguem o padrão em português:

```text
<tipo>: <descricao curta>
<tipo>(escopo): <descricao>
```

Tipos usados pelo time: `funcionalidade`, `correção`, `documentação`, `estilo`, `refatoração`, `teste` e `tarefa`.

Exemplos:

```text
funcionalidade: endpoint de complemento
correção: tratamento de jff inválido
documentação: atualizar readme com estado atual
teste: cobrir rejeição de xml com entidades
```

Consulte o [`AGENT.md`](AGENT.md) para as convenções completas de código, arquitetura e fluxo de trabalho.

## Projeto

Projeto de pesquisa do Departamento de Sistemas de Informação — UFS.

Equipe: Anderson, Luiz Felipe, Ulisses, Clara, Alisson e Eduardo.

**AutoLab-TC — 2026.2–2027.1**
