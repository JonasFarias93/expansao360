# ADR-041 — Sessão exclusiva de execução por Chamado (lock)

**Data:** 2026-02-08  
**Status:** Aceito

## Decisão
Criar a entidade operacional `ExecutionSession`
para garantir lock exclusivo por `Chamado` durante a execução.

Uma sessão ativa é definida como:

- `ended_at IS NULL`
- `expires_at > now()`

## Contexto
Na fila operacional, ao clicar “Abrir”, é necessário impedir
edição concorrente do mesmo chamado por técnicos diferentes,
mantendo rastreabilidade e permitindo reentrada pelo mesmo técnico.

## Consequências
- `ExecutionSession` armazena:
  - chamado
  - usuário
  - started_at
  - expires_at
  - ended_at
  - ended_reason
- Restrição no banco garante no máximo 1 sessão ativa por chamado.
- Histórico de sessões é preservado (FK em vez de OneToOne).
- Ainda não há:
  - job de timeout
  - tomada de sessão
  - autosave
  (devem virar ADRs futuras quando decididos)