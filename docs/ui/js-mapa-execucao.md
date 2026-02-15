# Mapa HTML → JS — Execução (Source of Truth)

Este documento é a fonte de verdade do **carregamento de JavaScript** nas páginas de Execução.

Objetivo:
- Evitar scripts “fantasma” e responsabilidades duplicadas.
- Tornar explícito **quais páginas carregam quais scripts**.
- Preparar o terreno para PR6 (execution_state) e padronização de carregamento (`defer`).

---

## Regras (estado desejado)

- Todo `<script src="...">` externo deve usar `defer`, salvo justificativa explícita no template.
- Cada template deve conter um comentário listando os JS que carrega (dependências).
- Cada arquivo JS deve conter header comment: responsabilidade + páginas onde roda + contratos (IDs/data-*).

---

## Tabela de dependências (inventário atual)

| Template (web/chamados/templates/execucao/) | JS (web/execucao/static/execucao/js/) | Defer | Responsabilidade (placeholder) | App dono (placeholder) |
|---|---|---:|---|---|
| fila_operacional.html | fila_operacional.js | ✅ | TODO | TODO |
| chamado_abertura.html | chamado_abertura.js | ❌ | TODO | TODO |
| chamado_setup.html | chamado_setup.js | ❌ | TODO | TODO |
| chamado_execucao.html | chamado_detalhe.js | ✅ | TODO | TODO |
| chamado_execucao.html | chamado_salvar_execucao.js | ❌ | TODO | TODO |
| chamado_execucao.html | item_configurado.js | ❌ | TODO | TODO |
| chamado_execucao.html | chamado_finalizar.js | ✅ | TODO | TODO |

---

## Lista única de scripts (assets existentes)

- fila_operacional.js
- chamado_abertura.js
- chamado_setup.js
- chamado_detalhe.js
- chamado_salvar_execucao.js
- item_configurado.js
- chamado_finalizar.js

---

## Observações técnicas (problemas detectados)

### Mistura de `defer`
- Templates com `defer` consistente:
  - fila_operacional.html (fila_operacional.js)
  - chamado_execucao.html (chamado_detalhe.js, chamado_finalizar.js)

- Templates com scripts **sem `defer`**:
  - chamado_abertura.html (chamado_abertura.js)
  - chamado_setup.html (chamado_setup.js)
  - chamado_execucao.html (chamado_salvar_execucao.js, item_configurado.js)

Impacto: risco de inicialização em ordem diferente, dependência implícita e regressões ao introduzir `execution_state.js` (PR6).

---

## Próximos passos (MT-02+)

- [ ] Inserir comentário em cada template listando dependências JS.
- [ ] Adicionar header comment em cada JS com: responsabilidade + páginas + contrato esperado.
- [ ] Padronizar `defer` (todos com `defer` ou justificar exceção).
- [ ] Renomear scripts para nomes semânticos por fluxo/página (remover `chamado_*` legado).
- [ ] Reavaliar “app dono” (chamados vs execucao) por responsabilidade real.


Ownership definido

| Template              | JS                                       | App dono | Defer | Comentário no template | Header no JS |
| --------------------- | ---------------------------------------- | -------- | ----: | ---------------------: | -----------: |
| fila_operacional.html | execucao/js/execucao_fila_operacional.js | execucao |     ✅ |                      ✅ |            ✅ |
| chamado_abertura.html | chamados/js/chamados_abertura.js         | chamados |     ✅ |                      ✅ |            ✅ |
| chamado_setup.html    | chamados/js/chamados_setup.js            | chamados |     ✅ |                      ✅ |            ✅ |
| chamado_execucao.html | execucao/js/execucao_detalhe.js          | execucao |     ✅ |                      ✅ |            ✅ |
| chamado_execucao.html | execucao/js/execucao_salvar.js           | execucao |     ✅ |                      ✅ |            ✅ |
| chamado_execucao.html | execucao/js/execucao_item_configurado.js | execucao |     ✅ |                      ✅ |            ✅ |
| chamado_execucao.html | execucao/js/execucao_finalizar.js        | execucao |     ✅ |                      ✅ |            ✅ |



## Smoke (MT-07)
- manage.py check: OK
- findstatic (execucao + chamados): OK
- Smoke manual (fila/abertura/setup/execução): OK (console limpo / assets 200)

---

## Estado final pós-limpeza (baseline)

### Regras consolidadas
- Ownership de JS é por app (chamados vs execucao).
- Somente templates de página carregam JS (componentes/parciais não importam scripts).
- Todos os scripts externos são carregados com `defer`.
- Headers de JS e comentários "Depends on" nos templates são obrigatórios.

### Smoke / verificação de assets
- `python web/manage.py check` ✅
- `python web/manage.py findstatic ...` ✅ (todos assets resolvem)
- Smoke manual: fila, abertura, setup, execução/detalhe ✅ (console limpo, assets 200)

---


## PR6 — Pré-requisitos e páginas-alvo do execution_state.js

### Onde o state manager deve rodar
O `execution_state.js` será carregado **apenas em páginas que exibem/alteram estado de execução**.

Páginas-alvo:
- web/chamados/templates/execucao/chamado_execucao.html

Páginas fora do escopo (por enquanto):
- fila_operacional.html (pode entrar depois se houver estado/lock no front)
- chamado_abertura.html (domínio do chamado)
- chamado_setup.html (domínio do chamado)

### Contrato mínimo esperado (data-*)
A página de execução/detalhe deve expor um host com dataset:

- `data-has-session="0|1"`
- `data-can-edit="0|1"`
- `data-can-finalize="0|1"`

E o JS deve ser idempotente:
- `applyExecutionState()` pode ser chamado múltiplas vezes sem efeitos colaterais.

### Lista de scripts na página (ordem recomendada, todos com defer)
- execucao/js/execution_state.js (novo - PR6)
- execucao/js/execucao_detalhe.js
- execucao/js/execucao_item_configurado.js
- execucao/js/execucao_salvar.js
- execucao/js/execucao_finalizar.js

Observação:
- A PR6 deve remover qualquer lógica de “read-only global” espalhada e centralizar em `execution_state.js`.