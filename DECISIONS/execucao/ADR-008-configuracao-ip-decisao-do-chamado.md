# ADR-008 — Configuração (ex.: IP) é decisão do Chamado, não do Kit

**Data:** 2026-02-03  
**Status:** Aceito (ajuste de entendimento)

## Decisão
A necessidade de configuração operacional (ex.: exigir IP) é decidida na execução do **Chamado**
e não imposta pelo cadastro de Kit/KitItem.

## Contexto
No cadastro, um Kit pode sugerir que um item costuma precisar de configuração,
mas a obrigatoriedade varia por cenário/loja/orientação e deve ser avaliada
no momento da execução.

## Consequências
- Campo operacional `deve_configurar` vive na execução.
- Campos operacionais como `ip` ficam na execução.
- O cadastro pode manter um campo de sugestão (`sugere_configuracao`)
  sem caráter obrigatório.
- A validação de finalização exige configuração somente quando `deve_configurar=True`.