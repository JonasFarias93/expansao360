# ADR-011 — Separação entre Abertura do Chamado e Fila Operacional

**Data:** 2026-02-04  
**Status:** Aceito

## Decisão
Introduzir explicitamente a separação entre:

- **Abertura do Chamado (setup operacional)**
- **Execução Operacional (fila de trabalho)**

Chamados **não entram automaticamente na fila operacional no momento da criação**.

## Contexto
Durante ajustes de layout e fluxo, foi identificado que:

- A tela de decisão operacional (bipagem e “configurar este item”) estava sendo exibida
  diretamente na fila operacional.
- Isso causava confusão de fluxo e a impressão de que itens já estavam “em execução”
  logo após a criação.
- A decisão de configuração (`deve_configurar`) pertence ao step de abertura,
  não à execução em fila.

O problema não era estético, mas **arquitetural**: ausência de um estado explícito
para o momento intermediário entre “criado” e “em execução”.

## Decisão Técnica
O ciclo de vida do Chamado passa a considerar explicitamente:

### 1) Abertura / Preparação
- Criação do Chamado
- Geração dos itens de execução
- Decisão de configuração (`deve_configurar`)
- Planejamento técnico (definição de IP obrigatório quando aplicável)

### 2) Fila Operacional
- Apenas Chamados prontos para execução entram na fila
- Chamados em abertura **não aparecem** na fila

A transição para a fila ocorre explicitamente após salvar os itens
e concluir as decisões iniciais.

## Consequências
- Elimina mistura de responsabilidades entre setup e execução.
- Evita estados “meio operacionais”.
- Reduz risco de regressão por alterações de layout.
- Permite validações mais claras por estágio.
- Abre caminho para possíveis wizards de abertura no futuro.
- Melhora métricas operacionais (fila reflete apenas trabalho executável).