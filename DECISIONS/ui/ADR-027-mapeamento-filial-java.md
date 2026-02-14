# ADR-027 — Mapeamento Operacional: “Filial” como “Java” no Cadastro de Lojas

**Data:** 2026-02-02  
**Status:** Aceito

## Decisão
Exibir o campo **Filial** como **Java**
e **Nome Filial** como **Nome loja** na interface,
mantendo compatibilidade com a base externa.

## Contexto
O sistema precisa alinhar-se à linguagem operacional
utilizada no dia a dia da organização.

Internamente, o modelo utiliza nomenclatura técnica,
mas externamente o termo “Java” é o identificador reconhecido.

A decisão busca:

- Melhorar aderência operacional
- Evitar ruído semântico
- Preservar compatibilidade com integrações existentes

## Consequências
- O importador mapeia explicitamente os campos.
- A UI utiliza labels operacionais.
- O modelo interno permanece consistente.
- Testes cobrem o mapeamento entre nomenclatura técnica e operacional.
- Evita ruptura com sistemas externos.