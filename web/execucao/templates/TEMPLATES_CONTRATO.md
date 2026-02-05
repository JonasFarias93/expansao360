# Contrato de Templates — Execução (Chamados)

Este documento define responsabilidades e contexto mínimo esperado por cada template
do app `execucao`, para evitar mistura entre abertura/planejamento e execução operacional.

## Princípios
- Página (`execucao/*.html`) **orquestra** componentes; não implementa regra de negócio.
- Componente (`execucao/components/*.html`) concentra UI/ações do bloco específico.
- **Fila não pode virar detalhe.**
- `ABERTO` = planejamento; `EM_EXECUCAO+` = operação.

---

## execucao/chamado_abertura.html

**Responsabilidade:** Tela 1 — criar chamado  
✅ Contém somente o formulário de criação (`ChamadoCreateForm`)

**Recebe no contexto:**
- `form`

**Não pode conter:**
- `chamado`, itens, evidências, gates, finalizar, ações operacionais.

---

## execucao/chamado_execucao.html

**Responsabilidade:** Página “viva” do chamado (planejamento + execução, dependendo do status)  
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
3. `components/_itens_chamado.html`

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

**Recebe no contexto (full):**
- `chamado`
- `pode_liberar_nf`
- `evidencias`
- `evidencia_tipos`

**Recebe no contexto (compact):**
- `chamado`

---

## components/_itens_chamado.html

**Responsabilidade:** Itens do chamado com “modo” por status.

**Recebe no contexto:**
- `chamado`
- `itens`

**Modo Planejamento (`status == ABERTO`):**
- `deve_configurar`
- `ip` obrigatório quando configurável e marcado

**Modo Operação (`status != ABERTO`):**
- bipagem (ativo/série) e conferência (confirmado)
- status de configuração + IP (edição controlada com log)

---

## components/_evidencias_chamado.html

**Responsabilidade:** Upload + listagem de evidências.

**Recebe no contexto:**
- `chamado`
- `evidencias`
- `evidencia_tipos`