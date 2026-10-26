# AGENT.md — AutoLabTC

Este arquivo é o "manual de instruções" do projeto AutoLabTC. Ele estabelece o contrato de desenvolvimento para todos os membros da equipe (Anderson, Luiz Felipe, Ulisses, Clara, Alisson e Eduardo) e para qualquer IA utilizada para codar. O objetivo é manter consistência de código, arquitetura e fluxo de trabalho, especialmente porque trabalhamos com revisão de código obrigatória via Pull Request.

---

## 1. Visão do Projeto

**AutoLab-TC** é uma plataforma computacional para construção, transformação e manipulação de autômatos finitos, integrada ao JFLAP. É um projeto de pesquisa do Departamento de Sistemas de Informação — UFS (período 2026.2–2027.1).

**Objetivo:** ferramenta web voltada ao estudo de Linguagens Formais e Teoria da Computação, permitindo trabalhar com:
- Expressões Regulares (ER);
- Autômatos Finitos Não Determinísticos (AFN);
- Autômatos Finitos Determinísticos (AFD);
- Arquivos `.jff` do JFLAP;
- Operações e transformações sobre autômatos;
- Registro das etapas intermediárias dos algoritmos.

**Diferencial:** as etapas intermediárias dos algoritmos são registradas pelo backend e geradas em **PDF** usando a biblioteca `pylatex`. A visualização passo a passo não será feita na página web (pelo menos por enquanto).

---

## 2. Stack e Versões

### Backend
- Python 3.12
- FastAPI
- Uvicorn
- `python-dotenv` (variáveis de ambiente)
- `defusedxml` (leitura segura de arquivos `.jff`/XML)
- `slowapi` (rate limiting)
- **`pylatex`** (geração de PDF das etapas dos algoritmos) — ainda não instalada/implementada

### Desenvolvimento backend
- `pytest`, `pytest-asyncio`, `httpx` (testes)
- `black`, `ruff` (formatação e lint)

### Frontend
- React 19 + TypeScript + Vite
- ESLint
- Nenhuma biblioteca de diagramação/grafo definida ainda — essa decisão deve ser tomada antes de iniciar o frontend de autômatos.

---

## 3. Convenções de Código

### Python (backend)
- Nomes de arquivos, pastas, variáveis e funções em **português** (conforme já iniciado no repositório).
- Classes em `PascalCase`, funções e variáveis em `snake_case`.
- Docstrings em português nas funções públicas.
- Formatação com `black`, lint com `ruff`.
- Tipagem opcional mas recomendada em serviços e núcleo.

### TypeScript (frontend)
- Interfaces e tipos em `src/tipos/`, escritos em **português** (ex: `Estado`, `Transicao`, `Automato`, `ErRegular`).
- Nomes de componentes React e arquivos: seguir a convenção do time (recomendado português para manter consistência com o backend).
- Sempre tipar respostas da API; evitar `any`.
- Componentes funcionais com hooks.

---

## 4. Padrões de Implementação

### Regra geral
Nunca pule camadas. O frontend não acessa o núcleo do backend diretamente; sempre vai pelas rotas → serviços. O backend não expõe lógica de autômatos direto nas rotas; sempre delega para o serviço ou núcleo.

### Backend — novo endpoint
1. Criar/adicionar rota em `api/rotas/automatos.py` (ou novo arquivo em `rotas/`).
2. Implementar regra de negócio em `api/servicos/`.
3. Se houver exceção específica, adicionar em `api/nucleo/excecoes.py`.
4. Configurações gerais ficam em `api/configuracoes/configuracao.py`.

### Frontend — novo componente/página
1. Criar interface em `src/tipos/` se representar um domínio novo.
2. Criar serviço de API em `src/servicos/` com funções tipadas que chamam o backend via `fetch` ou `axios`.
3. Criar componente em `src/componentes/` e/ou página em `src/paginas/`.
4. Registrar rotas no `App.tsx` (ou em um roteador, quando definido).

### Geração de PDF com `pylatex`
- As etapas intermediárias dos algoritmos (ER→AFN, AFN→AFD, minimização, etc.) são registradas pelo backend.
- A geração do PDF é feita com `pylatex`, rodando no lado do servidor (FastAPI).
- O frontend apenas solicita a geração/download do PDF via endpoint; não há renderização visual dos autômatos na página web por enquanto.
- O endpoint de PDF deve retornar o arquivo (ou link para download), não o conteúdo LaTeX bruto.

---

## 5. Regras para Uso de IA

Como alguns membros utilizarão IA para codar, as seguintes regras são obrigatórias:

- **Não commitar código gerado por IA sem revisar.** A IA pode inventar endpoints, importações inexistentes ou quebrar a camada de arquitetura.
- Sempre que pedir código à IA, cole o trecho relevante do `AGENT.md` e dos arquivos existentes (ex: `main.py`, `automato_service.py`) para ela manter o contexto.
- Peça à IA para seguir nomes em português (backend e tipos TypeScript) e para não criar pastas fora da estrutura definida.
- Ao gerar código Python, peça que use `black`/`ruff` compatível; ao gerar TypeScript, peça tipagem forte e sem `any`.
- Se a IA sugerir uma biblioteca nova, discuta com o time antes de instalar.

---

## 6. Estrutura Detalhada de Pastas

