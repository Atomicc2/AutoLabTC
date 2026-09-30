# AutoLab-TC

Plataforma computacional para construção, transformação e manipulação de autômatos finitos, integrada ao JFLAP.

## Status

**Em fase de planejamento e definição da arquitetura.**

Neste momento, o projeto ainda não possui implementação. A equipe está discutindo a arquitetura, tecnologias, módulos e fluxo de funcionamento da aplicação.

## Objetivo

Desenvolver uma ferramenta web voltada ao estudo de Linguagens Formais e Teoria da Computação, permitindo trabalhar com:

- Expressões Regulares (ER);
- Autômatos Finitos Não Determinísticos (AFN);
- Autômatos Finitos Determinísticos (AFD);
- Arquivos `.jff` do JFLAP;
- Operações e transformações sobre autômatos;
- Visualização dos algoritmos passo a passo.

Um dos principais objetivos é permitir que o usuário acompanhe as **etapas intermediárias dos algoritmos**, e não apenas o resultado final.

## Arquitetura em discussão

A arquitetura atualmente proposta é composta por:

```text
Frontend
React / Angular
       │
       │ HTTP / REST
       ▼
Backend
Spring Boot
       │
       ├── Parser XML (.jff)
       │
       ├── Módulo de Expressões Regulares
       │       ├── Lexer
       │       ├── Parser
       │       └── AST
       │
       ├── Automata Core
       │       ├── AFN
       │       ├── AFD
       │       └── Operações
       │
       └── Trace Module
               │
               ├── Visualização das etapas
               └── Geração de gabarito/PDF
```

A arquitetura ainda está sujeita a alterações durante o desenvolvimento e as próximas reuniões da equipe.

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

## Tecnologias em estudo

- **Frontend:** React ou Angular
- **Backend:** Java + Spring Boot
- **Banco de dados:** PostgreSQL, se necessário
- **PDF:** Python + LaTeX, conforme necessidade definida no projeto
- **Integração:** JFLAP / arquivos `.jff`

## Projeto

Projeto de pesquisa do Departamento de Sistemas de Informação — UFS.

**AutoLab-TC — 2026.2–2027.1**
