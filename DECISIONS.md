# DECISIONS — EXPANSÃO360

Este documento registra decisões técnicas e arquiteturais relevantes do projeto, com o objetivo de evitar ambiguidades, manter rastreabilidade e facilitar onboarding.

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
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> develop

* **Registry (Cadastro Mestre):** define “o que existe” e “como deve ser”
* **Operation (Execução de Campo):** registra “o que foi executado”, com rastreabilidade e histórico

**Contexto**  
Precisamos garantir governança sobre padrões e, ao mesmo tempo, registrar a execução real
em campo sem poluir o cadastro mestre e sem perder histórico.

<<<<<<< HEAD
=======

* **Registry (Cadastro Mestre):** define “o que existe” e “como deve ser”
* **Operation (Execução de Campo):** registra “o que foi executado”, com rastreabilidade e histórico

**Contexto**
Precisamos garantir governança sobre padrões e, ao mesmo tempo, registrar a execução real em campo sem poluir o cadastro mestre e sem perder histórico.

>>>>>>> origin/main
=======
>>>>>>> develop
**Consequências**

* Operation referencia Registry; Registry não depende de Operation.
* O domínio será desenhado para suportar auditoria e evolução segura.

---

## 2026-01-20 — Estratégia de trabalho: microtarefas + disciplina de versionamento

<<<<<<< HEAD
**Decisão**  
<<<<<<< HEAD
=======
**Decisão**
>>>>>>> origin/main
=======
>>>>>>> develop
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
<<<<<<< HEAD
<<<<<<< HEAD
=======

* `main` para estabilidade e releases
* `develop` para integração contínua
>>>>>>> develop

* `main` para estabilidade e releases
* `develop` para integração contínua
=======
>>>>>>> origin/main

* `main` para estabilidade e releases
* `develop` para integração contínua

**Contexto**
Separar o que está pronto para release do que está em desenvolvimento reduz risco operacional.

**Consequências**
<<<<<<< HEAD
<<<<<<< HEAD

* Mudanças entram via branches derivadas.
* `main` recebe apenas conteúdo estável.
=======

* Mudanças entram via branches derivadas.
* `main` recebe apenas conteúdo estável.

---

## 2026-01-20 — Repositório stack-agnostic (fase inicial)

**Decisão**
O projeto permanecerá neutro quanto a stack e framework no estágio inicial.

**Contexto**
Evitar acoplamento prematuro permite decisões baseadas em requisitos reais.

**Consequências**

* `.gitignore` genérico.
* Nenhuma estrutura de framework antecipada.
* Stack definida posteriormente via decisão formal.
>>>>>>> origin/main
=======

* Mudanças entram via branches derivadas.
* `main` recebe apenas conteúdo estável.
>>>>>>> develop

---

## 2026-01-21 — Stack Web definida: Django

**Decisão**
A camada Web será implementada em **Django**.

<<<<<<< HEAD
**Contexto**  
Após estabilização do core, era necessário um framework maduro para UI, ORM e velocidade de entrega.

**Consequências**
<<<<<<< HEAD

* Core permanece independente.
* Django atua como adapter.
* Models Django não concentram regras de negócio complexas.
=======
**Contexto**
Após estabilização do core e da CLI, era necessário um framework maduro para UI, autenticação, ORM e velocidade de entrega.

**Consequências**

* Core permanece independente.
* Django atua como adapter.
* Models Django não contêm regras de negócio (apenas validações e consistência de dados).

---

## 2026-01-21 — Nomenclatura em PT-BR no domínio

**Decisão**
O domínio e casos de uso utilizam nomenclatura em português (PT-BR).

**Contexto**
Reduzir carga cognitiva e aproximar o código do negócio real.

**Consequências**

* Core em PT-BR.
* Framework/infra seguem convenções originais.
* Glossário mantido para consistência.
>>>>>>> origin/main
=======

* Core permanece independente.
* Django atua como adapter.
* Models Django não concentram regras de negócio complexas.
>>>>>>> develop

---

## 2026-01-21 — Entidade operacional “Chamado”

**Decisão**
O termo **Chamado** substitui “Card” como entidade operacional.

<<<<<<< HEAD
**Contexto**  
“Card” é ambíguo e visual. “Chamado” representa melhor uma unidade operacional real.
<<<<<<< HEAD

