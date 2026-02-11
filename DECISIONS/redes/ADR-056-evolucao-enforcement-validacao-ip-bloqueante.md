# ADR-056 — Evolução do enforcement: validação de IP por regra torna-se bloqueante quando houver governança completa

**Data:** 2026-02-04  
**Status:** Proposto

## Decisão
Na fase futura (após integração Cadastro ↔ Redes), regras passam a ser aplicadas como bloqueio:

- IP inválido para a regra → `ERROR` **bloqueante**
- `TYPO_WARNING` pode continuar como `WARN` (não bloqueante)

O ponto de bloqueio será aplicado em um destes locais (a decidir quando implementar):
- setup do chamado
- validação final antes de concluir execução

## Contexto
No MVP atual, a validação roda como service puro, com warnings não bloqueantes.

Ao integrar regras governadas no cadastro, a ausência de enforcement permite inconsistências
operacionais (IP “qualquer” para um tipo conhecido).

Ainda assim, a implementação deve respeitar pré-condições de maturidade do domínio.

## Consequências
- A validação evolui de orientação (WARN) para governança (ERROR bloqueante).
- Regras de rede tornam-se contrato operacional de execução.
- A decisão do ponto exato de bloqueio deve ser registrada em ADR específica no momento da implementação.