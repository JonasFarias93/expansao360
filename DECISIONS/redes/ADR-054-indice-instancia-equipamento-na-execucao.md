# ADR-054 — Índice/instância de equipamento pertence à Execução (Operation), não ao Cadastro (Registry)

**Data:** 2026-02-04  
**Status:** Aceito

## Decisão
O **índice da instância** do equipamento (ex.: `PDV #1`, `PDV #2`) pertence sempre à **Execução (Operation)**.

O Cadastro (Registry) mantém apenas o **tipo lógico** (`TipoEquipamento`, ex.: `PDV`, `TC`, `CONSULTA_PRECO`),
sem numeração, índice ou instâncias.

## Contexto
Modelar instâncias no cadastro (ex.: `PDV1`, `PDV2`, `PDV3`) mistura planejamento com execução e gera:

- explosão de registros
- maior custo de manutenção
- inconsistência de governança
- acoplamento indevido do fluxo operacional no registry

No mundo real, `PDV1/PDV2` são apenas instâncias do mesmo tipo,
e a quantidade/ordem nasce no chamado/kit e é materializada na execução.

## Consequências
- A **instância real** do equipamento nasce na execução (Operation).
- O índice da instância pode ser usado para derivar offsets/IPs conforme a regra de rede.
- O Cadastro mantém governança de tipo e padronização, sem representar multiplicidade operacional.