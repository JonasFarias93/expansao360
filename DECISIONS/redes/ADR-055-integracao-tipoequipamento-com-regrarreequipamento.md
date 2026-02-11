# ADR-055 — Integração entre Cadastro e Redes via RegraRedeEquipamento (FK opcional)

**Data:** 2026-02-04  
**Status:** Proposto

## Decisão
Permitir que `TipoEquipamento` (Registry) referencie opcionalmente uma regra de rede (`RegraRedeEquipamento`)
para governança e validação consistente de IP.

A integração é planejada como **FK opcional**, para permitir adoção incremental.

## Contexto
O serviço de redes valida/classifica IP com base em:

- perfil de rede ativo
- regra do tipo do equipamento
- IP informado
- (futuro) índice da instância na execução

Conectar Cadastro ↔ Redes permite:

- governança do tipo (registry)
- aplicação determinística da regra (redes)
- redução de “strings soltas” e exceções manuais

## Consequências
- O cadastro passa a ser capaz de apontar a regra correta (quando aplicável).
- A execução poderá consultar a regra via tipo de equipamento (sem hardcode).
- Mudança deve ser aplicada apenas quando:
  - cadastro estiver estável
  - regras cobrirem mais de um tipo além de `TC`