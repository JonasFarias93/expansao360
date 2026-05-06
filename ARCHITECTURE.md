# Arquitetura — EXPANSÃO360

Este documento descreve **como o sistema EXPANSÃO360 é construído** —
quais apps existem, o que cada um faz, como eles se comunicam
e onde cada regra de negócio vive.

> O que o sistema deve fazer: consulte `REQUIREMENTS.md`.
> Decisões técnicas pontuais: consulte `DECISIONS/`.
> Fonte de verdade: código em `web/`, ADRs em `DECISIONS/`, testes automatizados.

Última revisão: 2026-05-06

---

# 1. Princípio Central

A arquitetura do EXPANSÃO360 é organizada em torno de uma regra simples:

> **Apps de baixo fornecem. Apps de cima consomem.**
> **Nenhum app conhece quem o consome.**

Isso significa:

- `cadastro/` não sabe que `chamados/` existe
- `chamados/` não sabe que `execucao/` existe
- `execucao/` não sabe que `historico/` existe

Essa regra protege o sistema de acoplamento acidental.
Quando você muda `historico/`, `chamados/` não quebra.
Quando você muda `cadastro/`, nenhum chamado é afetado.

---

# 2. Separação Registry vs Operation

O princípio arquitetural central é a separação entre dois mundos:

**Registry (Cadastro Mestre)**
— define o que existe e como deve ser.
— dados estruturais, relativamente estáveis.
— alterações impactam apenas operações futuras.
— nunca guarda histórico operacional.

**Operation (Execução de Campo)**
— registra o que aconteceu de fato.
— eventos reais, imutáveis.
— histórico preservado.
— referencia o Registry, nunca o contrário.

---

# 3. Mapa de Apps

## Visão geral

| App          | Status        | Papel                                               |
|--------------|---------------|-----------------------------------------------------|
| `cadastro/`  | Existe        | Registry — entidades estruturais                    |
| `chamados/`  | Existe        | Domínio central — Chamado, ciclo de vida, gates     |
| `execucao/`  | Existe        | Operação em campo — sessão, fila, log               |
| `iam/`       | Existe        | Capabilities — o que cada ação exige                |
| `redes/`     | Existe (parcial) | Validação de IP e regras de rede                 |
| `users/`     | Não existe    | Usuários — perfil, autenticação, capabilities ativas|
| `historico/` | Não existe    | Projeção — histórico consolidado e imutável         |
| `dashboards/`| Não existe    | Métricas e relatórios                               |

---

## 3.1 `cadastro/` — Registry

**Papel:** Manter as entidades estruturais que servem de base
para todas as operações. É a memória institucional do sistema.

**Entidades que expõe:**

- `Loja`
- `Projeto`, `Subprojeto`
- `Equipamento`, `TipoEquipamento`, `Categoria`
- `Kit`, `ItemDeKit`

**Regras:**

- Alterações no cadastro não afetam chamados já criados
- Entidades vinculadas a chamados existentes não podem ser excluídas

**Consome:** nada

**É consumido por:** `chamados/`

**Fonte:** `web/cadastro/`

---

## 3.2 `chamados/` — Domínio Central

**Papel:** Dono do domínio Chamado.
Concentra o ciclo de vida, as regras de negócio, os gates operacionais,
o snapshot de itens e as evidências.

> Origem: ADR-058 e ADR-059 — separação formal do domínio Chamado do app `execucao/`.

**Entidades que expõe:**

- `Chamado` — entidade central, com tipo (ENVIO/RETORNO), status e itens
- `InstalacaoItem` — item individual do chamado (snapshot)
- `EvidenciaChamado` — documento PDF vinculado ao chamado
- `StatusConfiguracao` — configuração de status por tipo de chamado
- `ItemConfiguracaoLog` — log de alterações de configuração de item

**Responsabilidades:**

- Dono do STATUS do Chamado
- Dono das regras de transição de status (gates)
- Geração do snapshot de itens no momento da abertura
- Validação de integridade (retorno só de envio finalizado, etc.)

