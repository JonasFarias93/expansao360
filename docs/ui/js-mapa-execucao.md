# Mapa HTML → JS — Execução (Source of Truth)

Este documento é a **fonte oficial de verdade** sobre o carregamento de JavaScript nas páginas do fluxo de Execução.

Objetivo:

* Evitar scripts “fantasma” e responsabilidades duplicadas.
* Tornar explícito quais páginas carregam quais scripts.
* Garantir ownership claro por app.
* Servir como baseline arquitetural para PR6 (execution_state).

---

# Regras Consolidadas

1. Ownership de JS é por app (**chamados** ou **execucao**).
2. Somente **templates de página** carregam scripts.
3. Componentes/parciais **não** importam JS.
4. Todos os scripts externos devem usar `defer`.
5. Cada template deve conter comentário "Depends on" listando seus JS.
6. Cada arquivo JS deve conter header documentando:

   * Páginas onde roda
   * Responsabilidade
   * Pré-requisitos de DOM (IDs, classes, data-attrs)

---

# Ownership e Dependências (Estado Atual Consolidado)

| Template (web/chamados/templates/execucao/) | JS carregado                             | App dono | Defer | Comentário no template | Header no JS |
| ------------------------------------------- | ---------------------------------------- | -------- | :---: | :--------------------: | :----------: |
| fila_operacional.html                       | execucao/js/execucao_fila_operacional.js | execucao |   ✅   |            ✅           |       ✅      |
| chamado_abertura.html                       | chamados/js/chamados_abertura.js         | chamados |   ✅   |            ✅           |       ✅      |
| chamado_setup.html                          | chamados/js/chamados_setup.js            | chamados |   ✅   |            ✅           |       ✅      |
| chamado_execucao.html                       | execucao/js/execucao_detalhe.js          | execucao |   ✅   |            ✅           |       ✅      |
| chamado_execucao.html                       | execucao/js/execucao_salvar.js           | execucao |   ✅   |            ✅           |       ✅      |
| chamado_execucao.html                       | execucao/js/execucao_item_configurado.js | execucao |   ✅   |            ✅           |       ✅      |
| chamado_execucao.html                       | execucao/js/execucao_finalizar.js        | execucao |   ✅   |            ✅           |       ✅      |

---

# Smoke (MT-07)

Validação pós-limpeza estrutural:

* `python web/manage.py check` → OK
* `python web/manage.py findstatic` (todos os JS) → OK
* Smoke manual (fila, abertura, setup, execução/detalhe) → OK
* Console limpo (sem erros JS)
* Assets retornando HTTP 200

Este estado é considerado **baseline estável**.

---

# Estado Final Pós-Limpeza (Baseline Oficial)

Após MT-01 até MT-07:

* Naming de arquivos JS é semântico e orientado por fluxo.
* JS está fisicamente localizado no app responsável.
* Não há mistura de `defer`.
* Não há referências a nomes antigos.
* Console das páginas principais está limpo.
* O sistema está pronto para introdução de state manager.

---

# PR6 — Pré-requisitos e Diretrizes

## Onde o execution_state.js deve rodar

O state manager deve ser carregado **apenas na página que controla estado de execução**:

* `web/chamados/templates/execucao/chamado_execucao.html`

Páginas fora do escopo inicial:

* fila_operacional.html
* chamado_abertura.html
* chamado_setup.html

---

## Contrato mínimo esperado (data-*)

A página `chamado_execucao.html` deve expor um host com os seguintes atributos:

* `data-has-session="0|1"`
* `data-can-edit="0|1"`
* `data-can-finalize="0|1"`

O state manager deve ser:

* Idempotente
* Determinístico
* Baseado exclusivamente no contrato `data-*`

`applyExecutionState()` deve poder ser chamado múltiplas vezes sem efeitos colaterais.

---

## Ordem recomendada de scripts na página de execução

Todos com `defer`:

1. execucao/js/execution_state.js (novo — PR6)
2. execucao/js/execucao_detalhe.js
3. execucao/js/execucao_item_configurado.js
4. execucao/js/execucao_salvar.js
5. execucao/js/execucao_finalizar.js

---

## Diretriz Arquitetural da PR6

* Remover qualquer lógica espalhada de “read-only global”.
* Centralizar controle de estado em `execution_state.js`.
* JS de página deve apenas reagir ao contrato (não decidir regras).

---

# Status

✅ JS organizado por ownership
✅ Loading padronizado
✅ Dependências explícitas
✅ Baseline estável

Sistema oficialmente **Pronto para iniciar PR6**.
