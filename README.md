# EXPANSÃO360

Plataforma para gestão de expansão, padronização e **operação de campo**,
com separação rigorosa entre **Cadastro Mestre (Registry)** e **Execução Operacional (Operation)**,
garantindo **rastreabilidade, histórico e governança de ponta a ponta**.

---

## Objetivo

O **EXPANSÃO360** tem como objetivo estruturar e padronizar a expansão de operações físicas,
assegurando que o que foi definido no planejamento seja corretamente executado em campo,
com evidências, histórico auditável e regras claras de operação.

O sistema foi concebido para evitar:

* perda de histórico
* edições destrutivas de execução
* inconsistência entre planejamento e operação
* falta de governança em fluxos de retorno e exceção

O foco do sistema é **rastreabilidade, consistência e evolução segura** dos processos.

🚀 **Release atual:** `v0.3.5 — Execução operacional mais clara`
🚧 **Sprint atual:** Sprint 4 — UX Operacional & Views

---

## ✨ O que mudou na versão atual

### Execução

* Separação explícita entre **setup (planejamento)** e **execução operacional**
* Reativação do bloco de **Evidências** na tela de execução
* Novo componente `_card_operacional_chamado_full.html`

### UI / UX

* Projetos agora possuem **cor definida no cadastro**
* Fila operacional com **identificação visual por projeto**
* Header e cards da fila mais informativos

### Arquitetura

* Introdução de **templatetags de UI** (`execucao_ui`)
* Contratos de templates respeitados
* Refatoração incremental sem quebra de compatibilidade

### Qualidade

* Testes adicionados para:

  * Views de execução
  * Template tags de UI
* Ruff / Black / Pre-commit ativos

> 🔖 Esta versão consolida a transição do fluxo de execução e prepara o terreno
> para evolução visual e operacional da fila.

---

## O que já está consolidado

* Arquitetura em camadas (Domain / Application / Infrastructure)
* Core de domínio independente de framework
* Regras de negócio explícitas e testadas (TDD)
* Execução operacional baseada em **Chamados**
* Suporte a **fluxo direto (Matriz → Loja)** e **fluxo inverso (Loja → Matriz)**
* Registro de **Itens de Execução** como *snapshot operacional*
* Registro de **Evidências** (NF, Carta de Conteúdo, exceções)
* IAM mínimo baseado em **capabilities**
* Camada Web (Django) atuando como **adapter**
* CLI **experimental** como interface de referência do core
* Testes automatizados e hooks de qualidade (ruff, black, pre-commit)

---

## Conceito Central

O sistema é baseado em uma separação **clara, explícita e intencional** de responsabilidades,
que orienta toda a modelagem do domínio e evita acoplamentos indevidos.

### Registry (Cadastro Mestre)

Define **o que existe** e **como deve ser padronizado**.

Exemplos:

* Lojas
* Projetos / Subprojetos
* Equipamentos
* Categorias e Tipos de Equipamento
* Kits e seus itens

**Características**

* Fonte da verdade
* Alterações controladas e governadas
* Estável ao longo do tempo
* Não registra execução
* Não depende do domínio operacional

---

### Operation (Execução de Campo)

Registra **o que foi executado**, **quando**, **por quem** e **com quais evidências**.

Exemplos:

* Chamados
* Itens de Execução
* Evidências (anexos)
* Fluxos de retorno e exceção

**Características**

* Histórico imutável
* Rastreabilidade completa
* Suporte a auditoria e contabilidade
* Não altera o cadastro mestre

---

## Conceito-chave: Chamado

O **Chamado** é a unidade central de execução operacional.

* Representa um **evento real** no mundo físico
* Possui ciclo de vida explícito
* Nunca é editado de forma destrutiva após finalização
* Correções e retornos geram **novos Chamados**
* Pode representar:

  * Envio (Matriz → Loja)
  * Retorno (Loja → Matriz)

O Chamado atua como a **ponte controlada** entre planejamento (Registry) e execução (Operation).

---

## Ciclo de Vida do Chamado

O ciclo de vida do Chamado separa explicitamente **planejamento** de **execução**:

1. **EM_ABERTURA**

   * Criação do chamado
   * Geração dos itens de execução
   * Decisão de configuração (ex.: necessidade de IP)
   * Planejamento técnico

2. **ABERTO**

   * Chamado promovido explicitamente após salvar o setup
   * Entra na fila operacional

3. **EM_EXECUCAO / AGUARDANDO_***

   * Execução em campo
   * Bipagem, conferências e coleta de evidências

4. **FINALIZADO**

   * Estado terminal
   * Histórico preservado

Chamados em **EM_ABERTURA** **nunca aparecem** na fila operacional.

---

## Gates Operacionais

O avanço do Chamado é protegido por regras explícitas:

* Liberação de NF exige:

  * Todos os itens rastreáveis bipados
  * Todos os itens contáveis confirmados

* Finalização do Chamado exige:

  * NF registrada (quando aplicável)
  * Confirmação de coleta
  * Evidências mínimas conforme o fluxo

Essas regras garantem consistência operacional e auditabilidade.

---

## Chamado Externo

Chamados podem ser associados a sistemas externos através dos campos:

* `ticket_externo_sistema`
* `ticket_externo_id`

Na UI, o Chamado Externo é exibido no formato:

```
<sistema>: <id>
```

O campo `ticket_externo_id` é **globalmente único** quando preenchido,
garantindo buscas e auditoria sem ambiguidade.

---

## Como rodar o projeto localmente

### Pré-requisitos

* Git
* Conda (Miniforge / Miniconda)
* GNU Make

### Setup do ambiente

```bash
conda env create -f environment.yml
conda activate expansao360
```

---

## CLI (experimental / interface de referência)

A CLI existe como **interface de referência** para demonstrar o core em camadas
(Domain / Application / Infrastructure) funcionando **sem a camada Web**.

> **Status:** experimental
>
> A CLI pode não refletir todos os fluxos e validações do sistema Web.
> A **camada Web (Django)** é o produto principal e a fonte da verdade operacional.

Casos de uso da CLI:

* validações rápidas do core
* demonstrações e experimentos locais
* testes manuais fora do contexto Web

```bash
python -m expansao360 --help
python -m expansao360 location --help
python -m expansao360 mount --help
```

### Nota sobre futuras integrações (APIs)

Integrações externas devem ser implementadas como **adapters (APIs/serviços)**,
consumindo os mesmos **use cases** do core.

A existência da CLI **não é pré-requisito** para APIs.

---

## Web (Django)

A camada Web atua como **adapter**, oferecendo:

* Cadastro administrativo (Registry)
* Execução operacional via Chamados
* Abertura de Chamados a partir de Kits
* Separação clara entre setup e execução
* Suporte a fluxo direto e inverso
* Registro e visualização de evidências
* IAM por capabilities
* Interface administrativa (Django Admin)

### Comandos principais

```bash
python web/manage.py migrate
python web/manage.py runserver
python web/manage.py test
```

---

## Documentação do Projeto

* `ARCHITECTURE.md` — visão arquitetural
* `DECISIONS.md` — ADRs e decisões técnicas
* `REQUIREMENTS.md` — requisitos funcionais e não funcionais
* `GLOSSARIO.md` — terminologia oficial do domínio
* `STATUS.md` — status por sprint e release

---

## Princípios do Projeto

* Registro histórico é sagrado
* Nenhuma execução é apagada
* Correções geram novos eventos
* Planejamento e execução não se misturam
* Governança acima de conveniência
