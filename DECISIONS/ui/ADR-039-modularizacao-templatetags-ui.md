# ADR-039 — Modularização de templatetags por tema de UI

**Data:** 2026-02-06  
**Status:** Aceito

## Decisão
Separar os templatetags de UI do app `execucao`
em módulos semânticos por responsabilidade
(ex.: cores de projeto, urgência visual).

Manter `execucao_ui.py` como fachada (facade/reexport)
para compatibilidade com templates existentes.

## Contexto
O arquivo `execucao_ui.py` começou com responsabilidade única
(cores do projeto), mas a UI da execução está evoluindo.

Novas regras visuais (ex.: urgência) tendem a crescer,
e concentrar tudo em um único arquivo geraria um “arquivo deus”.

Era necessário separar por tema mantendo retrocompatibilidade.

## Consequências
- Novos templatetags devem ser criados em módulos dedicados
  (ex.: `execucao_projeto_cores.py`, `execucao_urgencia.py`).
- `execucao_ui.py` permanece como facade/reexport.
- Testes passam a ser organizados por tema
  (ex.: `test_ui_projeto_cores_templatetags.py`).
- Redução de acoplamento e melhor organização de UI.