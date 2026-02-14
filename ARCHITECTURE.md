# Arquitetura — EXPANSÃO360

Este documento descreve a **arquitetura atual (as-is)** do sistema EXPANSÃO360,
com base no código existente, ADRs registrados e comportamento validado por testes.

> Fonte de verdade: código em `web/`, ADRs em `DECISIONS/`, testes automatizados.

---

# 1. Visão Geral

O **EXPANSÃO360** é um sistema orientado a processos de expansão e operação de campo,
com foco em:

* Padronização operacional
* Rastreabilidade histórica
* Governança explícita

O princípio arquitetural central é a **separação entre planejamento (Registry)**
e **execução (Operation)**.

* **Registry (Cadastro Mestre)** → define o que existe e como deve ser.
* **Operation (Execução)** → registra o que aconteceu de fato.

Essa separação evita ambiguidade histórica e impede que correções
alterem eventos já ocorridos.

---

# 2. Camadas Conceituais

## 2.1 Registry (Cadastro Mestre)

Responsável por manter entidades estruturais relativamente estáveis.

Exemplos implementados no app `cadastro`:

* Lojas
* Projetos
* Subprojetos
* Equipamentos
* Categorias
* Tipos de Equipamento
* Kits e seus itens

Características:

* Dados governados
* Alterações impactam apenas execuções futuras
* Não mantém histórico operacional
* Não depende do domínio de execução

Fonte:

* `web/cadastro/*`

---

## 2.2 Operation (Execução de Campo)

Responsável por registrar eventos reais e imutáveis.

Exemplos implementados no app `execucao`:

* Chamado
* Itens de execução
* Evidências
* Sessões de execução
* Fluxos ENVIO / RETORNO

Características:

* Alto volume transacional
* Histórico preservado
* Estados explícitos
* Gates operacionais formais

A camada Operation referencia Registry, nunca o contrário.

Fonte:

* `web/execucao/models.py`
* `web/execucao/views.py`

---

# 3. Entidade Central: Chamado

O **Chamado** é a unidade central da execução.

Representa:

* Um evento físico real
* Com contexto organizacional
* Com itens derivados de kit (snapshot)
* Com status e evidências

Tipos implementados:

* `ENVIO`
* `RETORNO`

Princípios:

* Chamados finalizados são imutáveis
* Correções geram novos chamados
* Fluxo inverso não altera histórico

Fonte:

* `web/execucao/models.py`
* testes em `web/execucao/tests/`

---

# 4. Ciclo de Vida do Chamado

Estados principais (conforme modelo atual):

1. **EM_ABERTURA**

   * Planejamento
   * Geração de itens
   * Definição de configuração

2. **ABERTO**

   * Promovido após salvar setup
   * Entra na fila operacional

3. **EM_EXECUCAO / AGUARDANDO_***

   * Execução ativa
   * Bipagem, conferência, evidências

4. **FINALIZADO**

   * Estado terminal
   * Histórico preservado

Chamados em `EM_ABERTURA` não aparecem na fila.

Fonte:

* `web/execucao/models.py`
* `web/execucao/views.py`

---

# 5. Snapshot Operacional

Ao criar um Chamado:

* Itens do kit são copiados
* Gera-se snapshot operacional
* Alterações futuras no kit não afetam chamados existentes

Objetivo:

* Garantir consistência histórica
* Preservar auditoria

Fonte:

* `web/execucao/models.py`
* `test_models_chamado_itens.py`

---

# 6. Gates Operacionais

O avanço do Chamado é protegido por validações formais.

Exemplos implementados:

* Liberação de NF exige itens válidos
* Finalização exige pré-condições
* Sessão ativa obrigatória para edição

Validações ocorrem na camada Application/Web,
com regras no domínio quando aplicável.

Fonte:

* `web/execucao/views.py`
* `web/execucao/tests/`

---

# 7. Modelo em Camadas (Visão Lógica)

```
┌────────────────────────────┐
│ Interfaces / Adapters      │
│ Web (Django) • CLI         │
└────────────▲───────────────┘
             │
┌────────────┴───────────────┐
│ Application                │
│ Views / Orquestração       │
└────────────▲───────────────┘
             │
┌────────────┴───────────────┐
│ Domain / Services          │
│ Regras puras               │
└────────────────────────────┘
```

Observação:

* O domínio não depende de Django.
* A Web atua como adapter.

---

# 8. Stack Web

Framework:

* Django

Apps principais:

* `cadastro`
* `execucao`
* `iam`
* `redes`

Diretrizes arquiteturais:

* Models não concentram regra crítica
* Views orquestram
* Templates não implementam regra
* Admin é ferramenta técnica

Fonte:

* Estrutura real do diretório `web/`

---

# 9. IAM (Autorização)

Modelo baseado em capabilities.

* Enforcement ocorre na camada Web
* Domínio é permission-agnostic

Exemplos:

* `execucao.chamado.finalizar`
* `execucao.evidencia.upload`

Fonte:

* `web/iam/`
* `CapabilityRequiredMixin`

---

# 10. Redes (Domínio Técnico)

Validação de IP implementada como service isolado.

* Contrato em `docs/redes/validacao-ip-mvp.md`
* Código em `web/redes/services/validacao.py`
* Testes em `web/redes/tests/`

O domínio redes é independente da UI.

---

# 11. Testes

Stack ativa:

* pytest
* pytest-django
* Jest + jsdom (frontend)

Testes Python em:

* `tests/`
* `web/*/tests/`

Testes JS em:

* `web/**/static/**/__tests__/`

Objetivo:

* TDD no domínio
* Regressão protegida

---

# 12. Princípios Arquiteturais Ativos

* Separação Registry vs Operation
* Histórico imutável
* Gates explícitos
* Pequenas mudanças rastreáveis
* Decisões registradas em ADR

---

# 13. Fora de Escopo Atual

* APIs públicas
* Integrações corporativas
* Multitenancy
* Infra hardening avançado
* Mobile/offline-first

---

# 14. Conclusão

A arquitetura atual privilegia:

* Clareza estrutural
* Governança
* Evolução segura
* Rastreabilidade real

Não é arquitetura teórica — é arquitetura validada pelo código existente.

---

Última revisão: 2026-02-11
Fonte:

* Estrutura real em `web/`
* Testes automatizados
* ADRs em `DECISIONS/`