**Gates implementados aqui:**

| Gate | Transição | Regra |
|------|-----------|-------|
| Gate 1 | ABERTO → EM_EXECUCAO | Chamado tem itens + técnico com sessão ativa |
| Gate 2 | EM_EXECUCAO → AGUARDANDO_NF | Todos itens validados + C.EQUIPAMENTO preenchido |
| Gate 3 | AGUARDANDO_NF → AGUARDANDO_COLETA | NF preenchida + evidência obrigatória anexada |
| Gate 4 | AGUARDANDO_COLETA → FINALIZADO | Coleta confirmada |

**Consome:** `cadastro/`, `iam/`, `redes/`

**É consumido por:** `execucao/`, `historico/`, `dashboards/`

**Fonte:** `web/chamados/models.py`, `web/chamados/views.py`

---

## 3.3 `execucao/` — Operação em Campo

**Papel:** Gerenciar o trabalho ativo do técnico sobre um chamado.
Controla quem está trabalhando, quando começou, quando parou,
e apresenta a fila de chamados disponíveis.

**Entidades que expõe:**

- `ExecutionSession` — sessão ativa de um técnico em um chamado
- `ExecutionSessionLog` — auditoria de todas as sessões (quem, quando, como saiu)

**Responsabilidades:**

- Criar e encerrar sessões de execução
- Travar o chamado para outros técnicos enquanto há sessão ativa
- Expirar sessão após 1 hora de inatividade (sem perda de dados)
- Registrar no log quem trabalhou, quando e como saiu (manual ou expiração)
- Apresentar a fila operacional (chamados ABERTO+)

**Sobre a Fila Operacional:**

- A **ordenação** da fila (FIFO + prioridade) é responsabilidade de `execucao/`
- A **elegibilidade** dos chamados (status ABERTO+) é definida por `chamados/`
- `execucao/` consulta `chamados/` — nunca replica as regras

**Sobre Gates:**

- `execucao/` **chama** o gate definido em `chamados/`
- `execucao/` **registra** o resultado no log
- `execucao/` nunca **define** a regra do gate

**Consome:** `chamados/`, `iam/`

**É consumido por:** `historico/`, `dashboards/`

**Fonte:** `web/execucao/models.py`, `web/execucao/views.py`

---

## 3.4 `iam/` — Capabilities

**Papel:** Definir o que pode ser feito no sistema e validar
se um usuário tem permissão para fazer.

**O que expõe:**

- `has_capability(user, capability) → bool`
- `CapabilityRequiredMixin` — para proteger views
- Catálogo de capabilities disponíveis

**Princípios:**

- `iam/` não depende de `users/` — recebe um `user_id` e responde
- Negação por padrão — sem capability explícita, ação negada
- Backend é a fonte de verdade — UI nunca garante permissão
- Capabilities são independentes de tela

**Capabilities definidas:**

| Capability | O que permite |
|---|---|
| `chamado.abrir` | Abrir novo chamado |
| `chamado.editar_itens` | Editar itens após status ABERTO |
| `chamado.alterar_prioridade` | Alterar prioridade do chamado |
| `chamado.executar` | Assumir chamado da fila |
| `chamado.liberar_nf` | Avançar para AGUARDANDO_NF |
| `chamado.liberar_coleta` | Avançar para AGUARDANDO_COLETA |
| `chamado.finalizar` | Finalizar chamado |
| `retorno.gerar` | Gerar chamado de RETORNO |
| `cadastro.editar` | Criar e editar entidades do cadastro |
| `historico.visualizar` | Visualizar histórico de lojas e ativos |

**Consome:** nada

**É consumido por:** `users/`, `chamados/`, `execucao/`

**Fonte:** `web/iam/`

---

## 3.5 `redes/` — Validação de Rede

**Papel:** Validar configurações de IP e regras de rede por loja.
Domínio técnico isolado — independente da UI.

**O que expõe:**

- `validar_ip(ip) → bool`
- Regras de rede por loja

