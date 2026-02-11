# ADR-043 — Validação e normalização de Contabilidade e NF Saída no Chamado

**Data:** 2026-02-09  
**Status:** Aceito

## Decisão
Aplicar padronização mínima no domínio para os campos:

- `contabilidade_numero`:
  - Normalizar com `strip()` antes de validar/salvar.
- `nf_saida_numero`:
  - Remover espaços.
  - Validar que contém apenas dígitos.
  - Mensagem padrão: “NF Saída deve conter apenas números.”

## Contexto
Esses campos são utilizados em processos fiscais e contábeis.

Formatos inconsistentes podem gerar:

- Problemas em auditoria
- Falhas de integração
- Inconsistência de relatórios

É necessário garantir validação mínima no domínio.

## Consequências
- Valores como “NF-123” passam a ser inválidos.
- Testes foram ajustados para utilizar apenas dígitos.
- Maior previsibilidade para processos contábeis.
- Redução de inconsistência de dados fiscais.