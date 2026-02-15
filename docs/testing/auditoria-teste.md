# Auditoria de Testes — Expansão360

---

# 🎯 Objetivo da Auditoria

Esta auditoria tem como finalidade:

1. Garantir que cada teste possua **contrato claro e verificável**.
2. Organizar a suíte por **camadas arquiteturais e domínios**.
3. Padronizar **nomenclatura semântica**.
4. Criar rastreabilidade para refactor controlado.
5. Elevar a confiabilidade da suíte antes de futuras evoluções.

⚠️ Importante:
Nenhum teste foi auditado ainda.
Todos são considerados LEGACY até revisão formal.

---

# 📊 Estado Atual da Suíte

Total coletado: **162 testes**
Status atual:

* 🟡 LEGACY: 162
* 🟢 KEEP: 0
* 🔵 REFATORAR: 0
* 🔴 REMOVER: 0

Fonte:

* `pytest --collect-only -q`
* Diretórios: `tests/` e `web/*/tests/`

---

# 🏷️ Legenda Oficial de Status

## 🟡 LEGACY

Teste ainda não auditado segundo o novo padrão.

## 🟢 KEEP

Teste auditado e aprovado segundo critérios:

✓ Nome semântico
✓ Arquivo correto por camada
✓ Uso adequado de fixtures
✓ Assert de efeito real
✓ Falha pelo motivo certo

## 🔵 REFATORAR

Teste válido, mas precisa:

* Renomeação
* Reorganização de arquivo
* Melhorar asserts
* Reduzir fragilidade
* Ajustar fixtures

## 🔴 REMOVER

Teste duplicado, frágil ou de baixo valor.
(Remover apenas após validação formal.)

---

# 🏗️ Organização Oficial dos Testes

## 1️⃣ Core (Framework-agnostic)

Local: `tests/`

* `tests/domain/` → Value Objects e contratos puros
* `tests/usecases/` → Casos de uso
* `tests/cli/` → CLI e smoke

Regra:
Core não pode depender de Django.

---

## 2️⃣ Web / Django

Local: `web/<app>/tests/`

### Modelos

`test_models_*.py`

Protege:

* Invariantes
* Constraints
* Regras internas

### Serviços

`test_services_*.py`

Protege:

* Regras de domínio
* Transições de estado
* Idempotência

### Views

`test_views_*.py`

Protege:

* Permissões
* Fluxo HTTP
* Redirecionamentos
* Efeitos persistidos

### Forms

`test_forms_*.py`

Protege:

* Validação real
* Regras de negócio (não label superficial)

### UI / TemplateTags

`test_ui_*.py`

Protege:

* Contratos mínimos de renderização
* `data-*` críticos

---

## 3️⃣ JavaScript (Jest)

Local:

* `web/<app>/static/<app>/js/__tests__/`

Protege:

* Contratos DOM
* Estado determinístico
* Idempotência

Evitar:

* Snapshot gigante
* Teste de estrutura irrelevante

---

# 🧠 Padrão de Nomenclatura

## Arquivos

Deve indicar contrato específico.

✅ Correto:

* `test_models_user_capability_unique.py`
* `test_services_import_lojas_idempotencia.py`
* `test_views_salvar_execucao_permissoes.py`

⚠️ Temporário (LEGACY):

* `test_models.py`
* `test_forms.py`
* `test_views_flows.py`

---

## Funções de Teste

Formato preferido:

`test_quando_<contexto>_entao_<resultado>()`

ou

`test_dado_<condicao>_quando_<acao>_entao_<resultado>()`

Exemplos:

* `test_quando_nf_saida_tem_letras_entao_rejeita()`
* `test_dado_sessao_ativa_quando_outro_usuario_tenta_abrir_entao_bloqueia()`

---

# 📋 Checklist Mínimo de Qualidade

Todo teste deve:

* Ter contrato claro (nome ou comentário)
* Usar arrange mínimo
* Ter assert de efeito real
* Falhar pelo motivo correto
* Não depender de detalhe irrelevante

---

# 🧩 Padrão de Fixtures e Base Compartilhada

## Dados compartilhados

Usar `conftest.py`

Estrutura recomendada:

* `tests/conftest.py` → Core
* `web/conftest.py` → Fixtures Django comuns
* `web/<app>/conftest.py` → Fixtures específicas

## Helpers e Mixins

Opcional:

* `web/<app>/tests/_base.py`

Regra:
_base.py não deve criar dados ocultos.
Dados devem vir de fixtures explícitas.

---

# 🔄 Processo de Auditoria (App por App)

Para cada teste:

1. Definir contrato em 1 frase
2. Identificar camada
3. Avaliar clareza
4. Avaliar fragilidade
5. Classificar status

🚫 Não alterar regra de negócio nesta fase.
🚫 Não criar testes novos ainda.

✔ Primeiro organizar.
✔ Depois fortalecer.
✔ Só então criar GAPs.

---

# 📍 Ordem Estratégica de Auditoria

1. iam
2. redes
3. execucao
4. cadastro
5. chamados

---

# 📊 Tabela de Tracking

| App      | Arquivo                         | Total | LEGACY | KEEP | REFATORAR | REMOVER |
| -------- | ------------------------------- | ----- | ------ | ---- | --------- | ------- |
| iam      | test_models.py                  | ?     | 🟡     | 0    | 0         | 0       |
| redes    | test_validacao_ip.py            | ?     | 🟡     | 0    | 0         | 0       |
| execucao | test_execution_session_model.py | ?     | 🟡     | 0    | 0         | 0       |
| cadastro | test_models.py                  | ?     | 🟡     | 0    | 0         | 0       |
| chamados | test_models_chamado_basics.py   | ?     | 🟡     | 0    | 0         | 0       |

(Preencher durante auditoria.)



# 📊 Estado Atual da Suíte

Total coletado: **162 testes**
Status atual:

* 🟡 LEGACY: 160
* 🟢 KEEP: 2
* 🔵 REFATORAR: 0
* 🔴 REMOVER: 0

# 📊 Tabela de Tracking Atualizada

Última atualização: 2026-02-15
Fonte oficial: `pytest --collect-only -q`
