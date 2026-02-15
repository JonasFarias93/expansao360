# Auditoria de Testes — Expansão360

---

# 🎯 Objetivo da Auditoria

Esta auditoria tem como finalidade:

1. Garantir que cada teste possua **contrato claro e verificável**.
2. Organizar a suíte por **camadas arquiteturais e domínios**.
3. Padronizar **nomenclatura semântica**.
4. Criar rastreabilidade para refactor controlado.
5. Elevar a confiabilidade da suíte antes da versão 1.0.0.

⚠️ Importante:
Todo teste inicia como **🟡 LEGACY** até revisão formal.

---

# 📊 Estado Atual da Suíte

Total coletado: **162 testes**
Fonte oficial: `pytest --collect-only -q`

Status atual:

* 🟡 LEGACY: **0**
* 🟢 KEEP: **162**
* 🔵 REFATORAR: **0**
* 🔴 REMOVER: **0**

> Atualização desta rodada (2026-02-15):
>
> * Auditoria concluída (nenhum teste permanece como LEGACY).

---

# 🏷️ Legenda Oficial de Status

## 🟡 LEGACY

Teste ainda não auditado segundo o novo padrão.

## 🟢 KEEP

Teste auditado e aprovado segundo critérios:

* ✓ Nome semântico
* ✓ Arquivo correto por camada
* ✓ Uso adequado de fixtures
* ✓ Assert de efeito real
* ✓ Falha pelo motivo certo

## 🔵 REFATORAR

Teste válido, mas precisa:

* Renomeação
* Reorganização de arquivo
* Melhorar clareza de contrato
* Reduzir sobreposição

## 🔴 REMOVER

Teste duplicado, frágil ou de baixo valor (não representa requisito).

---

# 🏗️ Organização Oficial dos Testes

## 1️⃣ Core (Framework-agnostic)

Local: `tests/`

* `tests/domain/` → Value Objects e contratos puros
* `tests/usecases/` → Casos de uso
* `tests/cli/` → CLI e smoke

Regra:
Core **não pode** depender de Django.

---

## 2️⃣ Web / Django

Local: `web/<app>/tests/`

### Modelos

Arquivos: `test_models_*.py`

Protege:

* Invariantes
* Constraints
* Regras internas

### Serviços

Arquivos: `test_services_*.py`

Protege:

* Regras de domínio
* Transições de estado
* Idempotência

### Views

Arquivos: `test_views_*.py`

Protege:

* Permissões
* Fluxo HTTP
* Redirecionamentos
* Efeitos persistidos

### Forms

Arquivos: `test_forms_*.py`

Protege:

* Validação real
* Regras de negócio

### UI / TemplateTags

Arquivos: `test_ui_*.py`

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
* Teste estrutural irrelevante

---

# 🧠 Padrão de Nomenclatura

## Arquivos

Deve indicar contrato específico.

Exemplos corretos:

* `test_models_user_capability_unique.py`
* `test_services_execution_session_active.py`
* `test_views_chamado_take_session.py`

Temporário (LEGACY):

* `test_models.py`
* `test_forms.py`
* `test_views_flows.py`

---

## Funções de Teste

Formato preferido:

* `test_quando_<contexto>_entao_<resultado>()`
  ou
* `test_dado_<condicao>_quando_<acao>_entao_<resultado>()`

---

# 📋 Checklist Mínimo de Qualidade

Todo teste deve:

* Ter contrato claro
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
`_base.py` não deve criar dados ocultos.

---

# 🔄 Processo de Auditoria

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

# 📍 Ordem Estratégica

1. iam ✅
2. redes ✅
3. execucao ✅
4. cadastro ✅
5. chamados ✅

---

# 📊 Tabela de Tracking Atualizada

> Regras da tabela:
>
> * As colunas **LEGACY + KEEP + REFATORAR + REMOVER** devem somar o **Total**.
> * Migração de arquivo entre apps deve ser registrada como **arquivo novo no app destino** (e removido do app origem).

