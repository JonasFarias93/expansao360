# ADR-058 — Separação do Domínio Chamado do App Execucao

## Data
2026-02-11

## Status
Aceito

## Decisão

Formalizar a separação conceitual do domínio **Chamado**
do escopo amplo do app `execucao`,
estabelecendo boundaries claros de responsabilidade.

Embora fisicamente ainda permaneça no mesmo app,
o domínio Chamado passa a ser tratado como subdomínio próprio
com regras isoladas.

## Contexto

O app `execucao` agregou múltiplas responsabilidades:

- Sessão operacional (ExecutionSession)
- Fluxo de execução em campo
- Evidências
- Regras fiscais (NF)
- Coleta
- Finalização
- Entidade Chamado

O modelo `Chamado` concentra regras de negócio próprias,
incluindo estados, transições e validações críticas.

Essa concentração indica identidade de domínio autônoma.

A ausência de boundary explícito aumenta acoplamento
e dificulta futura modularização.

## Consequências

### Positivas

- Redução de acoplamento conceitual
- Preparação para possível extração futura em app próprio
- Melhor clareza de responsabilidades
- Facilita testes isolados por domínio

### Negativas

- Exige disciplina arquitetural
- Pode demandar refatorações incrementais futuras

### Impacto Técnico

- Nenhuma alteração de schema
- Nenhuma alteração de rota
- Nenhum impacto imediato em testes