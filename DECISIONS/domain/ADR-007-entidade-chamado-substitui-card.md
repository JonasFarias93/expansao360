# ADR-007 — Entidade operacional “Chamado” substitui “Card”

**Data:** 2026-01-21  
**Status:** Aceito

## Decisão
A entidade anteriormente referida como “Card” passa a se chamar **Chamado** no domínio do sistema.

## Contexto
O termo “Card” é genérico e pode causar ambiguidade com elementos visuais da interface.
“Chamado” é um termo consolidado em contextos operacionais e de TI, representando uma
unidade de trabalho com status, histórico e rastreabilidade.

## Consequências
- O domínio e os casos de uso passam a utilizar o termo “Chamado”.
- A CLI e a Web expõem o conceito como “Chamado”.
- Caso necessário, aliases temporários podem ser mantidos para compatibilidade.