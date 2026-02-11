# Auditoria de Testes — Expansão360 (2026-02-03)

## Contexto

* Suíte atual: **49 testes**, ~**0.9s**, **100% verde**.
* Estrutura clara entre **core agnóstico** (`tests/`) e **camada Web/Django** (`web/<app>/tests/`).
* Objetivo desta auditoria: **manter o que tem alto valor**, **marcar fragilidades** e **registrar ações futuras**, sem refatorar agora.

---

## Legenda de status

* ✅ **KEEP** — teste de alto valor, deve ser mantido
* ⚠️ **REFATORAR (futuro)** — conteúdo válido, mas com melhoria estrutural ou duplicidade
* ❌ **REMOVIDO** — sem valor real ou arquivo vazio

---

## 1) Core (framework-agnostic)

### CLI

* `tests/cli/test_smoke.py`

  * protege: fluxo end-to-end do CLI (estado em arquivo)
  * risco coberto: CLI quebrado / regressão grosseira
  * nível: smoke / flow
  * status: ✅ KEEP
  * nota futura: se CLI crescer, manter **apenas um** smoke mínimo

* `tests/cli/test_errors.py`

  * protege: contrato de erro do CLI (exit code + mensagem)
  * risco coberto: operação inválida passando como sucesso
  * nível: flow
  * status: ✅ KEEP

---

### Domain (contratos / value objects)

* `tests/domain/contracts/test_domain_contract.py`

  * protege: invariantes de `OperationMount`
  * risco coberto: operação sem rastreabilidade
  * nível: unit
  * status: ✅ KEEP

* `tests/domain/value_objects/test_value_objects.py`

  * protege: invariantes e normalização de `LocationId` e `ActorId`
  * risco coberto: ids inválidos / dados sujos no core
  * nível: unit
  * status: ✅ KEEP

* `tests/domain/value_objects/test_mount_status.py`

  * protege: contrato do enum `MountStatus` (`label`, `can_execute`)
  * risco coberto: regressão em status/fluxos
  * nível: unit
  * status: ✅ KEEP

---

### Usecases — Operation

* `tests/usecases/operation/test_register_mount.py`

  * protege: normalização de input + criação da operação
  * risco coberto: operação inválida criada
  * nível: unit/usecase
  * status: ✅ KEEP

* `tests/usecases/operation/test_register_mount_requires_location.py`

  * protege: pré-condição crítica (Location deve existir)
  * risco coberto: operação sem vínculo com registry
  * nível: unit/usecase
  * status: ✅ KEEP (altíssimo valor)

* `tests/usecases/operation/test_register_mount_with_repo.py`

  * protege: persistência da operação via repo in-memory
  * risco coberto: **já coberto** por teste acima
  * nível: unit/usecase
  * status: ⚠️ REFATORAR (duplicado)
  * ação futura: consolidar/remover

---

### Usecases — Registry

* `tests/usecases/registry/test_register_location.py`

  * protege: criação e persistência de Location via usecase
  * risco coberto: cadastro mestre quebrado
  * nível: unit/usecase
  * status: ✅ KEEP

* `tests/usecases/registry/test_registry_location.py`

  * protege: invariantes da entidade `Location`
  * risco coberto: entidade inválida no core
  * nível real: unit (domain)
  * status: ⚠️ REFATORAR
  * ação futura: mover para `tests/domain/registry/`

---

## 2) Web / Django

### App `cadastro`

* `web/cadastro/tests/test_models.py`

  * protege: constraints, normalizações e geração automática
  * risco coberto: duplicidade e dados inválidos
  * nível: integration (ORM)
  * status: ✅ KEEP

* `web/cadastro/tests/test_services_import_lojas.py`

  * protege: normalização + idempotência + atualização seletiva + command
  * risco coberto: import inconsistente / duplicidade
  * nível: integration (ORM + service)
  * status: ✅ KEEP (excelente cobertura)

* `web/cadastro/tests/test_forms.py`

  * protege: existência básica de campos/labels
  * risco coberto: muito baixo
  * nível: integration (forms)
  * status: ⚠️ FRÁGIL / baixo valor
  * ação futura: remover ou substituir por teste de validação real

* `web/cadastro/tests/test_views.py`

  * status: ❌ REMOVIDO
  * motivo: arquivo vazio / sem cobertura real

---

### App `execucao`

* `web/execucao/tests/_base.py`

  * protege: infraestrutura de testes (setup + auth + capabilities)
  * risco coberto: repetição e setups inconsistentes
  * nível: infra de teste
  * status: ✅ KEEP

* `web/execucao/tests/test_models_chamado_basics.py`

  * protege: protocolo automático + unicidade ServiceNow + bloqueio sem itens
  * risco coberto: rastreabilidade e integridade inicial
  * nível: integration
  * status: ✅ KEEP

* `web/execucao/tests/test_models_chamado_finalizar.py`

  * protege: pré-condições de finalização + imutabilidade
  * risco coberto: fechamento indevido
  * nível: integration
  * status: ✅ KEEP (altíssimo valor)

* `web/execucao/tests/test_models_chamado_itens.py`

  * protege: geração de itens do kit + regra ativo/confirmado
  * risco coberto: inconsistência registry → operation
  * nível: integration
  * status: ✅ KEEP

* `web/execucao/tests/test_models_evidencias.py`

  * protege: vínculo evidência ↔ chamado + upload
  * risco coberto: rastreabilidade quebrada
  * nível: integration
  * status: ✅ KEEP

* `web/execucao/tests/test_views_flows.py`

  * protege: fluxos via POST + permissões
  * risco coberto: endpoints quebrados
  * nível: flow/integration
  * status: ✅ KEEP

---

### App `iam`

* `web/iam/tests/test_models.py`

  * protege: unicidade user↔capability
  * risco coberto: duplicidade de permissões
  * nível: integration
  * status: ✅ KEEP

---

## 3) Ações futuras registradas (não fazer agora)

### Refactors pontuais

* [ ] Consolidar/remover `test_register_mount_with_repo.py`
* [ ] Mover `test_registry_location.py` para camada de domain
* [ ] Substituir/remover `test_forms.py` (labels)

### Backlog de testes (riscos reais)

* [ ] IAM: usuário sem capability → acesso negado
* [ ] Execução: finalizar chamado sem evidência obrigatória
* [ ] Import lojas: linha inválida (UF/código vazio)
* [ ] Cadastro: unicidade de `Loja.codigo` (se aplicável)

---

## 4) ADR?

Nenhuma mudança estrutural foi feita.
Criar ADR apenas se decidir:

* política oficial sobre testes de template/HTML
* rebaixar/remover definitivamente o CLI
* introduzir nova estratégia de testes (ex.: factories globais)

---

**Status geral:** suíte saudável, rápida, com pouquíssima dívida técnica em testes.

---

## Testes JavaScript (Frontend)

- Local: `web/cadastro/static/cadastro/js/__tests__/`
- Runner: Jest (jsdom)
- Comandos:
  - `npm run test:js`
  - `npm run test:js:watch`
  - `make test` (roda Python + JS)