**Consequências**

* Domínio, UI e testes utilizam “Chamado”.
* Histórico operacional preservado.
=======
**Contexto**
“Card” é ambíguo e visual. “Chamado” representa melhor uma unidade operacional.

**Consequências**

* Domínio, CLI e Web utilizam “Chamado”.
* Possíveis aliases temporários para compatibilidade (se necessário).
>>>>>>> origin/main

---

## 2026-02-03 — Configuração (ex.: IP) é decisão do Chamado, não do Kit
=======

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

---
# 2026-02-05 — Status EM_ABERTURA e promoção explícita para ABERTO

**Status:** Aceito

## Decisão
Introduzir o status **EM_ABERTURA** no ciclo de vida de `Chamado`, separando explicitamente:

- **Abertura (setup / planejamento)** → `EM_ABERTURA`
- **Fila operacional** → `ABERTO` em diante

## Contexto
A tela 2 (setup) ocorre imediatamente após o POST do formulário inicial, quando o chamado já existe e os itens foram gerados, mas ainda não deve:
- aparecer na fila operacional
- permitir execução (bipagem / gates / finalizar)

Sem um estado explícito, a UI e as regras ficam ambíguas e geram regressões.

## Regras de negócio
1) POST da Tela 1 cria o chamado com `status = EM_ABERTURA`
2) Ao clicar **Salvar setup**, o chamado é promovido para `status = ABERTO`
3) A fila operacional lista somente `ABERTO`, `EM_EXECUCAO`, `AGUARDANDO_*` (nunca `EM_ABERTURA`)

## Consequências
- Separa claramente setup vs execução
- Simplifica templates (modo setup vs modo execução)
- Simplifica regras e testes
- Evita chamados “meio operacionais” logo após a criação


---

## 2026-02-05 — Separação de template para Setup do Chamado

**Decisão**
Criar um template dedicado `execucao/chamado_setup.html` para o estágio de planejamento (status `ABERTO`),
mantendo `execucao/chamado_execucao.html` apenas para os estágios operacionais (`EM_EXECUCAO+`).

**Contexto**
O template “vivo” estava acumulando responsabilidades de planejamento e execução, exigindo muitos `ifs`
por status e aumentando risco de mistura de ações operacionais no estado `ABERTO`.

**Consequências**
- `ChamadoSetupView` passa a renderizar `chamado_setup.html`.
- `ChamadoDetailView` passa a ser acessível somente quando `status != ABERTO` (ou redireciona para setup).
- O contrato de templates fica mais simples e reduz branching no HTML.

---

# 2026-02-05 — Padronização de Layout, Componentes e Contratos de Templates (Execução & Cadastro)

**Status:** Aceito

## Decisão

Padronizar o layout, componentes visuais e contratos de templates dos módulos **Execução** e **Cadastro**, estabelecendo:

* Um **layout base único** (sidebar + topbar + mensagens)
* Componentes reutilizáveis bem definidos (`card`, `actions`, headers)
* Separação clara entre **listagem (fila)**, **detalhe**, **setup** e **execução**
* Um padrão visual consistente para tabelas, botões, badges e formulários

## Contexto

Antes desta mudança, o sistema apresentava:

* Variação visual significativa entre telas de Execução e Cadastro
* Templates com responsabilidades misturadas (setup + execução no mesmo HTML)
* Uso inconsistente de cores, botões e estruturas de página
* Dificuldade de evoluir UI sem medo de regressão
* Falta de um “contrato mental” claro sobre o papel de cada template

Além disso, o crescimento do fluxo de Execução exigia **clareza absoluta** entre:

* Planejamento
* Fila operacional
* Execução ativa
* Histórico

## Decisões Técnicas Aplicadas

### 1) Layout Base Unificado

* `base.html` passa a ser o ponto único de:

  * Sidebar
  * Topbar
  * Mensagens (`_messages`)
* Execução e Cadastro usam **o mesmo layout estrutural**, mudando apenas conteúdo.

### 2) Componentização Clara

Introdução e consolidação de componentes reutilizáveis:

* `_sidebar.html`
* `_topbar.html`
* `_messages.html`
* `_card.html`
* `_actions.html`

Esses componentes **não contêm regra de negócio**, apenas estrutura visual.

### 3) Execução — Contrato de Templates

