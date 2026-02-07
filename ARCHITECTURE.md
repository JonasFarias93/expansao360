# Arquitetura — EXPANSÃO360

## Visão Geral

O **EXPANSÃO360** é um sistema orientado a processos de expansão e operação de campo,
desenhado para garantir **padronização, rastreabilidade e governança**.

O princípio arquitetural central é a **separação rigorosa entre planejamento e execução**:

* **Registry (Cadastro Mestre)** → define *o que existe* e *como deve ser*
* **Operation (Execução de Campo)** → registra *o que aconteceu de fato*

Essa separação evita ambiguidade, preserva histórico
em processos físicos e permite evolução segura do sistema ao longo do tempo.

---

## Camadas Conceituais

### 1) Registry (Cadastro Mestre)

Responsável por manter entidades que funcionam como **fonte da verdade** do planejamento
organizacional e técnico.

**Exemplos de entidades:**

* Lojas
* Projetos
* Subprojetos
* Equipamentos
* Categorias e Tipos de Equipamento
* Kits e composição de itens

**Características:**

* Dados relativamente estáveis
* Alterações controladas e governadas
* Impactam apenas execuções futuras
* Não possuem histórico operacional

> O Registry **não depende** do domínio de execução.

---

### 2) Operation (Execução de Campo)

Responsável por registrar **eventos operacionais reais**,
com histórico imutável e rastreabilidade completa.

**Exemplos de entidades:**

* Chamados
* Itens de Execução
* Evidências (NF, carta de conteúdo, documentos de exceção)
* Fluxos de envio e retorno

**Características:**

* Alto volume transacional
* Histórico imutável
* Auditoria e rastreabilidade são requisitos centrais
* Suporte explícito a exceções operacionais

> A camada Operation **referencia** Registry, nunca o contrário.

---

## Entidade Central: Chamado

O **Chamado** é a unidade central da execução operacional.

Ele representa:

* um evento real no mundo físico
* com contexto organizacional
* com itens, status e evidências
* com impacto operacional e contábil

### Tipos de Chamado

* **ENVIO** → Matriz → Loja
* **RETORNO** → Loja → Matriz (fluxo inverso)

### Princípios fundamentais

* Chamados **finalizados são imutáveis**
* Correções e retornos geram **novos Chamados**
* Fluxo inverso nunca edita histórico existente

---

## Ciclo de Vida do Chamado

O ciclo de vida do Chamado separa explicitamente **planejamento** de **execução**:

1. **EM_ABERTURA**

   * Criação do Chamado
   * Geração dos Itens de Execução
   * Decisão de configuração (ex.: IP obrigatório)
   * Planejamento técnico

2. **ABERTO**

   * Promoção explícita após salvar o setup
   * Entrada na fila operacional

3. **EM_EXECUCAO / AGUARDANDO_***

   * Execução em campo
   * Bipagem, conferência e coleta de evidências

4. **FINALIZADO**

   * Estado terminal
   * Histórico preservado

Chamados em **EM_ABERTURA** **não aparecem** na fila operacional.

---

## Geração de Itens de Execução

Ao criar um Chamado:

* é gerado um **snapshot operacional**
* cada Item do Kit gera um Item de Execução
* alterações futuras no Kit **não afetam** Chamados já criados

Essa abordagem garante:

* rastreabilidade
* consistência histórica
* auditoria confiável

---

## Gates Operacionais

O avanço do Chamado é protegido por regras explícitas:

* **Liberação de NF** exige:

  * todos os itens rastreáveis bipados
  * todos os itens contáveis confirmados

* **Finalização** exige:

  * NF registrada (quando aplicável)
  * confirmação de coleta
  * evidências mínimas conforme o fluxo

Esses gates impedem estados inválidos e preservam a integridade do processo.

---

## Modelo em Camadas (Visão Lógica)

```
┌────────────────────────────┐
│ Interfaces / Adapters      │
│ Web • CLI • APIs (futuro)  │
└────────────▲───────────────┘
             │
┌────────────┴───────────────┐
│ Application                │
│ Casos de uso / Orquestração│
└────────────▲───────────────┘
             │
┌────────────┴───────────────┐
│ Domain                     │
│ Regras de negócio puras    │
└────────────────────────────┘
```

---

## Core de Domínio

O **core** do EXPANSÃO360:

* é independente de framework
* concentra regras de negócio
* não conhece UI, banco ou permissões
* é validado via testes automatizados (TDD)

**Exemplos de regras no core:**

* validação de finalização de Chamado
* regras de rastreabilidade (`tem_ativo`)
* fluxo inverso e exceções

---

## Adapters / Interfaces

### CLI

* Interface de linha de comando
* Compartilha o mesmo domínio
* Útil para testes, simulações e demonstrações

---

### Web (Django)

A camada Web atua como **adapter de entrega**, não como domínio.

**Apps principais:**

* `cadastro` → Registry
* `execucao` → Operation
* `iam` → Identidade e permissões

**Diretrizes:**

* Models Django **não contêm regras de negócio**
* Views orquestram casos de uso
* Templates apenas apresentam estado resolvido
* Django Admin é ferramenta técnica, não operacional

---

## IAM (Autorização)

O sistema adota um modelo **mínimo e explícito** de autorização:

* Baseado em **capabilities**
* Enforcement ocorre na camada Web
* O domínio permanece permission-agnostic

**Exemplos:**

* `execucao.chamado.finalizar`
* `execucao.evidencia.upload`
* `cadastro.editar`

---

## UI Web (Templates)

A UI é tratada como **adapter de apresentação**.

### Estrutura

```
templates/
├── base.html
├── partials/
│   ├── _sidebar.html
│   ├── _messages.html
│   └── ...
├── cadastro/
├── execucao/
│   └── components/
└── iam/
```

**Diretrizes:**

* Templates não contêm regra de negócio
* Componentes são reutilizáveis
* Estados vazios e mensagens são explícitos
* Tailwind via CDN (setup leve)

---

## Testes JavaScript

O projeto utiliza **Jest + jsdom** para validar comportamentos críticos de
JavaScript puro (sem framework), especialmente em formulários dinâmicos
(e.g. formsets).

Os testes ficam próximos aos arquivos estáticos de cada app Django e são
integrados ao fluxo de qualidade via Makefile.

---

## Princípios Arquiteturais

* Separação clara de responsabilidades
* Histórico nunca é destruído
* Fluxos explícitos (direto e inverso)
* Mudanças pequenas e rastreáveis
* Decisões registradas em `DECISIONS.md`

---

## Fora de Escopo (por enquanto)

* APIs públicas
* Integrações corporativas
* Hardening de infraestrutura
* Multitenancy
* Mobile / offline-first

Esses pontos serão abordados conforme a maturidade do produto.

---

## Conclusão

O **EXPANSÃO360** é projetado para **resistir ao tempo**:

* sem atalhos destrutivos
* sem acoplamento prematuro
* com rastreabilidade como princípio, não como feature

A arquitetura privilegia clareza, governança

---
