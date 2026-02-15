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

