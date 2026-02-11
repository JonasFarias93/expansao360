# Auditoria de Testes — Expansão360

## Contexto (as-is)

* Suíte atual: ~158 testes, ~10s, 100% verde (1 skipped).
* Estrutura predominante: **Web/Django (apps cadastro, execucao, iam)**.
* Core framework-agnostic ainda existe, mas não é o centro do produto.
* Objetivo desta auditoria: manter alto valor, marcar fragilidades e registrar riscos reais.

Fonte:
- Execução: `pytest -q`
- Diretórios: `web/*/tests/`

---

## Legenda de status

* ✅ KEEP — alto valor
* ⚠️ REFATORAR (futuro)
* ❌ REMOVER

---

# 1) Core (Framework-agnostic)

⚠️ Status: secundário no produto atual.

Se CLI/core ainda estiver ativo:
- manter smoke mínimo
- evitar duplicação com camada Web

Se não estiver mais ativo:
- considerar mover para `legacy/`
- ou reduzir para testes contratuais mínimos

(Decisão futura pode exigir ADR.)

---

# 2) Web / Django (Camada Principal)

## App `cadastro`

### test_models.py
- protege constraints + geração automática
- nível: integration (ORM)
- status: ✅ KEEP

### test_services_import_lojas.py
- protege idempotência + atualização seletiva
- status: ✅ KEEP (alto valor)

### test_forms.py
- protege estrutura superficial
- risco coberto: baixo
- status: ⚠️ avaliar substituição por validações reais

---

## App `execucao` (núcleo operacional)

### test_models_chamado_basics.py
- protocolo automático
- unicidade ServiceNow
- status: ✅ KEEP

### test_models_chamado_finalizar.py
- pré-condições de finalização
- status: ✅ KEEP (altíssimo valor)

### test_models_chamado_itens.py
- geração de itens do kit
- status: ✅ KEEP

### test_models_evidencias.py
- vínculo evidência ↔ chamado
- status: ✅ KEEP

### test_views_flows.py
- fluxos + permissões
- status: ✅ KEEP

### test_views_chamado_execucao_get.py
- garante template correto para execução
- status: ✅ KEEP

### test_views_fila_operacional.py
- garante contagem e filtro por prioridade
- status: ✅ KEEP

---

## App `iam`

### test_models.py
- unicidade capability
- status: ✅ KEEP

---

# 3) Riscos reais ainda não cobertos

- [ ] Bloqueio de finalizar sem evidência obrigatória
- [ ] Teste explícito de 403 quando usuário sem capability acessa execução
- [ ] Teste de concorrência real (duas sessões simultâneas)
- [ ] Teste de promoção automática ABERTO → EM_EXECUCAO

---

# 4) Estratégia futura

Criar ADR apenas se:

- Descontinuar definitivamente o CLI
- Introduzir política oficial para testes de template HTML
- Adotar factories globais (factory_boy)

---

## Testes JavaScript

- Local: `web/cadastro/static/cadastro/js/__tests__/`
- Runner: Jest
- Comandos:
  - `npm run test:js`
  - `make test` (Python + JS)

---

Última revisão: 2026-02-11  
Fonte: `pytest -q`, `web/*/tests/`