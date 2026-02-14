# STATUS — EXPANSÃO360

Este documento apresenta o estado atual do projeto com base nos releases publicados
e no comportamento real implementado no código.

Fonte de verdade:

* Tags de release (Git)
* CHANGELOG.md
* Código em `web/`

---

# 📦 Release Atual

## v0.3.6

Data: 08/02/2026
Tag: `0fb9f9d`

### Added

* Lookup API de loja por código (Java) para uso no fluxo de chamados
* Novo input "Loja (Java)" no Abrir Chamado com validação e feedback ao usuário

### Changed

* Seleção de loja no Abrir Chamado deixa de depender de `<select>` grande
* `<select>` mantido apenas como fallback técnico (preenchido via JS)

### Security / Integrity

* Validação server-side impede criação de chamado sem loja válida
* Proteção contra ID inválido ou injetado no backend

### Tests

Cobertura para o endpoint de lookup de loja:

* 200 (sucesso)
* 404 (loja inexistente)
* 400 (código inválido)

Ajustes nos testes do form conforme novo contrato de validação.

---

# 🟡 Sprint Atual

## Sprint 4 — UX Operacional & Views

Status: Em andamento
Releases associados: v0.3.1 → v0.3.6

### Objetivo

Evoluir a experiência operacional sem alterar o core de domínio.

Foco em:

* Clareza visual
* Redução de atrito
* Contratos de templates
* Feedback operacional

---

## Entregas Consolidadas (Sprint 4)

### Registry

* Importação idempotente de Lojas (CSV/XLSX)
* Normalização automática de campos críticos
* UX aprimorada na listagem de Lojas

### Execução

* Separação explícita entre `EM_ABERTURA` e `ABERTO`
* Reativação de evidências na execução
* Consolidação da fila operacional

### UI

* Projetos com cor definida
* Cards-resumo na fila operacional
* Preview inline de Chamado
* Componente `_card_operacional_chamado_full.html`

### Arquitetura

* Introdução de templatetags de UI (`execucao_ui`)
* Refatoração incremental de templates

### Qualidade

* Testes para views de execução
* Testes para templatetags
* Stack ativa: Ruff, Black, Pre-commit
* Testes JS (Jest + jsdom)

---

# ✅ Sprint 3 — Core Operacional

Release: v0.3.0
Status: Concluída

### Entregas

* Fluxo direto e inverso (ENVIO / RETORNO)
* Regras completas de finalização
* Evidências vinculadas ao Chamado
* IAM mínimo por capability
* Testes cobrindo regras críticas

---

# ✅ Sprint 2 — Base Estrutural

Status: Concluída

### Entregas

* Core independente de framework
* CLI funcional (Registry e Operation)
* Camada Web inicial (Django)
* Workflow básico de Chamado
* Testes automatizados estruturais

---

# 📌 Próximos Passos Técnicos

* Refinamento visual da fila
* Ajuste de microcopy
* Avaliação de filtros avançados

---

# 📚 Leitura Relacionada

* `README.md`
* `ARCHITECTURE.md`
* `CHANGELOG.md`
* `DECISIONS/`

---

Última revisão: 2026-02-11
Fonte: Tags Git + CHANGELOG.md + código real em `web/`
