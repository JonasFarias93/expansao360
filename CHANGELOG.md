# Changelog — EXPANSÃO360

Todas as mudanças relevantes do projeto são documentadas neste arquivo.
O versionamento segue o padrão **SemVer**.

---
## v0.4.1 - YYYY-MM-DD

### Changed
- Reset estrutural de migrations após split definitivo
- Remoção de duplicidade de templatetags
- Alinhamento de admin ao boundary de domínio

### Internal
- Boundary final: chamados = domínio / execucao = sessão/fila
- pytest 160 passed / 1 skipped
- manage.py check limpo
---

## [v0.4.0] — 2026-02-13

### Infra consolidada — Postgres como padrão

Este release consolida a base de infraestrutura do projeto, oficializando
**PostgreSQL como banco padrão** e garantindo reprodutibilidade via
docker-compose e CI.

---

### 🐘 Database

* PostgreSQL definido como banco oficial do projeto
* Configuração baseada em variáveis de ambiente (`DB_ENGINE`, `DB_*`)
* `.env.example` atualizado com contrato mínimo obrigatório
* docker-compose validado com healthcheck de Postgres

---

### ⚙️ Infra / Dev Experience

* Novo target `make compose-smoke`
  - Sobe Postgres
  - Aguarda healthcheck
  - Executa migrations
  - Executa pytest
* Padronização do fluxo local via `.env`
* Pipeline CI ajustado para usar Postgres de forma obrigatória

---

### 🧪 Quality Gate

* Teste PG-01: CI falha se banco não for Postgres
* Garantia de conexão real com vendor `postgresql`
* Pipeline validando instalação limpa + testes verdes

---

### 🔄 Changed

* Postgres deixa de ser “fase futura” e passa a ser padrão oficial
* Removido fallback implícito para SQLite no ambiente principal

---

### ⛔ Não incluso nesta versão

* Refatoração final de templatetags duplicadas (warnings W003)
* Split estrutural definitivo no banco (FKs → chamados.Chamado)

---

### Próximo passo

* Limpeza de duplicidade de templatetags
* Ajustes finais do split
* Preparação estrutural para v1.0.0

---

## [v0.3.6] — 2026-02-08

### Lookup de Loja por Código (Java)

Este release evolui o fluxo de abertura de Chamado, substituindo a seleção por
`<select>` massivo por um modelo baseado em lookup assíncrono.

### ✨ Added

* Endpoint de lookup de Loja por código ("Java")
* Novo input **"Loja (Java)"** no Abrir Chamado
* Feedback visual para sucesso/erro na validação

### 🔄 Changed

* Seleção de loja não depende mais de `<select>` gigante
* `<select>` mantido como fallback técnico (preenchido via JS)

### 🔐 Security / Integrity

* Validação server-side garante loja válida
* Proteção contra ID inválido/injetado

### 🧪 Tests

Cobertura para o endpoint de lookup:

* 200 — sucesso
* 404 — loja inexistente
* 400 — código inválido

Ajustes nos testes do form conforme novo contrato de validação.

---

## [v0.3.5] — 2026-02-07

### Execução operacional mais clara

Consolida a separação explícita entre setup e execução operacional, reforçando contratos arquiteturais sem quebra de compatibilidade.

### ✨ Execução

* Reativação do bloco de Evidências na execução
* Separação clara entre setup e execução operacional
* Novo componente `_card_operacional_chamado_full.html`

### 🎨 UI / UX

* Projetos com cor definida no cadastro
* Identificação visual por projeto na fila
* Header e cards mais informativos

### 🛠 Arquitetura

* Introdução de templatetags (`execucao_ui`)
* Refatoração incremental de templates

### 🧪 Qualidade

* Testes para views de execução
* Testes para template tags
* Ruff / Black / Pre-commit ativos

---

## [v0.3.3] — 2026-02-04

### Consolidação funcional (Cadastro + Execução + IAM)

### ✨ Destaques

* Registry, Operation e IAM estabilizados
* UI normalizada
* Cobertura de testes ampliada

### 🔄 Registry

* Ajustes em models, forms, views
* Melhorias em formsets
* Migração incluída

### 🔄 Execução

* Consolidação de regras operacionais
* Validações para fechamento de Chamados

### 🎨 UI

* Remoção de JS inline
* Normalização de templates

### 🧪 Testes

* Novos testes para AJAX e formsets
* Configuração pytest consolidada

---

## [v0.3.2] — 2026-02-03

### Tipos de Equipamento por Categoria

* `TipoEquipamento` vinculado à `Categoria`
* Ativar/inativar tipos sem apagar histórico
* `ItemKit.tipo` migra de texto livre para FK

### 🎨 UI

* Edição inline de tipos (formset)

### 🧪 Testes

* Cobertura de unicidade
* Ajustes por migração de schema

---

## [v0.3.1] — 2026-02-02

### Importação de Lojas (CSV/XLSX)

* Import idempotente
* Normalização automática (UF, logomarca)
* UX aprimorada na listagem

### 🧪 Testes

* Cobertura para normalização e idempotência

---

## [v0.3.0] — 2026-01-30

### Fluxo Inverso e Consolidação Operacional

* Suporte a fluxo direto e inverso
* Regras completas de finalização
* Evidências associadas
* IAM mínimo por capability
* Testes cobrindo regras críticas

---

## [v0.2.0] — 2026-01-22

### Web v1 (Registry + Chamado)

* Core independente de framework
* CLI funcional
* Cadastro via Web
* Chamado com protocolo automático
* Snapshot operacional de itens
* Workflow básico
* UI inicial (histórico/detalhe)

---

Última revisão: 2026-02-11
Fonte: Tags Git + código versionado
