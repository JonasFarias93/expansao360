# ADR-053 — IpPolicy como estratégia de atribuição/validação de IP por equipamento

**Data:** 2026-02-04  
**Status:** Aceito

## Decisão
Definir o campo `ip_policy` em `RegraRedeEquipamento` como enum `IpPolicy` para suportar estratégias:

- `OFFSET_FIXO`
- `SEQUENCIAL`
- `FAIXA`

Manter campos MVP para suportar políticas atuais e evolução incremental:

- `offset_fixo`
- `offset_inicio`, `offset_fim`
- `offset_base`
- `reservados` (JSON)

## Contexto
O MVP de redes começa com regras simples (ex.: TC), mas precisa escalar para outros equipamentos
que podem ter:

- IP em offset fixo
- ranges por faixa
- distribuição sequencial (com base e reservas)

Codificar isso como if/else em serviços não escala.

## Consequências
- `ip_policy` explicita a estratégia aplicada pela regra.
- Campos de offsets suportam implementação incremental por policy.
- `reservados` permite exceções sem alterar schema (MVP simples), com disciplina futura via ADR.
- As regras passam a ser dados (registry) e não apenas código.