* **Fila operacional** usa cards compactos (somente leitura + CTA)
* **Detalhe do chamado** contém:

  * Header informativo (`_header_chamado`)
  * Itens de execução
* Ações operacionais **não aparecem** na fila
* O template de execução deixa de ser “tudo-em-um”

Isso reduz `if status == ...` espalhados pelo HTML.

### 4) Execução — UX de Configuração

* Campos sensíveis (ex: IP) passam a:

  * Abrir em **modo leitura**
  * Ter edição **explícita** via ação do usuário
* Evita alteração acidental e melhora rastreabilidade

### 5) Cadastro — Padronização Visual

Listagens e formulários de:

* Lojas
* Categorias
* Equipamentos
* Kits
* Projetos
* Subprojetos

passam a seguir o mesmo padrão de:

* Header da página
* Card com tabela
* Botões primários (`slate`)
* Badges semânticos (`Sim/Não`, status)

### 6) CSS e Estáticos

* Confirmação explícita de carregamento de `ui.css`
* Uso consciente de CSS global (layout) vs CSS local (quando necessário)
* Evita duplicação e “CSS fantasma”

## Consequências

### Positivas

* UI previsível e consistente
* Templates mais simples e legíveis
* Redução de branching por status
* Facilidade para onboarding
* Base sólida para evolução (gates, finalização, auditoria)
* Menor risco de regressão visual

### Custos / Trade-offs

* Refatoração inicial extensa de templates
* Necessidade de disciplina para manter contratos
* Algumas telas antigas precisaram ser ajustadas para o novo padrão

## Status

Aceito ✅

(Implementado e validado em Codespaces e ambiente local)


---
# ADR — Fila de Chamados: Detalhes como Preview e Deprecação do DetailView

## Data
2026-02-05

## Decisão 1 — "Detalhes" na fila vira preview inline (accordion), sem nova página
### Contexto
Hoje o botão **Detalhes** abre uma `DetailView` ques. Porém ele leva para a mesma experiência do **Abrir**, gerando redundância e fricção na triagem da fila.

### Decisão
O botão **Detalhes** na fila será um **accordion inline** no card (preview simples).  
Inicialmente será um placeholder (“aqui vai ter detalhes”), sem regras operacionais.

### Consequências
- A fila fica mais rápida para triagem.
- Evita criar nova página e nova view desnecessárias.
- “Abrir” permanece como único fluxo para a tela operacional (execução).

---

## Decisão 2 — `ChamadoDetailView` deixa de ser o destino do botão "Detalhes" (deprecado)
### Contexto
O link atual de “Detalhes” aponta para uma `DetailView`, mas esse fluxo deixa de existir com o preview inline.

### Decisão
- O botão "Detalhes" **não** chama mais a `DetailView`.
- A `DetailView` poderá ser **mantida temporariamente** (compatibilidade/rotas antigas), porém deve:
  - (opção recomendada) **redirecionar** para a tela de execução (`ExecucaoView`) ou
  - (opção alternativa) exibir uma página realmente read-only futuramente (fora do escopo de hoje).

### Consequências
- Evita duplicidade de telas.
- Mantém retrocompatibilidade sem quebrar URLs antigas.
- Reduz manutenção e confusão para o usuário.

---

## Decisão 3 — Organização de JS por página: execução vs fila
### Contexto
Existe `execucao/js/chamado_detalhe.js` cuidando de UI helpers da tela de execução (progress bar e edição inline de IP).

### Decisão
- `chamado_detalhe.js` permanece **exclusivo da tela de execução** (`chamado_execucao.html`).
- Um novo JS será criado para a fila: `execucao/js/fila_operacional.js`, cuidando do accordion do preview.

### Consequências
- Evita "perder JS" em meio a muitos templates.
- Mantém cada comportamento no contexto correto (por página).
- Reforça a regra: **sem JS inline em templates** e scripts com `defer`.

---

## Status
Aceito


---

## 2026-02-05 — Renomeação da DetailView para Execução do Chamado
>>>>>>> develop

**Status:** Aceito

<<<<<<< HEAD
**Decisão**  
<<<<<<< HEAD
A necessidade de configuração operacional (ex.: exigir IP) é decidida na execução do **Chamado**
e não imposta pelo cadastro de Kit/KitItem.

**Contexto**  
O cadastro apenas sugere padrões; a obrigatoriedade varia conforme cenário real de execução.

