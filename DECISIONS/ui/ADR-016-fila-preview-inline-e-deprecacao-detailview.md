# ADR-016 — Fila de Chamados: Preview Inline e Deprecação da DetailView

**Data:** 2026-02-05  
**Status:** Aceito

## Decisão
Reestruturar o comportamento do botão "Detalhes" na Fila Operacional,
transformando-o em um preview inline (accordion) e descontinuando
o uso da `ChamadoDetailView` como destino desse botão.

A decisão envolve três pontos principais:

1) O botão "Detalhes" passa a abrir um preview inline no próprio card.
2) A `ChamadoDetailView` deixa de ser o destino do botão.
3) O JavaScript da fila e da execução passam a ser separados por página.

---

## 1) Preview Inline na Fila

### Contexto
O botão "Detalhes" abria uma `DetailView`, mas essa experiência
era praticamente idêntica ao fluxo de "Abrir", gerando redundância
e fricção na triagem.

### Decisão
O botão "Detalhes" passa a ser um accordion inline no card,
com preview simples e sem regras operacionais.

### Consequências
- A fila fica mais rápida para triagem.
- Evita criação de página adicional.
- "Abrir" permanece como único fluxo para execução.

---

## 2) Deprecação da ChamadoDetailView

### Contexto
Com o preview inline, a `DetailView` deixa de ser necessária
para a navegação principal da fila.

### Decisão
- O botão "Detalhes" não chama mais a `DetailView`.
- A `DetailView` pode:
  - Redirecionar para a tela de execução (`ChamadoExecucaoView`), ou
  - Permanecer temporariamente para retrocompatibilidade.

### Consequências
- Evita duplicidade de telas.
- Mantém compatibilidade com URLs antigas.
- Reduz manutenção futura.

---

## 3) Organização de JavaScript por Página

### Contexto
`execucao/js/chamado_detalhe.js` continha lógica específica da execução
(progress bar, edição inline de IP).

### Decisão
- `chamado_detalhe.js` permanece exclusivo da tela de execução.
- Criar `execucao/js/fila_operacional.js` para cuidar do accordion da fila.
- Proibir JS inline em templates.
- Scripts devem ser carregados com `defer`.

### Consequências
- Cada página possui seu comportamento isolado.
- Evita mistura de responsabilidades.
- Facilita manutenção e testes.