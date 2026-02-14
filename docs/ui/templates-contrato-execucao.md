# Contrato de Templates — Execução (Chamados)

Este documento define responsabilidades e contexto mínimo esperado por cada template
do app `execucao`, para evitar mistura entre abertura/planejamento e execução operacional.

## Princípios
- Página (`execucao/*.html`) **orquestra** componentes; não implementa regra de negócio.
- Componente (`execucao/components/*.html`) concentra UI/ações do bloco específico.
- **Fila não pode virar detalhe.**
- `ABERTO` = estado de fila/transição (setup obrigatório via guard server-side).
- Execução ativa ocorre a partir de `EM_EXECUCAO` (primeiro save operacional promove `ABERTO -> EM_EXECUCAO`).
- Setup é uma tela dedicada e obrigatória quando status = `ABERTO`.

Fonte (guard/fluxo):
- Guard ABERTO → setup: `web/execucao/views.py:539` (e também `771`, `1023`, `1028`)
- Promoção ABERTO → EM_EXECUCAO: `web/execucao/views.py:815-816`
- Enum de status: `web/execucao/models.py:41-43`

---

## execucao/chamado_abertura.html

**Responsabilidade:** Tela 1 — criar chamado  
✅ Contém somente o formulário de criação (`ChamadoCreateForm`)

**Recebe no contexto:**
- `form`

**Não pode conter:**
- `chamado`, itens, evidências, gates, finalizar, ações operacionais.

---

## execucao/chamado_setup.html

**Responsabilidade:** Tela 2 — setup/planejamento do chamado (`status == ABERTO`)  
✅ Define itens, necessidade de configuração, IP (quando aplicável) e valida “pronto para execução”.

**Recebe no contexto:**
- `chamado`
- `itens` (lista/qs já ordenado)
- (opcionais) `gate_*` / flags de validação de planejamento (ex.: `pode_iniciar_execucao`)

**Inclui (ordem recomendada):**
1. `components/_header_chamado.html`
2. `components/_itens_chamado_setup.html` (modo planejamento)
3. `components/_setup_actions.html` (CTA “Iniciar execução”, salvar, validações visuais)

Fonte (include itens setup):
- `web/execucao/templates/execucao/chamado_setup.html:19`

**Não pode conter:**
- upload de evidências
- finalizar
- ações operacionais de ponta final (NF, coleta, etc.)

---

## execucao/chamado_execucao.html

**Responsabilidade:** Página “viva” do chamado (somente operação — `status != ABERTO`)  
✅ Apenas orquestra includes; não deve ter regra de negócio.

**Recebe no contexto:**
- `chamado`
- `itens` (lista/qs já ordenado)
- `evidencias`
- `evidencia_tipos`
- `pode_liberar_nf`
- (opcionais) `is_envio`, `is_retorno`, `gate_*`

**Inclui (ordem recomendada):**
1. `components/_header_chamado.html`
2. `components/_card_operacional_chamado.html`
3. `components/_itens_chamado_execucao.html` (modo operação)

Fonte (include itens execução):
- `web/execucao/templates/execucao/chamado_execucao.html:21`

**Nota:**
- Evidências ficam dentro do card operacional (ponta final).

---

## execucao/fila_operacional.html

**Responsabilidade:** Lista de trabalho  
✅ Renderiza cards compactos e links/CTAs.

**Recebe no contexto:**
- `chamados`
- (opcional) `rows`

**Inclui:**
- `components/_card_operacional_chamado.html` (modo compacto)

**Não pode conter:**
- itens, evidências, gates em form, nada que pareça “detalhe do chamado”.

---

## execucao/historico_chamados.html

**Responsabilidade:** Consulta / auditoria  
✅ Lista chamados (com busca).

**Recebe no contexto:**
- `chamados`
- `q`

**Não pode conter:**
- forms operacionais (salvar item/finalizar/gates)
- upload de evidências

---

## components/_header_chamado.html

**Responsabilidade:** Banner superior informativo do chamado  
✅ Exibe metadados (protocolo, tipo, prioridade, status, loja/projeto etc.)

**Recebe no contexto:**
- `chamado`

**Não pode conter:**
- gates, finalizar, upload de evidências, salvar itens.

---

## components/_card_operacional_chamado.html

**Responsabilidade:** Ponta final de trabalho do chamado (ações operacionais)  
✅ Este é o card onde o técnico trabalha.

**Modo Full (detalhe):**
- ações de assumir / gates / finalizar
- inclui evidências

**Modo Compact (fila):**
- apenas resumo + link "Abrir"

Arquivos relacionados (as-is):
- `components/_card_operacional_chamado.html` (wrapper / modo compacto)
- `components/_card_operacional_chamado_full.html` (modo full)

**Recebe no contexto (full):**
- `chamado`
- `pode_liberar_nf`
- `evidencias`
- `evidencia_tipos`

**Recebe no contexto (compact):**
- `chamado`

Fonte (include evidências no full):
- `web/execucao/templates/execucao/components/_card_operacional_chamado_full.html:81`

---

## components/_itens_chamado_setup.html

**Responsabilidade:** Itens do chamado em modo planejamento (`status == ABERTO`).

**Recebe no contexto:**
- `chamado`
- `itens`

---

## components/_itens_chamado_execucao.html

**Responsabilidade:** Itens do chamado em modo operação (`status != ABERTO`).

**Recebe no contexto:**
- `chamado`
- `itens`

---

## components/_evidencias_chamado.html

**Responsabilidade:** Upload + listagem de evidências.

**Recebe no contexto:**
- `chamado`
- `evidencias`
- `evidencia_tipos`

---

## components/_setup_actions.html

**Responsabilidade:** Ações do setup (planejamento)  
✅ CTA de salvar e “Iniciar execução”, com mensagens de bloqueio visual.

**Recebe no contexto:**
- `chamado`
- (opcional) `pode_iniciar_execucao`
- (opcional) `motivos_bloqueio` (lista de strings)

---

## Provas automatizadas (nível 2)

- Execução usa template correto:
  - `web/execucao/tests/test_views_chamado_execucao_get.py:44`
- Fila operacional tem cobertura:
  - `web/execucao/tests/test_views_fila_operacional.py:*`
- Fluxo de setup/abrir:
  - `web/execucao/tests/test_chamado_abrir_inicia_sessao.py:34`

---

Última revisão: 2026-02-11  
Fonte: `web/execucao/views.py`, `web/execucao/models.py`, `web/execucao/templates/execucao/*`, `web/execucao/tests/*`