**Consequências**

* Campo operacional `deve_configurar` pertence à execução.
* Validação exige IP **somente** quando `deve_configurar=True`.
* Cadastro não força configuração.
=======
**Decisão**
Equipamentos são classificados como:

* **Rastreáveis** (`tem_ativo=True`)
* **Contáveis** (`tem_ativo=False`)

**Contexto**
Nem todos os itens exigem ativo/número de série.

**Consequências**

* Execução valida campos conforme tipo.
* Relatórios diferenciam ativos e consumíveis.
>>>>>>> origin/main

---

## 2026-02-03 — Gate de NF e critérios de fechamento do Chamado

<<<<<<< HEAD
**Decisão**  
O Chamado só será liberado para NF quando todos os itens estiverem conferidos.
O fechamento exige NF e confirmação de coleta quando aplicável.

**Contexto**  
Processo real exige controle contábil e evidência mínima antes de encerramento.

**Consequências**

* Método `pode_liberar_nf()` no Chamado.
* `finalizar()` valida regras conforme tipo (ENVIO / RETORNO).
=======
**Decisão**
Adotar Tailwind via CDN e estrutura base de templates (`base`, `partials`, `components`).

**Contexto**
Padronizar UI desde o início sem custo de build frontend.

**Consequências**

* UI padronizada desde o início.
* Evita HTML duplicado e decisões visuais ad-hoc.
>>>>>>> origin/main

---

## 2026-02-04 — Ciclo de Vida do Chamado, Prioridade e Ticket Externo

<<<<<<< HEAD
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
=======
**Decisão**
A Web atua apenas como adapter (UI + persistência + orquestração), preservando regras de negócio fora da camada de entrega.

**Contexto**
Evitar migração de regras de negócio para a camada Web.

**Consequências**

* Core independente.
* CLI e Web compartilham domínio.
* Facilita API e mobile no futuro.
>>>>>>> origin/main

---

# 🆕 2026-02-04 — Separação entre Abertura do Chamado e Fila Operacional

<<<<<<< HEAD
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
=======
**Decisão**
Correções e retornos geram **novo Chamado**, nunca edição destrutiva.

**Contexto**
Chamados representam eventos operacionais e contábeis reais.

**Consequências**

* Histórico imutável.
* Retornos exigem desfecho explícito.
* Auditoria e contabilidade preservadas.
>>>>>>> origin/main

---

## Decisões pendentes de implementação

<<<<<<< HEAD
Esta seção lista decisões **já aceitas** mas ainda não completamente implementadas.

### 1) Transição explícita de estado após abertura
* Promover Chamado para estado operacional somente após salvar itens.
* Ajustar testes de fluxo completo.

### 2) Ajuste fino de UX no step de abertura
* Feedback visual claro de “setup” vs “execução”.
* Possível separação visual ou wizard (futuro).
=======
**Decisão**
Evidências são entidades próprias vinculadas a Chamados.

**Contexto**
NF, Carta de Conteúdo e documentos de exceção são parte do processo real.

**Consequências**

* Finalização pode exigir evidência.
* Auditoria fortalecida.
* Modelo extensível (fotos, assinaturas, etc.).
>>>>>>> origin/main

---

# ADR — Nomes semânticos e separação de templates do fluxo de Chamado

<<<<<<< HEAD
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

---
# ADR — 2026-02-05 — Status EM_ABERTURA e promoção explícita para ABERTO

**Status:** Aceito

## Decisão
Introduzir o status **EM_ABERTURA** no ciclo de vida de `Chamado`, separando explicitamente:

- **Abertura (setup / planejamento)** → `EM_ABERTURA`
- **Fila operacional** → `ABERTO` em diante

## Contexto
A tela 2 (setup) ocorre imediatamente após o POST do formulário inicial, quando o chamado já existe e os itens foram gerados, mas ainda não deve:
- aparecer na fila operacional
- permitir execução (bipagem / gates / finalizar)

Sem um estado explícito, a UI e as regras ficam ambíguas e geram regressões.

## Regras de negócio
1) POST da Tela 1 cria o chamado com `status = EM_ABERTURA`
2) Ao clicar **Salvar setup**, o chamado é promovido para `status = ABERTO`
3) A fila operacional lista somente `ABERTO`, `EM_EXECUCAO`, `AGUARDANDO_*` (nunca `EM_ABERTURA`)

