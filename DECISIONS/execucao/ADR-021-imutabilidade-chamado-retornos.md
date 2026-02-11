# ADR-021 — Imutabilidade do Chamado: Correções e Retornos Geram Novo Chamado

**Data:** 2026-02-04  
**Status:** Aceito

## Decisão
Correções e retornos devem gerar um **novo Chamado**,
nunca edição destrutiva de um chamado já existente.

## Contexto
Chamados representam eventos operacionais e contábeis reais.

Alterar destrutivamente um chamado encerrado comprometeria:

- Rastreabilidade
- Auditoria
- Integridade contábil
- Histórico operacional

O modelo precisa refletir que cada chamado é um evento fechado no tempo.

## Consequências
- Histórico torna-se imutável.
- Retornos exigem novo chamado com vínculo explícito ao anterior (quando aplicável).
- Auditoria e contabilidade permanecem preservadas.
- Evita edição retroativa de dados operacionais.
- Simplifica rastreabilidade de eventos reais.