# DECISIONS — EXPANSÃO360

Este documento registra decisões técnicas e arquiteturais relevantes do projeto,
com o objetivo de evitar ambiguidades, manter rastreabilidade e facilitar onboarding.

## Formato padrão de cada decisão

* **Data** (YYYY-MM-DD)
* **Decisão**
* **Contexto**
* **Consequências**
* **Status** (opcional: Proposto | Aceito | Deprecado)

---

## 2026-01-20 — Separação conceitual: Registry x Operation

**Decisão**  
O sistema será modelado com duas camadas conceituais principais:

* **Registry (Cadastro Mestre):** define “o que existe” e “como deve ser”
* **Operation (Execução de Campo):** registra “o que foi executado”, com rastreabilidade e histórico

**Contexto**  
Precisamos garantir governança sobre padrões e, ao mesmo tempo, registrar a execução real
em campo sem poluir o cadastro mestre e sem perder histórico.

**Consequências**

* Operation referencia Registry; Registry não depende de Operation.
* O domínio será desenhado para suportar auditoria e evolução segura.

---

## 2026-01-20 — Estratégia de trabalho: microtarefas + disciplina de versionamento

**Decisão**  
O desenvolvimento seguirá por microtarefas com validação objetiva, usando branches e commits pequenos.

**Contexto**  
Queremos previsibilidade, rastreabilidade e redução de retrabalho.

**Consequências**

* Cada microtarefa deve resultar em um commit (quando aplicável).
* Push frequente após validação.
* Branches com nomes descritivos (`docs/`, `feat/`, `fix/`).

---

## 2026-01-20 — Branches base: main / develop

**Decisão**  
Usaremos:

* `main` para estabilidade e releases
* `develop` para integração contínua

**Contexto**  
Separar o que está pronto para release do que está em desenvolvimento reduz risco operacional.

**Consequências**

* Mudanças entram via branches derivadas.
* `main` recebe apenas conteúdo estável.

---

## 2026-01-21 — Stack Web definida: Django

**Decisão**  
A camada Web será implementada em **Django**.

**Contexto**  
Após estabilização do core, era necessário um framework maduro para UI, ORM e velocidade de entrega.

**Consequências**

* Core permanece independente.
* Django atua como adapter.
* Models Django não concentram regras de negócio complexas.

---

## 2026-01-21 — Entidade operacional “Chamado”

**Decisão**  
O termo **Chamado** substitui “Card” como entidade operacional.

**Contexto**  
“Card” é ambíguo e visual. “Chamado” representa melhor uma unidade operacional real.

**Consequências**

* Domínio, UI e testes utilizam “Chamado”.
* Histórico operacional preservado.

---

## 2026-02-03 — Configuração (ex.: IP) é decisão do Chamado, não do Kit

**Status:** Aceito

**Decisão**  
A necessidade de configuração operacional (ex.: exigir IP) é decidida na execução do **Chamado**
e não imposta pelo cadastro de Kit/KitItem.

**Contexto**  
O cadastro apenas sugere padrões; a obrigatoriedade varia conforme cenário real de execução.

**Consequências**

* Campo operacional `deve_configurar` pertence à execução.
* Validação exige IP **somente** quando `deve_configurar=True`.
* Cadastro não força configuração.

---

## 2026-02-03 — Gate de NF e critérios de fechamento do Chamado

**Decisão**  
O Chamado só será liberado para NF quando todos os itens estiverem conferidos.
O fechamento exige NF e confirmação de coleta quando aplicável.

**Contexto**  
Processo real exige controle contábil e evidência mínima antes de encerramento.

**Consequências**

* Método `pode_liberar_nf()` no Chamado.
* `finalizar()` valida regras conforme tipo (ENVIO / RETORNO).

---

## 2026-02-04 — Ciclo de Vida do Chamado, Prioridade e Ticket Externo

**Decisão**  
Evoluir o **Chamado** para operar com regras explícitas de ciclo de vida, incluindo:

* Ticket Externo obrigatório na criação
* Prioridade para ordenação da fila
* Estados intermediários (contábil, NF, coleta)
* `FINALIZADO` como estado terminal

**Contexto**  
O processo real não permite:
* NF sem contábil
* Finalização sem coleta
* Chamado sem ticket externo

**Consequências**

* Domínio reflete processo real.
* UI orienta avanço de status.
* Evita inconsistências operacionais.

---

# 🆕 2026-02-04 — Separação entre Abertura do Chamado e Fila Operacional

**Status:** Aceito

## Decisão
Introduzir explicitamente a separação entre:

* **Abertura do Chamado (setup operacional)**  
* **Execução Operacional (fila de trabalho)**

Chamados **não entram automaticamente na fila operacional no momento da criação**.

## Contexto
Durante ajustes de layout e fluxo, foi identificado que:

* A tela de **decisão operacional** (bipagem e “configurar este item”) estava sendo exibida
  diretamente na **fila operacional**.
* Isso causava confusão de fluxo e a impressão de que itens já estavam “em execução”
  logo após a criação.
* A decisão de configuração (`deve_configurar`) pertence ao **step de abertura**,
  não à execução em fila.

O problema não era estético, mas **arquitetural**: ausência de um estado explícito
para o momento intermediário entre “criado” e “em execução”.

## Decisão Técnica
O ciclo de vida do Chamado passa a considerar explicitamente:

1) Abertura / Preparação
   * Criação do Chamado
   * Geração dos itens de execução
   * Decisão de configuração (`deve_configurar`)
   * Planejamento técnico (definição de IP obrigatório para itens configuráveis)

2) **Fila Operacional**
   * Apenas Chamados prontos para execução entram na fila
   * Chamados em abertura **não aparecem** na fila

A transição para a fila ocorre **explicitamente** após salvar os itens e decisões iniciais.

## Consequências

* Elimina mistura de responsabilidades entre setup e execução.
* Evita confusão de UX e estados “meio operacionais”.
* Garante que decisões iniciais não sejam tratadas como execução em andamento.
* Abre caminho para:
  * validações mais claras
  * métricas corretas
  * possíveis wizards de abertura no futuro
* Previne regressões semelhantes em alterações de layout/UI.

---

## Decisões pendentes de implementação

Esta seção lista decisões **já aceitas** mas ainda não completamente implementadas.

### 1) Transição explícita de estado após abertura
* Promover Chamado para estado operacional somente após salvar itens.
* Ajustar testes de fluxo completo.

### 2) Ajuste fino de UX no step de abertura
* Feedback visual claro de “setup” vs “execução”.
* Possível separação visual ou wizard (futuro).

---

# ADR — Nomes semânticos e separação de templates do fluxo de Chamado

## Data
2026-02-04

## Status
Aceito

## Decisão
Renomear templates e componentes do app `execucao` para nomes semânticos que expressem
claramente a responsabilidade de cada tela/fragmento, reduzindo risco de misturar
etapas do fluxo (abertura/planejamento vs execução operacional).

Além disso, separar explicitamente a renderização de itens em:
- planejamento (status `ABERTO`)
- operação (status `EM_EXECUCAO` e posteriores)

## Contexto
Após mudanças de layout, trechos de execução operacional foram inseridos em templates
de abertura/planejamento, causando confusão de fluxo e regressões.
O problema foi agravado por nomes genéricos (`chamado_detalhe`, `_itens_execucao`) que não
evidenciam o estágio do processo.

## Consequências
- Alteração de nomes de arquivos impacta includes e `template_name` nas views.
- A refatoração é mecânica e deve ser entregue em commit atômico (renome + ajustes).
- Reduz significativamente risco de regressões futuras por confusão de responsabilidade.