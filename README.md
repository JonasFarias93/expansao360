# EXPANSÃO360

Plataforma para gestão de expansão, padronização e **operação de campo**,
com separação rigorosa entre **Cadastro Mestre (Registry)** e **Execução Operacional (Operation)**,
garantindo **rastreabilidade, histórico e governança de ponta a ponta**.

---

## 🚀 Release Atual

**v0.3.6 — Lookup de Loja por Código (Java)**
Veja detalhes em `CHANGELOG.md`.

Sprint atual: **Sprint 4 — UX Operacional & Views**
Status detalhado em `STATUS.md`.

---

# 🎯 Objetivo

Estruturar e padronizar a expansão de operações físicas,
assegurando que o planejamento (Registry) seja executado corretamente em campo (Operation),
com evidências, histórico auditável e regras explícitas.

O sistema evita:

* Perda de histórico
* Edições destrutivas de execução
* Inconsistência entre planejamento e operação
* Falta de governança em fluxos de retorno e exceção

---

# 🧱 Conceito Central

## Registry (Cadastro Mestre)

Define **o que existe** e **como deve ser padronizado**.

Exemplos:

* Lojas
* Projetos / Subprojetos
* Equipamentos
* Categorias e Tipos de Equipamento
* Kits

Características:

* Fonte da verdade
* Alterações impactam apenas execuções futuras
* Não registra execução

---

## Operation (Execução)

Registra **o que foi executado**, **quando**, **por quem** e **com quais evidências**.

Exemplos:

* Chamados
* Itens de Execução (snapshot)
* Evidências
* Fluxos direto e inverso

Características:

* Histórico imutável
* Rastreabilidade completa
* Não altera cadastro mestre

---

# 📌 Conceito-chave: Chamado

Unidade central da execução operacional.

* Representa evento real
* Possui ciclo de vida explícito
* Finalizado = imutável
* Correções geram novo Chamado

Estados principais:

1. `EM_ABERTURA` (setup)
2. `ABERTO` (entra na fila)
3. `EM_EXECUCAO / AGUARDANDO_*`
4. `FINALIZADO`

Chamados em `EM_ABERTURA` **não aparecem na fila operacional**.

---

# 🛡️ Gates Operacionais

Avanço de status protegido por regras:

* Liberação de NF exige itens rastreáveis bipados e contáveis confirmados
* Finalização exige NF (quando aplicável) + coleta + evidências mínimas

Regras implementadas no backend e cobertas por testes.

---

# 🖥️ Como Rodar o Projeto

## Pré-requisitos

* Git
* Conda (Miniforge / Miniconda)
* Node (para testes JS)

---

## Setup do Ambiente

```bash
conda env create -f environment.yml
conda activate expansao360
```

---

## Banco e Servidor

```bash
python web/manage.py migrate
python web/manage.py runserver
```

---

# 🧪 Como Rodar Testes

## Python (pytest)

```bash
pytest
```

ou

```bash
python web/manage.py test
```

## JavaScript (Jest)

```bash
npm install
npm run test:js
```

Testes JS ficam em:

```
web/cadastro/static/cadastro/js/__tests__/
```

---

# 🧩 Web (Django)

Apps principais:

* `cadastro` → Registry
* `execucao` → Operation
* `iam` → Capabilities
* `redes` → Regras de validação de IP (MVP)

A Web atua como **adapter**, não como domínio.

---

# 📚 Documentação

* `ARCHITECTURE.md` → visão arquitetural
* `REQUIREMENTS.md` → requisitos funcionais e não funcionais
* `SECURITY.md` → diretrizes de segurança
* `GLOSSARIO.md` → terminologia oficial
* `STATUS.md` → visão executiva por sprint
* `CHANGELOG.md` → histórico de releases

Documentação operacional adicional em:

```
docs/
```

Decisões arquiteturais (ADRs) em:

```
DECISIONS/
```

---

# 🧠 Princípios

* Histórico é sagrado
* Planejamento ≠ Execução
* Correções geram novos eventos
* Regras explícitas > comportamento implícito
* Evolução incremental e rastreável

---

Última revisão: 2026-02-11
Fonte: Código real em `web/` + CHANGELOG + STATUS