## Consequências
- Separa claramente setup vs execução
- Simplifica templates (modo setup vs modo execução)
- Simplifica regras e testes
- Evita chamados “meio operacionais” logo após a criação


---

## 2026-02-05 — Separação de template para Setup do Chamado

**Decisão**
Criar um template dedicado `execucao/chamado_setup.html` para o estágio de planejamento (status `ABERTO`),
mantendo `execucao/chamado_execucao.html` apenas para os estágios operacionais (`EM_EXECUCAO+`).

**Contexto**
O template “vivo” estava acumulando responsabilidades de planejamento e execução, exigindo muitos `ifs`
por status e aumentando risco de mistura de ações operacionais no estado `ABERTO`.

**Consequências**
- `ChamadoSetupView` passa a renderizar `chamado_setup.html`.
- `ChamadoDetailView` passa a ser acessível somente quando `status != ABERTO` (ou redireciona para setup).
- O contrato de templates fica mais simples e reduz branching no HTML.
=======
**Decisão**
Adoção de **Capability-Based Access Control** na camada Web.

**Contexto**
Precisamos restringir ações sensíveis sem acoplar IAM ao domínio.

**Consequências**

* Backend valida permissões.
* Templates apenas refletem.
* Core permanece permission-agnostic.

---

## 2026-01-24 — Padronização de CBVs + `CapabilityRequiredMixin`

**Status:** Aceito

**Decisão**

* Migrar views críticas para CBVs.
* Centralizar autorização em `CapabilityRequiredMixin`.

**Contexto**
Sprint 3 — Execução / Fluxo inverso / IAM.

**Consequências**

* Menos repetição.
* Padrão consistente.
* Migração incremental segura.

---

## 2026-01-24 — Abertura de Chamado via UI (snapshot operacional)

**Decisão**
Chamados podem ser abertos via UI, gerando automaticamente Itens de Execução a partir do Kit (snapshot operacional).

**Contexto**
Necessidade de testes end-to-end e uso real do sistema.

**Consequências**

* Chamado nasce do Registry.
* Itens de execução são tratados como imutáveis conceitualmente (histórico).
* Planejamento e execução ficam claramente separados.

---

## 2026-01-25 — Introdução de Subprojetos no Registry

**Decisão**
Introduzir a entidade **Subprojeto** no **Registry (Cadastro Mestre)** como recorte organizacional quando aplicável.

**Contexto**
Projetos reais de expansão exigem segmentação operacional por linhas de entrega.

**Consequências**

* Subprojeto pertence ao Registry.
* Chamados referenciam Subprojeto quando existir.
* Subprojetos não são deletados destrutivamente (preservar histórico).

---

## 2026-02-02 — Mapeamento operacional: “Filial” como “Java” no Cadastro de Lojas

**Decisão**
Exibir **Filial** como **Java** e **Nome Filial** como **Nome loja** na UI, mantendo compatibilidade com base externa.

**Contexto**
Alinhar o sistema à linguagem operacional do dia a dia sem quebrar integrações.

**Consequências**

* Importador mapeia campos explicitamente.
* UI usa labels operacionais.
* Testes cobrem o mapeamento.

---

## 2026-02-02 — Padronização de Logomarca no Cadastro de Lojas

**Decisão**
Padronizar o campo **Logomarca**:

* Normalizar para maiúsculo.
* Preferir dropdown no cadastro manual.

**Contexto**
Evitar divergências (RAIA/raia/RaIa).

**Consequências**

* Menos inconsistência.
* UI mais segura.
* Testes de normalização.

---

## 2026-02-02 — Refinamento do Cadastro de Equipamentos (Registry)

**Decisão**
Equipamentos são tratados como entidade de **Registry**, focados em padronização e reutilização operacional.

**Contexto**
CRUD inicial não refletia uso real nem validações necessárias.

**Consequências**

* Ajustes em model, form, testes e UI.
* Possível migração de dados.
* Reuso do padrão aplicado em Lojas.

---

## 2026-02-02 — Padronização da estrutura de testes por camadas

**Decisão**
Organizar testes por camadas arquiteturais (Domain, Usecases, Interfaces).

**Contexto**
A organização anterior dificultava leitura, manutenção e escalabilidade.