```
AutoLabTC/
├── AGENT.md
├── README.md
├── backend/
│   ├── api/
│   │   ├── main.py              # ponto de entrada (inicia o FastAPI)
│   │   ├── rotas/
│   │   │   ├── __init__.py
│   │   │   └── automatos.py     # camada de apresentação (endpoints)
│   │   ├── servicos/
│   │   │   ├── __init__.py
│   │   │   └── automato_service.py  # camada de negócio
│   │   ├── nucleo/
│   │   │   ├── __init__.py
│   │   │   └── excecoes.py      # exceções gerais
│   │   └── configuracoes/
│   │       ├── __init__.py
│   │       └── configuracao.py  # configurações (.env)
│   ├── testes/                  # testes pytest
│   ├── requisitos.txt           # dependências de produção
│   ├── requisitos-dev.txt       # dependências de desenvolvimento
│   ├── .env                     # variáveis de ambiente (local, não versionar)
│   └── .venv/                   # ambiente virtual (não versionar)
├── frontend/
│   ├── src/
│   │   ├── main.tsx             # ponto de entrada do React
│   │   ├── App.tsx              # componente raiz
│   │   ├── App.css
│   │   ├── index.css
│   │   ├── assets/              # recursos e imagens
│   │   ├── tipos/               # interfaces TypeScript (em português)
│   │   ├── servicos/            # chamadas HTTP ao backend
│   │   ├── componentes/         # componentes de tela
│   │   └── paginas/             # páginas/rotas da aplicação
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
```

---

## 7. Guia de Setup Rápido

### Backend
1. `cd backend`
2. `python -m venv .venv`
3. Ativar:
   - PowerShell: `.venv\Scripts\Activate.ps1`
   - CMD: `.venv\Scripts\activate.bat`
4. `pip install -r requisitos.txt`
5. Criar `.env` na pasta `backend/` com:
   ```env
   DEBUG=True
   SECRET_KEY=sua-chave-secreta-aqui
   ```
6. `uvicorn api.main:app --reload`
7. Acessar: `http://localhost:8000` (Swagger em `/docs`)

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`
4. Acessar: endereço indicado pelo Vite (geralmente `http://localhost:5173`)

---

## 8. Fluxo de Trabalho (Trello + Git)

- A branch `main` está protegida (Pull Request obrigatório com aprovação de revisor).
- Cada tarefa do Trello vira uma branch: `tarefa/<id-trello>-descricao-resumida` (ou `tarefa/descricao-resumida` se não houver card no Trello).
- Para esta tarefa de criação do AGENT.md (sem card no Trello), foi usada a branch: `tarefa/agent-md-padroes-projeto`.
- Commit apenas após revisão de código (pair ou Pull Request).
- Main branch sempre em estado funcional; não fazer `push` direto na main sem revisão.
- Atualizar o card do Trello para "Em revisão" quando abrir PR, e "Concluído" apenas após merge.

---

## 9. Testes e Qualidade

- Backend: testes em `backend/testes/` com `pytest`. Cobrir serviços e exceções do núcleo.
- Frontend: `npm run lint` antes de commitar.
- Backend: `ruff check .` e `black .` antes de commitar.

---

## 10. Integração JFLAP / `.jff`

- Arquivos `.jff` são XML. Usar `defusedxml` para parsing seguro (já em `requisitos.txt`).
- Definir esquema de dados interno do autômato (estados, transições, inicial, finais) separado do formato `.jff`.
- Funções de importação (`.jff` → modelo interno) e exportação (modelo interno → `.jff`) ficam no serviço ou núcleo de operações, não nas rotas.

---

## 11. Responsabilidades Iniciais (sugestão para dividir no Trello)

| Área | Responsabilidades |
|------|-------------------|
| Backend / API | Rotas, serviços, configuração |
| Núcleo de operações | Lógica de autômatos (ER→AFN, AFN→AFD, minimização, operações), parsing `.jff`, registro de etapas intermediárias |
| Frontend | Páginas, componentes, serviços de API, tipos TypeScript |
| PDF / pylatex | Geração de PDF das etapas dos algoritmos no backend |
| DevOps / Qualidade | Testes, CI básico, `.env`, documentação de setup |

*(Ajustar conforme afinidade de cada membro: Anderson, Luiz Felipe, Ulisses, Clara, Alisson, Eduardo.)*

---

## 12. Convencional Commits (em português)

Os tipos de commit são escritos em **português**:

| Tipo em português | Quando usar |
|-------------------|-------------|
| `funcionalidade` | Nova funcionalidade |
| `correção` | Correção de bug |
| `documentação` | Alterações apenas de documentação |
| `estilo` | Formatação, ponto-e-vírgula, etc. (sem mudar lógica) |
| `refatoração` | Mudança de código que não corrige bug nem adiciona feature |
| `teste` | Adição ou correção de testes |
| `tarefa` | Tarefas de manutenção, dependências, build, setup |

**Formato:**
```
<tipo>: <descricao curta em português>
```

Opcionalmente, com escopo:
```
<tipo>(escopo): <descricao>
```

**Exemplos:**
- `funcionalidade: endpoint listar automatos`
- `correção: exceção automato não encontrado`
- `documentação: readme com instruções de setup`
- `estilo: ajustar indentacao no service`
- `refatoração: separar servico de automato em camadas`
- `teste: adicionar teste unitário do automato service`
- `tarefa: atualizar dependencias do requirements`
- `funcionalidade(backend): adicionar endpoint de automatos`

---

## 13. Como Usar Este AGENT.md com IA

1. Ao iniciar uma sessão com a IA, anexe ou cole o `AGENT.md` no prompt.
2. Especifique: "Use a arquitetura em camadas rotas → serviços → núcleo descrita no AGENT.md."
3. Peça para a IA retornar apenas o código do arquivo solicitado, sem alterar arquivos existentes sem aviso.
4. Após receber o código, compare com a estrutura de pastas e convenções antes de colar no projeto.

---