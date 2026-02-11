## Ajuste fino de UX no step de abertura

- Feedback visual claro de “setup” vs “execução”
- Possível separação visual ou wizard (futuro)


# Decisões pendentes de implementação

## ADR-033 — Padronização de códigos (internos vs externos) (Proposto)
- Consolidar comportamento na UI (inputs, readonly, hints)
- Garantir cobertura de testes por categoria de código

## ADR-036 — TipoEquipamento governado por Categoria
- Garantir que não exista fluxo de criação de Tipo fora da Categoria
- Adicionar validação mínima (Categoria com ao menos 1 Tipo ativo, quando aplicável)
- Testes cobrindo atualização de Categoria + Tipos

## Em avaliação — Itens duplicados na edição de Kit (UX)
- Decidir: bloquear duplicidade ou fazer merge automático de quantidades
- Se aceito, registrar ADR específica
- Implementar testes de formset para edição de Kit

## ADR-037 — Integração pytest + jest no Makefile
- Verificar se `make test` executa ambos (pytest + jest).
- Caso não execute, ajustar alvo único para rodar toda a suíte.