**Consequências**

* Estrutura clara por responsabilidade.
* Facilita onboarding.
* Impõe disciplina para novos testes.

---

## 2026-02-03 — Código de Equipamento gerado automaticamente

**Decisão**
O campo `Equipamento.codigo` passa a ser gerado automaticamente, único, normalizado e imutável.

**Contexto**
Evitar inconsistência e erro humano em identificadores usados no dia a dia.

**Consequências**

* Lógica no model.
* Campo oculto/derivado na UI quando aplicável.
* Testes de geração, colisão e imutabilidade.

---

## 2026-02-03 — Tipos de Equipamento como cadastro mestre por categoria

**Decisão**
Criar `TipoEquipamento` como entidade de Registry vinculada à Categoria, substituindo texto livre em itens do Kit.

**Contexto**
Texto livre gera inconsistência e dificulta histórico.

**Consequências**

* Novo model e migração.
* Forms e testes atualizados.
* Integridade referencial garantida.

---

## 2026-02-03 — Padronização de códigos (internos vs externos)

**Status:** Proposto

**Decisão**
Diferenciar:

* **Códigos externos** (ex.: Loja/Java) — manuais/importados.
* **Códigos internos** (ex.: Equipamento, TipoEquipamento) — automáticos.

**Contexto**
Evitar confusão entre identificadores operacionais e internos do Registry.

**Consequências**

* UI trata códigos conforme tipo.
* Testes específicos por categoria.
* Maior clareza e segurança para integrações.

---

## 2026-02-03 — Cadastro mestre de Kit e KitItem (Registry)

**Decisão**
Adicionar entidades de cadastro mestre:

* **Kit:** conjunto padronizado usado em fluxos operacionais.
* **KitItem:** itens que compõem um Kit, com quantidade e ordenação.

**Contexto**
Precisamos representar kits padronizados para apoiar o fluxo de chamados, garantindo governança e reutilização. Como é informação relativamente estável e de referência, pertence ao **Registry**.

**Consequências**

* Operation poderá referenciar Kit (no futuro) sem criar dependência inversa.
* Validamos integridade de KitItem (quantidade mínima, ordenação).
* CRUD exposto via Django (camada de entrega), mantendo regras de negócio fora de views.

---

## 2026-02-03 — Configuração (ex.: IP) é decisão do Chamado, não do Kit

**Status:** Aceito (ajuste de entendimento)

**Decisão**
A necessidade de configuração operacional (ex.: exigir IP) é decidida na execução do **Chamado** e não imposta pelo cadastro de Kit/KitItem.

**Contexto**
No cadastro, um kit pode sugerir que um item costuma precisar de configuração, mas a obrigatoriedade varia por cenário/loja/orientação e deve ser avaliada no momento da execução.

**Consequências**

* Campo operacional `deve_configurar` vive na execução.
* Campos operacionais como `ip` ficam na execução.
* O cadastro pode manter campo de sugestão (`sugere_configuracao`) sem caráter obrigatório.
* A validação de finalização exige configuração somente quando `deve_configurar=True`.

---

## 2026-02-03 — Gate de NF e critérios de fechamento do Chamado

**Decisão**
O Chamado só será liberado para NF quando todos os itens rastreáveis estiverem bipados e todos os itens contáveis confirmados. O fechamento do Chamado exige NF e confirmação de coleta quando aplicável.

**Contexto**
A emissão da NF de saída depende da bipagem completa do kit e da conferência dos itens. Além disso, o Chamado não pode ser encerrado sem evidências mínimas do processo.

**Consequências**

* Implementar método/flag de liberação para NF no `Chamado`.
* Campos de NF e controle de coleta conforme fluxo.
* `finalizar()` valida pré-condições do status (ex.: ENVIO).

---

## 2026-02-03 — `InstalacaoItem` referencia `TipoEquipamento` via FK

**Decisão**
Alterar `InstalacaoItem.tipo` de string para `ForeignKey` para `TipoEquipamento`.

**Contexto**
Itens de cadastro e execução precisam referenciar o mesmo cadastro mestre para consistência, filtros e regras estáveis.

**Consequências**

* Migração de schema e ajuste na criação de itens.
* Ajuste de telas/serialização onde `tipo` era tratado como string.

---

## 2026-02-04 — Tipos de equipamento só existem no contexto de uma Categoria

