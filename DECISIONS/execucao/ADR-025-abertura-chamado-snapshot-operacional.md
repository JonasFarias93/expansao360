# ADR-025 — Abertura de Chamado via UI com Snapshot Operacional

**Data:** 2026-01-24  
**Status:** Aceito

## Decisão
Permitir abertura de Chamado via UI,
gerando automaticamente os Itens de Execução
a partir do Kit selecionado, como um snapshot operacional.

## Contexto
Era necessário:

- Permitir testes end-to-end reais.
- Utilizar o sistema de forma operacional concreta.
- Garantir que a execução refletisse o estado do Kit no momento da abertura.

Os itens não devem depender dinamicamente do cadastro após a criação do Chamado.

## Consequências
- O Chamado nasce a partir do Registry (Kit).
- Itens de execução representam um snapshot do Kit no momento da criação.
- Itens são tratados como imutáveis conceitualmente (histórico).
- Alterações futuras no Kit não afetam Chamados já criados.
- Planejamento e execução ficam claramente separados.