# Arquitetura — EXPANSÃO360

## Visão Geral

O **EXPANSÃO360** é um sistema orientado a processos de expansão e operação de campo,
desenhado para garantir **padronização, rastreabilidade e governança**.

O princípio arquitetural central é a **separação rigorosa entre planejamento e execução**:

- **Registry (Cadastro Mestre)** → define *o que existe* e *como deve ser*
- **Operation (Execução de Campo)** → registra *o que aconteceu de fato*

Essa separação evita ambiguidade, preserva histórico
e permite evolução segura do sistema.

---

## Camadas Conceituais

### 1) Registry (Cadastro Mestre)

Responsável por manter entidades que funcionam como **fonte da verdade** do planejamento.

**Exemplos:**
- Lojas
- Projetos
- Subprojetos
- Equipamentos
- Kits e composição de itens

**Características:**
- Dados relativamente estáveis
- Alterações controladas
- Impactam apenas execuções futuras
- Não possuem histórico operacional

> Registry **não depende** de Operation.

---

### 2) Operation (Execução de Campo)

Responsável por registrar **eventos operacionais reais**,
com histórico imutável e rastreabilidade completa.

**Exemplos:**
- Chamados
- Itens de execução
- Evidências (NF, carta de conteúdo, exceções)
- Fluxos de envio e retorno

**Características:**
- Alto volume transacional
- Histórico imutável
- Auditoria e rastreabilidade são essenciais
- Suporte explícito a exceções

> Operation **referencia** Registry, nunca o contrário.

---

## Entidade Central: Chamado

O **Chamado** é a unidade central da execução operacional.

Ele representa:
- uma operação real
- com contexto organizacional
- com itens, status e evidências
- com impacto operacional e contábil

### Tipos de Chamado
- **ENVIO** → Matriz → Loja
- **RETORNO** → Loja → Matriz (fluxo inverso)

### Princípios
- Chamados **finalizados são imutáveis**
- Correções geram **novo Chamado**
- Fluxo inverso nunca edita histórico existente

---

## Geração de Itens de Execução

Ao criar um Chamado:
- um **snapshot operacional** é gerado
- cada Item do Kit gera um Item de Execução
- alterações futuras no Kit **não afetam** Chamados já criados

Isso garante:
- rastreabilidade
- consistência histórica
- auditoria confiável

---

## Modelo em Camadas (Visão Lógica)

┌────────────────────┐
│ Interfaces │ → Web / CLI / (futuras APIs)
└─────────▲──────────┘
│
┌─────────┴──────────┐
│ Application │ → Casos de uso / orquestração
└─────────▲──────────┘
│
┌─────────┴──────────┐
│ Domain │ → Regras de negócio puras
└────────────────────┘


---

## Core de Domínio

O **core** do EXPANSÃO360:

- é independente de framework
- concentra regras de negócio
- não conhece UI, banco ou permissões
- é validado via testes automatizados (TDD)

Exemplos de regras no core:
- validação de finalização de Chamado
- regras de rastreabilidade (`tem_ativo`)
- fluxo inverso e exceções

---

## Adapters / Interfaces

### CLI
- Interface de linha de comando
- Compartilha o mesmo domínio
- Útil para testes, simulações e apresentação

---

### Web (Django)

A camada Web atua como **adapter de entrega**, não como domínio.

Apps principais:
- `cadastro` → Registry
- `execucao` → Operation
- `iam` → Identidade e permissões

**Diretrizes:**
- Models Django **não contêm regras de negócio**
- Views orquestram casos de uso
- Templates apenas apresentam estado resolvido
- Django Admin é ferramenta técnica, não operacional

---

## IAM (Autorização)

O sistema adota um modelo **mínimo e explícito** de autorização:

- Baseado em **capabilities**
- Enforcement ocorre na camada Web
- O domínio permanece permission-agnostic

Exemplos:
- `execucao.chamado.finalizar`
- `execucao.evidencia.upload`
- `cadastro.editar`

---

## UI Web (Templates)

A UI é tratada como **adapter de apresentação**.

### Estrutura

templates/
├── base.html
├── partials/
│ ├── _sidebar.html
│ ├── _messages.html
│ └── ...
├── cadastro/
├── execucao/
│ └── components/
└── iam/


**Diretrizes:**
- Templates não contêm regra de negócio
- Componentes são reutilizáveis
- Estados vazios e mensagens são explícitos
- Tailwind via CDN (setup leve)

---

## Princípios Arquiteturais

- Separação clara de responsabilidades
- Histórico nunca é destruído
- Fluxos explícitos (direto e inverso)
- Mudanças pequenas e rastreáveis
- Decisões registradas em `DECISIONS.md`

---

## Fora de Escopo (por enquanto)

- APIs públicas
- Integrações corporativas
- Hardening de infraestrutura
- Multitenancy
- Mobile / offline-first

Esses pontos serão abordados conforme a maturidade do produto.

---

## Conclusão

O EXPANSÃO360 é projetado para **resistir ao tempo**:
- sem atalhos destrutivos
- sem acoplamento prematuro
- com rastreabilidade como princípio, não como feature

A arquitetura privilegia clareza, governança
e evolução contínua com baixo risco.
