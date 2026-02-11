# Contrato de Templates — Execução (Chamados)

Este documento define responsabilidades e contexto mínimo esperado por cada template
do app `execucao`, para evitar mistura entre abertura/planejamento e execução operacional.

## Princípios
- Página (`execucao/*.html`) **orquestra** componentes; não implementa regra de negócio.
- Componente (`execucao/components/*.html`) concentra UI/ações do bloco específico.
- **Fila não pode virar detalhe.**
- `ABERTO` = planejamento; `EM_EXECUCAO+` = operação.
- Setup é uma tela dedicada e obrigatória quando status = `ABERTO`.

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
2. `components/_itens_chamado.html` (modo planejamento)
3. `components/_setup_actions.html` (CTA “Iniciar execução”, salvar, validações visuais)

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
3. `components/_itens_chamado.html` (modo operação)

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

---

## components/_setup_actions.html

**Responsabilidade:** Ações do setup (planejamento)  
✅ CTA de salvar e “Iniciar execução”, com mensagens de bloqueio visual.

**Recebe no contexto:**
- `chamado`
- (opcional) `pode_iniciar_execucao`
- (opcional) `motivos_bloqueio` (lista de strings)