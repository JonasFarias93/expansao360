# STATUS — EXPANSÃO360

Este documento apresenta o estado atual do projeto com base nos releases publicados
e no comportamento real implementado no código.

Fonte de verdade:

* Tags de release (Git)
* CHANGELOG.md
* Código em `web/`

---

# 📦 Release Atual

## v0.6.0

Data: 31/05/2026

### Resumo

Sprint operacional completa com correções críticas, novos apps de domínio e melhorias de UX.

### Bug Fixes

* Chamados sumindo da fila após configuração de itens (`EM_CONFIGURACAO` removido do recalcular_status)
* Snapshot operacional não propagava `deve_configurar` do kit
* Erro 403 (CSRF) ao enviar evidências

### Features

* `seed_dev` — comando para popular dados de desenvolvimento
* Cancelamento de chamado com motivo obrigatório e auditoria
* UX operacional: editar IP, salvar IP, TAB behavior para leitura de código de barras
* Resumo de equipamentos na sidebar do chamado

### Novos Apps

* `historico/` — snapshot imutável, timeline de ativos, busca auditável
* `users/` — identidade operacional, perfil, status, gerenciamento de capabilities

### Qualidade

* 189 testes passando
* TDD respeitado em todas as features críticas

---

# 🟡 Sprint Atual

## Sprint 5 — Domínio & Governança

Status: Em andamento

### Objetivo

Evoluir o domínio com foco em:

* Documentação atualizada e precisa
* Governança do fluxo operacional
* Gate de finalização completo
* Estabilização dos novos apps

---

## Entregas Consolidadas (Sprint 5)

### Documentação
* CHANGELOG atualizado com v0.6.0
* STATUS atualizado
* ARCHITECTURE pendente de atualização

### Domínio
* App `historico/` — snapshot + timeline + busca
* App `users/` — identidade operacional + capabilities UI
* Cancelamento de chamado com auditoria

### Qualidade
* 189 testes passando
* Regressão da fila operacional coberta por testes

---

# ✅ Sprint 4 — UX Operacional & Views

Releases: v0.3.1 → v0.5.0
Status: Concluída

### Entregas

* Importação idempotente de Lojas (CSV/XLSX)
* Separação explícita entre `EM_ABERTURA` e `ABERTO`
* Evidências na execução
* Fila operacional consolidada
* PostgreSQL como banco padrão
* Split definitivo de domínios
* State Manager centralizado

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

* Gate de finalização completo (`pode_finalizar` ainda hardcoded como `False`)
* Atualizar `ARCHITECTURE.md` com apps `historico/` e `users/`
* Teste manual ponta a ponta do fluxo completo (abertura → execução → finalização)
* Validar `MT-06` — teste manual da fila operacional pós-fix
* Fechar issue `#131` após validação manual

---

# 📚 Leitura Relacionada

* `README.md`
* `ARCHITECTURE.md`
* `CHANGELOG.md`
* `DECISIONS/`

---

Última revisão: 2026-05-31
Fonte: Tags Git + CHANGELOG.md + código real em `web/`