| App      | Arquivo                                       | Total | LEGACY | KEEP | REFATORAR | REMOVER |
| -------- | --------------------------------------------- | ----- | ------ | ---- | --------- | ------- |
| iam      | test_models_user_capability_unique.py         | 1     | 0      | 1    | 0         | 0       |
| redes    | test_services_validacao_ip_tc.py              | 8     | 0      | 8    | 0         | 0       |
| execucao | test_models_execution_session.py              | 2     | 0      | 2    | 0         | 0       |
| execucao | test_services_execution_session_active.py     | 5     | 0      | 5    | 0         | 0       |
| execucao | test_views_chamado_abrir_sessao_exclusiva.py  | 4     | 0      | 4    | 0         | 0       |
| execucao | test_views_chamado_take_session.py            | 3     | 0      | 3    | 0         | 0       |
| execucao | test_views_chamado_abrir_permissoes.py        | 1     | 0      | 1    | 0         | 0       |
| execucao | test_views_chamado_abrir_redirecionamentos.py | 3     | 0      | 3    | 0         | 0       |
| cadastro | test_views_loja_list_busca.py                 | 4     | 0      | 4    | 0         | 0       |
| cadastro | test_services_import_lojas.py                 | 4     | 0      | 4    | 0         | 0       |
| cadastro | test_models_kit_equipamento_constraints.py    | 4     | 0      | 4    | 0         | 0       |
| cadastro | test_models_loja_campos_validacao.py          | 2     | 0      | 2    | 0         | 0       |
| cadastro | test_models_tipo_equipamento_codigo.py        | 4     | 0      | 4    | 0         | 0       |
| cadastro | test_forms_itemkit_queryset_tipo.py           | 3     | 0      | 3    | 0         | 0       |
| cadastro | test_forms_smoke.py                           | 2     | 0      | 2    | 0         | 0       |
| cadastro | test_views_ajax_tipos_por_equipamento.py      | 1     | 0      | 1    | 0         | 0       |
| cadastro | test_views_api_kit_itens.py                   | 4     | 0      | 4    | 0         | 0       |
| execucao | test_views_chamado_salvar_dados_fiscais.py    | 4     | 0      | 4    | 0         | 0       |
| execucao | test_views_item_configurar_endpoint.py        | 4     | 0      | 4    | 0         | 0       |
| execucao | test_views_chamado_execucao_get.py            | 4     | 0      | 4    | 0         | 0       |
| execucao | test_views_fila_operacional.py                | 3     | 0      | 3    | 0         | 0       |
| execucao | test_views_chamado_atualizar_itens.py         | 1     | 0      | 1    | 0         | 0       |
| execucao | test_views_chamado_adicionar_evidencia.py     | 1     | 0      | 1    | 0         | 0       |
| execucao | test_api_loja_lookup.py                       | 3     | 0      | 3    | 0         | 0       |
| execucao | test_views_historico_filtro_java.py           | 1     | 0      | 1    | 0         | 0       |
| execucao | test_ui_urgencia_templatetags.py              | 5     | 0      | 5    | 0         | 0       |
| execucao | test_ui_execucao_ui_facade_templatetags.py    | 1     | 0      | 1    | 0         | 0       |
| execucao | test_ui_projeto_cores_templatetags.py         | 3     | 0      | 3    | 0         | 0       |
| execucao | test_ui_execucao_ui_templatetags.py           | 1     | 0      | 1    | 0         | 0       |
| execucao | test_views_chamado_salvar_execucao.py         | 4     | 0      | 4    | 0         | 0       |

### App `chamados` (arquivos presentes)
 
## 🧹 Limpeza de Infra (não conta como REMOVER de testes) (não conta como REMOVER de testes)

* `web/redes/tests.py` (arquivo vazio removido / sem testes coletados)

---

Última atualização: **2026-02-15**