**Consome:** nada

**É consumido por:** `chamados/`

**Fonte:** `web/redes/services/validacao.py`

> Status: implementado parcialmente. Contrato em `docs/redes/validacao-ip-mvp.md`.

---

## 3.6 `users/` — Usuários *(não existe ainda)*

**Papel:** Gerenciar perfis de usuário, autenticação e
habilitação de capabilities para cada usuário.

**O que vai expor:**

- Usuário autenticado
- Perfil (nome, contato, dados operacionais)
- Capabilities habilitadas para o usuário

**Princípio:**

- `users/` habilita capabilities — não as define
- As capabilities são definidas em `iam/`
- Um usuário herda exatamente o que foi habilitado — sem permissão implícita

**Consome:** `iam/`

**É consumido por:** todos os apps que precisam de contexto do usuário autenticado

---

## 3.7 `historico/` — Histórico *(não existe ainda)*

**Papel:** Projetar e consolidar o histórico completo de operações,
garantindo rastreabilidade por Loja e por Ativo.

**O que vai expor:**

- Histórico por Loja — todos os chamados e eventos de uma loja
- Histórico por Ativo — linha do tempo completa de um equipamento
- Linha do tempo de um Chamado — transições, sessões, evidências

**Princípio fundamental:**

> `historico/` é um leitor — nunca escreve dados próprios.
> A imutabilidade é garantida na origem: `chamados/` e `execucao/`
> nunca permitem edição de eventos passados.
> `historico/` projeta o que já está protegido na fonte.

**Projeções obrigatórias:**

- Por Loja → agrupa chamados e eventos por loja
- Por Ativo → agrupa movimentações por equipamento rastreável

**Consome:** `chamados/`, `execucao/` (leitura apenas — nunca escreve)

**É consumido por:** `dashboards/`

---

## 3.8 `dashboards/` — Métricas *(não existe ainda)*

**Papel:** Agregar dados operacionais em métricas e relatórios.

**O que vai expor:**

- Métricas consolidadas por período, loja, projeto
- Relatórios operacionais

**Princípio:**

- Apenas leitura — nunca escreve nem altera dados
- Consome dados já consolidados pelo `historico/`

**Consome:** `historico/`, `chamados/`, `execucao/` (leitura apenas)

---

# 4. Fluxo de Dependências

```
                        ┌─────────────┐
                        │  cadastro/  │
                        │  (Registry) │
                        └──────┬──────┘
                               │ fornece entidades
                               ▼
          ┌────────┐    ┌─────────────┐    ┌─────────┐
          │  iam/  │───▶│  chamados/  │◀───│ redes/  │
          │        │    │  (Domínio)  │    │         │
          └────────┘    └──────┬──────┘    └─────────┘
               │               │ gates + chamado
               │               ▼
               │        ┌─────────────┐
               └───────▶│  execucao/  │
                        │  (Operação) │
                        └──────┬──────┘
                               │ eventos + logs
                               ▼
                        ┌─────────────┐
                        │ historico/  │
                        │  (Projeção) │
                        └──────┬──────┘
                               │ dados consolidados
                               ▼
                        ┌─────────────┐
                        │ dashboards/ │
                        │  (Leitura)  │
                        └─────────────┘

users/ consome iam/ e é consumido por todos os apps
       que precisam de contexto de usuário autenticado
```

**Regra de ouro:**
Nenhum app importa de um app que está acima dele nesse fluxo.

---

# 5. Ciclo de Vida do Chamado

```
EM_ABERTURA → ABERTO → EM_EXECUCAO → AGUARDANDO_NF → AGUARDANDO_COLETA → FINALIZADO
```

