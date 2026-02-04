# EXPANSÃO360

Plataforma para gestão de expansão, padronização e **operação de campo**,
com separação rigorosa entre **Cadastro Mestre (Registry)** e **Execução Operacional (Operation)**,
garantindo **rastreabilidade, histórico e governança de ponta a ponta**.

---

## Objetivo

O EXPANSÃO360 tem como objetivo estruturar e padronizar a expansão de operações físicas,
assegurando que o que foi definido no planejamento seja corretamente executado em campo,
com evidências, histórico auditável e regras claras de operação.

O sistema foi concebido para evitar:

* perda de histórico
* edições destrutivas de execução
* inconsistência entre planejamento e operação
* falta de governança em fluxos de retorno e exceção

O foco do sistema é **rastreabilidade, consistência e evolução segura** dos processos.

🚀 **Release atual:** `v0.3.1 — Importação de Lojas & UX de Cadastro`
🚧 **Sprint atual:** Sprint 4 — UX Operacional & Views

---

## O que já está consolidado

* Arquitetura em camadas (Domain / Application / Infrastructure)
* Core de domínio independente de framework
* Regras de negócio explícitas e testadas (TDD)
* Execução operacional baseada em **Chamados**
* Suporte a **fluxo direto (Matriz → Loja)** e **fluxo inverso (Loja → Matriz)**
* Registro de **Itens de Execução** (snapshot operacional)
* Registro de **Evidências** (NF, Carta de Conteúdo, exceções)
* IAM mínimo baseado em **capabilities**
* Camada Web (Django) funcional
* CLI **experimental** como interface de referência do core
* Testes automatizados e hooks de qualidade (ruff, black, pre-commit)

---

## Conceito Central

O sistema é baseado em uma separação clara e intencional de responsabilidades:

### Registry (Cadastro Mestre)

Define **o que existe** e **como deve ser padronizado**.

Exemplos:

* Lojas
* Projetos / Subprojetos
* Equipamentos
* Kits e seus itens

**Características**

* Fonte da verdade
* Alterações controladas
* Governança e estabilidade
* Não registra execução

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
* Suporte a auditoria
* Não altera o cadastro mestre

---

## Conceito-chave: Chamado

O **Chamado** é a unidade central de execução operacional.

* Representa um **evento real**
* Nunca é editado de forma destrutiva após finalização
* Correções e retornos geram **novos Chamados**
* Pode representar:

  * Envio (Matriz → Loja)
  * Retorno (Loja → Matriz)

O Chamado atua como a **ponte controlada** entre planejamento (Registry) e execução (Operation).

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
> A CLI pode não refletir todas as regras, fluxos e validações do sistema Web (Django).
> O produto principal e a fonte da verdade operacional/administrativa é a **camada Web**.

Use a CLI quando for útil para:

* validações rápidas do core
* demonstrações e experimentos locais
* testes manuais fora do contexto Web

```bash
python -m expansao360 --help
python -m expansao360 location --help
python -m expansao360 mount --help
```

### Nota sobre futuras integrações (APIs)

Integrações externas (ex.: transportadoras, sistemas parceiros) devem ser implementadas
como **adapters (APIs/serviços)** consumindo os mesmos **use cases** do core.

A existência do CLI **não é pré-requisito** para APIs.

---

## Web (Django)

A camada Web atua como **adapter**, oferecendo:

* Cadastro administrativo (Registry)
* Execução operacional via Chamados
* Abertura de Chamados a partir de Kits
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
* `REQUIREMENTS.md` — requisitos
* `GLOSSARIO.md` — terminologia oficial
* `STATUS.md` — status por sprint/release

---

## Princípios do Projeto

* Registro histórico é sagrado
* Nenhuma execução é apagada
* Correções geram novos eventos
* Planejamento e execução não se misturam
* Governança acima de conveniência
