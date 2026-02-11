# Auditoria de Dependências Frontend / JS — EXPANSÃO360

Este documento registra a stack JavaScript utilizada no projeto,
sua motivação técnica, impacto arquitetural e critérios de manutenção.

> Toda dependência JS deve ser documentada aqui.
> Dependências não registradas são consideradas não autorizadas.

---

# 1. Source of Truth

- Código JS: `web/**/static/**`
- Testes JS: `web/**/static/**/__tests__/`
- Testes ativos encontrados:
  - `web/cadastro/static/cadastro/js/__tests__/tipos_formset.test.js`
  - `web/cadastro/static/cadastro/js/__tests__/tipos_formset_dynamic_row.test.js`
- Comandos:
  - `npm run test:js`
  - `make test` (Python + JS)

---

# 2. Stack JS Atual (ativa)

## 2.1 Node / npm

**Categoria:** Tooling de desenvolvimento  
**Escopo:** Ambiente de dev e CI  

- Executa testes JS
- Suporta Jest
- Não faz parte do runtime de produção

---

## 2.2 Jest

**Categoria:** Testes automatizados de frontend  
**Status:** Ativo  

Usado para:

- Testar manipulação de DOM
- Testar comportamento dinâmico de formsets
- Detectar regressões em scripts frontend

Exemplos reais no repositório:

- `tipos_formset.test.js`
- `tipos_formset_dynamic_row.test.js`

---

## 2.3 jsdom

**Categoria:** Simulação de ambiente DOM  

Fornece:

- `window`
- `document`
- eventos
- manipulação de HTML

Permite execução de testes JS sem navegador real.

---

# 3. Requisitos Não Funcionais Derivados

## RNF-FE-001 — Testabilidade de Frontend

O sistema deve permitir testes automatizados de JavaScript
sem dependência de navegador real.

Justificativa:

- Redução de regressões
- Refactor seguro de UI
- Padronização de qualidade

---

## RNF-FE-002 — Isolamento de Runtime

Ferramentas JS:

- Não são parte do runtime de produção
- São restritas ao ambiente de desenvolvimento e CI

---

# 4. Consequências da Remoção

Remover Jest/jsdom implica:

- ❌ Remoção de testes JS existentes
- ❌ Perda de cobertura de regressões de UI
- ❌ Maior risco em refactors frontend

Qualquer remoção exige ADR formal.

---

# 5. Critério Objetivo de Manutenção

A stack JS deve permanecer enquanto:

- Existirem testes JS no repositório
- Scripts manipularem DOM dinamicamente
- CI executar testes JS

Pode ser removida apenas se:

- Testes JS forem removidos formalmente
- Scripts JS deixarem de existir
- ADR aprovar a remoção

---

# 6. Status da Auditoria

- [x] Stack JS mapeada
- [x] Testes JS confirmados no repositório
- [x] RNFs derivados explicitados
- [x] Impacto da remoção formalizado

---

Última revisão: 2026-02-11  
Fonte: `web/cadastro/static/cadastro/js/__tests__/`