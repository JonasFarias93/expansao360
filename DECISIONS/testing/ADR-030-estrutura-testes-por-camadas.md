# ADR-030 — Padronização da Estrutura de Testes por Camadas

**Data:** 2026-02-02  
**Status:** Aceito

## Decisão
Organizar os testes do projeto por camadas arquiteturais:

- Domain
- Usecases
- Interfaces

## Contexto
A organização anterior dos testes dificultava:

- Leitura
- Manutenção
- Escalabilidade
- Identificação da responsabilidade testada

Era necessário alinhar a estrutura de testes
com a arquitetura do sistema.

## Consequências
- Estrutura clara por responsabilidade.
- Facilita onboarding de novos desenvolvedores.
- Impõe disciplina para novos testes.
- Melhora rastreabilidade entre regra de negócio e teste.
- Reduz risco de acoplamento indevido entre camadas.