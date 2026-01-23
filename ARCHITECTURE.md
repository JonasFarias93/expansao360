# Arquitetura — EXPANSÃO360

## Visão Geral

O EXPANSÃO360 é um sistema orientado a processos de expansão e operação de campo.  
O princípio central é separar claramente:

- **Cadastro administrativo (mestre / estático)**: define o que existe e como deve ser.
- **Operação de campo (transacional / execução)**: registra o que foi executado, com rastreabilidade e histórico.

Essa separação reduz ambiguidade, melhora governança e permite evolução do sistema com segurança.

---

## Camadas Conceituais

### 1) Registry (Cadastro Mestre)

Responsável por manter entidades **fonte da verdade** do planejamento e da padronização.

**Exemplos típicos:**
- Lojas / locais
- Projetos / iniciativas
- Padrões, layouts, checklists e regras
- Materiais e componentes aprovados

**Características:**
- Alterações são controladas (governança)
- Dados são relativamente estáveis
- Versionamento e auditoria são importantes

---

### 2) Operation (Execução de Campo)

Responsável por registrar eventos e evidências do que aconteceu na prática.

**Exemplos típicos:**
- Montagens realizadas
- Inspeções / validações
- Evidências (fotos, anexos, assinaturas)
- Ocorrências e retrabalhos

**Características:**
- Alto volume transacional
- Histórico e rastreabilidade são essenciais
- Permite reprocessamento e auditoria

---

## Diretrizes de Arquitetura

### Separação de responsabilidades

- Registry **não depende** de Operation para existir.
- Operation **referencia** Registry (nunca o contrário).

---

### Modelo em camadas (visão lógica)

- **Domain**: regras de negócio puras (entidades, value objects, políticas)
- **Application**: casos de uso (orquestração, comandos e queries)
- **Infrastructure**: banco, filas, storage, integrações externas
- **Interfaces**: API / CLI / UI (entrada do sistema)

---

### Princípios

- Código limpo e modular
- Mudanças pequenas e rastreáveis
- Commits pequenos e descritivos
- Decisões arquiteturais registradas em `DECISIONS.md`

---

## Fora de Escopo (por enquanto)

- Detalhes de stack (linguagem / framework) antes da decisão formal
- Estrutura de pastas definitiva antes do primeiro esqueleto do app
- Regras de autorização e perfis (definidas após o fluxo base)

---

## Implementação Atual (Core + Adapters)

O EXPANSÃO360 adota uma arquitetura em camadas, onde o **core de domínio**
permanece independente de frameworks e interfaces.

As interfaces (CLI / Web) atuam como **adapters**, responsáveis por entrada,
apresentação e orquestração, **sem concentrar regras de negócio**.

---

### Core

- Regras de negócio puras (Domain / Application)
- Entidades como **Chamado**, **Equipamento** e **Kit**
- Casos de uso validados via testes automatizados (TDD)

---

### Adapters / Interfaces

#### CLI

- Interface de linha de comando para operações do sistema
- Não depende da camada Web

---

#### Web (Django)

A camada Web é implementada com **Django**, organizada em apps:

- `cadastro`: Registry (Cadastro Mestre)
- `execucao`: Operation (Chamados e execução)
- `iam`: Identidade, autenticação e permissões (em evolução)

**Diretrizes:**
- A Web atua como camada de entrega e persistência.
- Models Django **não contêm regras de negócio** do core.
- A UI Web é tratada como adapter: entrada, apresentação e orquestração.

---

## UI Web (Templates e Static Files)

A interface Web (Django) segue o papel de **adapter de apresentação**, sem concentrar regras de negócio.

---

### Organização de Templates

A estrutura de templates é dividida por responsabilidade:


**Inclui:**
- `base.html`
- `partials/` — estruturas de layout (sidebar, topbar, mensagens)
- `components/` — componentes reutilizáveis e agnósticos de domínio

Templates específicos de execução:


**Subpastas:**
- `components/` — componentes reutilizáveis exclusivos da execução

**Diretrizes:**
- Templates globais não conhecem regras de negócio.
- Templates por app podem refletir estado e fluxo já resolvidos pelo backend.

---

### Organização de Static Files

Os arquivos estáticos seguem separação por app e tipo:


**Diretrizes:**
- Nenhum CSS ou JS crítico fica inline.
- Templates referenciam arquivos estáticos via `{% static %}`.
- JavaScript atua apenas em comportamento de UI (eventos, submits, feedback visual).
- Nenhuma regra de negócio reside em JS ou CSS.

---

Essa organização reforça:
- Isolamento entre UI e domínio
- Previsibilidade de manutenção
- Facilidade de evolução para pipeline de build futuro (ex.: Tailwind, bundler)