**Status:** Aceito

**Decisão**
O cadastro de **TipoEquipamento** deve acontecer exclusivamente **dentro do fluxo de Categoria** (inline no update da Categoria). Não haverá criação “solta” de Tipo sem Categoria.

**Contexto**
Tipos sem Categoria (ou categorias sem tipos mínimos) geram selects vazios e inconsistência na abertura de Chamados. Como `TipoEquipamento` é um cadastro mestre, ele deve ser governado por Categoria para garantir consistência do Registry.

**Consequências**

* UI: fluxo padrão é **criar Categoria → cadastrar Tipos** (na mesma tela).
* Evita cadastro de Tipo sem Categoria e reduz “tipos vazios” no Chamado.
* Testes de view devem cobrir: atualização de Categoria com formset de Tipos e validações mínimas.
* Qualquer shortcut (quick-create) deve garantir Categoria persistida antes de permitir Tipos.

---

## Decisões pendentes de implementação

Esta seção lista decisões **já registradas** neste documento que ainda não foram totalmente implementadas no código. O objetivo é dar visibilidade e evitar esquecimento, sem criar novas regras.

### 1) Padronização de códigos (internos vs externos)

* **Referência:** 2026-02-03 — Padronização de códigos (internos vs externos)
* **Status atual:** Proposto
* **Pendente:**

  * Consolidar comportamento na UI (inputs, readonly, hints)
  * Garantir cobertura de testes para cada tipo de código

### 2) Tipos de equipamento governados por Categoria

* **Referência:** 2026-02-04 — Tipos de equipamento só existem no contexto de uma Categoria
* **Status atual:** Aceito
* **Pendente:**

  * Garantir que não exista fluxo de criação de Tipo fora da Categoria
  * Adicionar validação mínima (Categoria com ao menos 1 Tipo ativo, quando aplicável)
  * Testes de view cobrindo atualização de Categoria + Tipos

### 3) Consolidação de itens duplicados na edição de Kit (UX)

* **Referência:** Discussão técnica (ainda sem ADR)
* **Status atual:** Em avaliação
* **Pendente:**

  * Decidir entre bloquear duplicidade ou fazer merge automático de quantidades
  * Caso aceito, registrar ADR específica
  * Implementar testes de formset para edição de Kit

  
---
## 2026-02-04 — Adoção de testes JavaScript com Jest

**Decisão**  
Adotar Jest + jsdom para testes de JavaScript no frontend.

**Contexto**  
Lógicas críticas em formulários dinâmicos não podem ser validadas apenas
por testes backend.

**Consequências**  
- Introdução de Node/npm como dependência de desenvolvimento
- Testes JS isolados da stack Python

---
## 2026-02-04 — Testes de JavaScript com Jest

**Decisão**
Adotar Jest + jsdom para testar JS puro do frontend (formsets dinâmicos).

**Contexto**
O bug do “tipo vazio” em linhas adicionadas dinamicamente não era coberto por testes backend.

**Consequências**
- Node/npm passam a ser dependência de desenvolvimento
- Testes JS ficam próximos aos arquivos estáticos do app
- Makefile integra `pytest` + `jest`
>>>>>>> origin/main
=======
A view anteriormente chamada `ChamadoDetailView` foi renomeada para `ChamadoExecucaoView`.

**Contexto**  
A view não representava uma tela apenas de leitura, mas sim a execução operacional do chamado, concentrando regras, progresso, evidências e gates.

**Consequências**
- O nome da classe passa a refletir sua responsabilidade real.
- A URL e o `url name` são mantidos para compatibilidade.
- O botão “Detalhes” da fila deixa de depender de view e passa a ser um preview inline.

---

## 2026-02-05 — Cor do Projeto no Cadastro para identidade visual na Fila Operacional

**Decisão**
Adicionar ao cadastro de `Projeto` um campo `cor_slug` (paleta fechada). A fila operacional usa essa cor para renderizar uma faixa no card do chamado.

**Contexto**
Mapear cor por código no frontend não escala e deixa projetos novos sem cor, degradando a consistência visual.

**Consequências**
- Migration em `cadastro`.
- Form de Projeto expõe seleção de cor (paleta limitada).
- `execucao` apenas consome `projeto.cor_slug` para UI.
<!-- merge resolved during v0.3.6 -->