| Status | O que significa | Quem pode avançar |
|--------|-----------------|-------------------|
| `EM_ABERTURA` | Planejamento — geração de itens, ajustes | Técnico com `chamado.abrir` |
| `ABERTO` | Na fila — disponível para execução | — |
| `EM_EXECUCAO` | Técnico com sessão ativa trabalhando | Técnico com `chamado.executar` |
| `AGUARDANDO_NF` | Itens validados — aguardando nota fiscal | Técnico com `chamado.liberar_nf` |
| `AGUARDANDO_COLETA` | NF emitida — aguardando coleta física | Técnico com `chamado.liberar_coleta` |
| `FINALIZADO` | Estado terminal — imutável | Técnico com `chamado.finalizar` |

**Regras:**

- Chamados em `EM_ABERTURA` não aparecem na fila operacional
- `FINALIZADO` é terminal — nenhuma edição posterior
- Correções geram novo chamado — o original nunca é alterado
- O STATUS é propriedade de `chamados/` — `execucao/` registra quem avançou, não decide se pode

---

# 6. Snapshot Operacional

Quando um Kit é selecionado na abertura do Chamado,
`chamados/` gera um snapshot dos itens naquele momento.

**Regras do snapshot:**

- Itens rastreáveis (com ativo) → gerados individualmente, um por unidade
- Itens contáveis (sem ativo) → gerados como linha agregada com quantidade
- Alterações futuras no Kit não afetam o Chamado já criado

**Por que isso importa:**

O snapshot garante que o histórico reflita o que foi planejado
no momento da operação — não o que o kit é hoje.

**Fonte:** `web/chamados/models.py` — `gerar_itens_de_instalacao()`

---

# 7. Modelo em Camadas

```
┌─────────────────────────────────┐
│      Interfaces / Adapters      │
│   Web (Django Views/Templates)  │
└─────────────────┬───────────────┘
                  │
┌─────────────────▼───────────────┐
│          Application            │
│     Orquestração / Services     │
└─────────────────┬───────────────┘
                  │
┌─────────────────▼───────────────┐
│        Domain / Models          │
│  Regras puras, Gates, Entidades │
└─────────────────────────────────┘
```

**Diretrizes:**

- Models não concentram regra crítica de orquestração
- Views orquestram — não implementam regra de negócio
- Templates não implementam regra — apenas refletem estado
- Admin é ferramenta técnica — não é interface operacional

---

# 8. IAM — Como Corta o Sistema

O IAM é transversal — todo app que executa uma ação sensível
valida capability antes de prosseguir.

**Fluxo de uma ação protegida:**

```
Usuário solicita ação
        ↓
View verifica has_capability(user, capability)
        ↓
    NÃO TEM → HTTP 403, ação bloqueada
    TEM     → ação executada
        ↓
execucao/ registra no log (quem, quando, o quê)
```

**Onde o enforcement acontece:**

- Sempre no backend (views/services)
- Templates ocultam ações não permitidas — mas não garantem segurança
- Domínio é permission-agnostic — não conhece IAM

---

# 9. Stack e Ferramentas

**Framework:** Django

**Banco de dados:** PostgreSQL

**Frontend:** Tailwind via CDN (sem build)

**Testes Python:**
- `pytest` + `pytest-django`
- Localização: `tests/` e `web/*/tests/`
- Abordagem: TDD no domínio, regressão protegida

**Testes JavaScript:**
- `Jest` + `jsdom`
- Localização: `web/**/static/**/__tests__/`

**Ambiente:** Conda (Python 3.11)

---

# 10. Princípios Arquiteturais Ativos

- Apps de baixo fornecem — apps de cima consomem
- Registry não conhece Operation
- STATUS pertence ao domínio (`chamados/`)
- Gates são definidos em `chamados/`, chamados por `execucao/`
- Histórico é projeção — nunca fonte de escrita
- IAM é transversal — enforcement sempre no backend
- Chamados finalizados são imutáveis
- Correções geram novos chamados — nunca alteram o original
- Decisões técnicas registradas em ADR

---

# 11. Fora de Escopo Atual

- APIs públicas / integrações externas
- Multitenancy
- Mobile / offline-first
- Infra hardening avançado

---

Fonte:
- Estrutura real em `web/`
- Testes automatizados
- ADRs em `DECISIONS/` (especialmente ADR-058, ADR-059)
