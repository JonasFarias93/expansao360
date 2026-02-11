# ADR-042 — Ação “Abrir” inicia ou reentra sessão de execução

**Data:** 2026-02-08  
**Status:** Aceito

## Decisão
O botão “Abrir” passa a:

- Criar uma `ExecutionSession` ativa para o Chamado, se não houver.
- Reentrar na sessão existente, caso pertença ao mesmo usuário.

Se existir sessão ativa de outro usuário,
a edição é bloqueada e o usuário é redirecionado
para o detalhe (modo read-only),
com mensagem informando:

“Em execução por X desde Y”.

## Contexto
É necessário:

- Evitar edição concorrente.
- Permitir reentrada do mesmo técnico.
- Garantir auditoria mínima de quem iniciou a execução.

Essa decisão complementa a criação da entidade `ExecutionSession`.

## Consequências
- A ação “Abrir” passa a ser um POST.
- Auditoria mínima garantida via:
  - `ExecutionSession.usuario`
  - `ExecutionSession.started_at`
- Redirecionamento conforme status:
  - `ABERTO` → setup
  - demais → detalhe
- Edição concorrente é bloqueada de forma explícita.