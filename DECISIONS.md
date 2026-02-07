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

## 2026-01-20 — Repositório stack-agnostic (fase inicial)

**Decisão**  
O projeto permanecerá neutro quanto a stack e framework no estágio inicial.

**Contexto**  
Evitar acoplamento prematuro permite decisões baseadas em requisitos reais.

**Consequências**
* `.gitignore` genérico.
* Nenhuma estrutura de framework antecipada.
* Stack definida posteriormente via decisão formal.

---

## 2026-01-21 — Stack Web definida: Django

**Decisão**  
A camada Web será implementada em **Django**.

**Contexto**  
Após estabilização do core, era necessário um framework maduro para UI, autenticação, ORM e velocidade de entrega.

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

---

## 2026-01-21 — Entidade operacional “Chamado”

**Decisão**  
O termo **Chamado** substitui “Card” como entidade operacional.

**Contexto**  
“Card” é ambíguo e visual. “Chamado” representa melhor uma unidade operacional.

**Consequências**
* Domínio, CLI e Web utilizam “Chamado”.
* Possíveis aliases temporários para compatibilidade (se necessário).

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

## 2026-01-24 — Adoção de Capability-Based Access Control (Web)

**Decisão**  
Adoção de **Capability-Based Access Control** na camada Web.

**Contexto**  
Precisamos restringir ações sensíveis sem acoplar IAM ao domínio.

**Consequências**
* Backend valida permissões.
* Templates apenas refletem.
* Core permanece permission-agnostic.

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

## 2026-02-03 — Equipamentos: rastreáveis vs contáveis

**Decisão**  
Equipamentos são classificados como:

* **Rastreáveis** (`tem_ativo=True`)
* **Contáveis** (`tem_ativo=False`)

**Contexto**  
Nem todos os itens exigem ativo/número de série.

**Consequências**
* Execução valida campos conforme tipo.
* Relatórios diferenciam ativos e consumíveis.

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
* A validação exige IP somente quando `deve_configurar=True`.

---

## 2026-02-03 — Gate de NF e critérios de fechamento do Chamado

**Decisão**  
O Chamado só será liberado para NF quando todos os itens rastreáveis estiverem bipados e todos os itens contáveis confirmados. O fechamento do Chamado exige NF e confirmação de coleta quando aplicável.

**Contexto**  
A emissão da NF de saída depende da bipagem completa do kit e da conferência dos itens. Além disso, o Chamado não pode ser encerrado sem evidências mínimas do processo.

**Consequências**
* Método `pode_liberar_nf()` no Chamado.
* Campos de NF e controle de coleta conforme fluxo.
* `finalizar()` valida pré-condições do status (ex.: ENVIO / RETORNO).

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
* Testes cobrem atualização de Categoria com formset de Tipos e validações mínimas.
* Qualquer quick-create deve garantir Categoria persistida antes de permitir Tipos.

---

## 2026-02-04 — Adoção de Tailwind via CDN

**Decisão**  
Adotar Tailwind via CDN e estrutura base de templates (`base`, `partials`, `components`).

**Contexto**  
Padronizar UI desde o início sem custo de build frontend.

**Consequências**
* UI padronizada desde o início.
* Evita HTML duplicado e decisões visuais ad-hoc.

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

## 2026-02-04 — Web como adapter (sem regras de negócio)

**Decisão**  
A Web atua apenas como adapter (UI + persistência + orquestração), preservando regras de negócio fora da camada de entrega.

**Contexto**  
Evitar migração de regras de negócio para a camada Web.

**Consequências**
* Core independente.
* CLI e Web compartilham domínio.
* Facilita API e mobile no futuro.

---

## 2026-02-04 — Evidências como entidades próprias

**Decisão**  
Evidências são entidades próprias vinculadas a Chamados.

**Contexto**  
NF, Carta de Conteúdo e documentos de exceção são parte do processo real.

**Consequências**
* Finalização pode exigir evidência.
* Auditoria fortalecida.
* Modelo extensível (fotos, assinaturas, etc.).

---

## 2026-02-04 — Correções e retornos geram novo Chamado (imutabilidade operacional)

**Decisão**  
Correções e retornos geram **novo Chamado**, nunca edição destrutiva.

**Contexto**  
Chamados representam eventos operacionais e contábeis reais.

**Consequências**
* Histórico imutável.
* Retornos exigem desfecho explícito.
* Auditoria e contabilidade preservadas.

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

* A tela de **decisão operacional** (bipagem e “configurar este item”) estava sendo exibida diretamente na **fila operacional**.
* Isso causava confusão de fluxo e a impressão de que itens já estavam “em execução” logo após a criação.
* A decisão de configuração (`deve_configurar`) pertence ao **step de abertura**, não à execução em fila.

O problema não era estético, mas **arquitetural**: ausência de um estado explícito para o momento intermediário entre “criado” e “em execução”.

## Decisão Técnica
O ciclo de vida do Chamado passa a considerar explicitamente:

1) **Abertura / Preparação**
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
* Abre caminho para validações e métricas corretas.
* Previne regressões semelhantes em alterações de layout/UI.

---

# ADR — Nomes semânticos e separação de templates do fluxo de Chamado

## Data
2026-02-04

## Status
Aceito

## Decisão
Renomear templates e componentes do app `execucao` para nomes semânticos que expressem claramente a responsabilidade de cada tela/fragmento, reduzindo risco de misturar etapas do fluxo (abertura/planejamento vs execução operacional).

Separar explicitamente a renderização de itens em:
- planejamento (status `ABERTO`)
- operação (status `EM_EXECUCAO` e posteriores)

## Contexto
Após mudanças de layout, trechos de execução operacional foram inseridos em templates de abertura/planejamento, causando confusão de fluxo e regressões. O problema foi agravado por nomes genéricos que não evidenciam o estágio do processo.

## Consequências
- Alteração de nomes de arquivos impacta includes e `template_name` nas views.
- A refatoração é mecânica e deve ser entregue em commit atômico (renome + ajustes).
- Reduz significativamente risco de regressões futuras por confusão de responsabilidade.

---

## 2026-02-05 — Status EM_ABERTURA e promoção explícita para ABERTO

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
Criar um template dedicado `execucao/chamado_setup.html` para o estágio de planejamento,
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
Antes desta mudança, o sistema apresentava variação visual significativa entre telas e templates com responsabilidades misturadas, aumentando risco de regressão e dificultando evolução.

## Consequências
### Positivas
* UI previsível e consistente
* Templates mais simples e legíveis
* Redução de branching por status
* Base sólida para evolução

### Custos / Trade-offs
* Refatoração inicial extensa de templates
* Necessidade de disciplina para manter contratos

---

# ADR — Fila de Chamados: Detalhes como Preview e Deprecação do DetailView

## Data
2026-02-05

## Decisão 1 — "Detalhes" na fila vira preview inline (accordion), sem nova página
### Contexto
O botão **Detalhes** abria uma `DetailView` redundante com **Abrir**, gerando fricção na triagem.

### Decisão
O botão **Detalhes** na fila será um **accordion inline** no card (preview simples).

### Consequências
- A fila fica mais rápida para triagem.
- Evita criar nova página e nova view desnecessárias.
- “Abrir” permanece como único fluxo para a tela operacional (execução).

---

## Decisão 2 — `ChamadoDetailView` deixa de ser o destino do botão "Detalhes" (deprecado)
### Decisão
- O botão "Detalhes" **não** chama mais a `DetailView`.
- A `DetailView` pode ser mantida temporariamente, mas deve redirecionar para a tela de execução.

---

## Decisão 3 — Organização de JS por página: execução vs fila
### Decisão
- JS da execução permanece exclusivo da tela de execução.
- Criar JS da fila para o preview inline.

---

## Status
Aceito

---

## 2026-02-05 — Renomeação da DetailView para Execução do Chamado

**Decisão**  
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

---

## 2026-02-06 — Modularização de templatetags por tema de UI (cores e urgência)

**Decisão**  
Separar os templatetags de UI do app `execucao` em módulos semânticos por responsabilidade
(ex.: cores de projeto, urgência visual), mantendo `execucao_ui.py` como fachada de compatibilidade.

**Contexto**  
O arquivo `execucao_ui.py` começou com uma única responsabilidade (cores do projeto), mas a UI
da execução está evoluindo e novas regras visuais tendem a crescer. Para evitar um “arquivo deus”
e manter o projeto saudável, optamos por separar por tema.

**Consequências**
- Novos templatetags devem ser criados em módulos dedicados.
- `execucao_ui.py` permanece como facade/reexport para não quebrar templates existentes.
- Testes passam a ser organizados por tema.

---

## 2026-02-06 — Cards-resumo interativos na Fila Operacional (prioridade)

**Status:** Aceito

**Decisão**  
Adicionar um header na tela de **Fila Operacional** contendo **cards-resumo clicáveis** para:
- Total de chamados na fila
- Quantidade por prioridade (Crítico/Alto/Médio/Baixo)

Os cards funcionam também como **filtro rápido** via querystring (`?prio=CRITICO|ALTO|MEDIO|BAIXO`).

**Contexto**  
A fila operacional precisa oferecer leitura imediata da carga de trabalho e reduzir o custo de “caçar” chamados.
A UI já é baseada em cards e ações rápidas; faltava uma visão agregada e um mecanismo direto de filtragem.

**Consequências**
- A view da fila expõe contadores agregados (`counts`) e o filtro atual (`prio_selected`).
- Filtragem stateless (URL), facilitando compartilhamento e testes.
- Template só renderiza; regra de filtro/agregações ficam na view.

---

## 2026-02-06 — Filtro por projeto na Fila via projeto_id (temporário)

**Status:** Aceito

### Decisão
Implementar o filtro de projeto na Fila Operacional via querystring usando **PK do Projeto**:
- `?projeto=<id>`

Mantendo compatibilidade com o filtro por prioridade (`?prio=`) e abordagem stateless (URL).

### Contexto
O modelo `Projeto` não possui o campo `slug` no estado atual do schema, e o projeto já utiliza `?projeto=<id>` em endpoints auxiliares (ex.: carregamento de subprojetos). Para entregar valor incremental sem migrações, adotamos `id` como identificador.

### Consequências
- A view expõe `projects` com `{id, nome, count, url, active, projeto}` para UI.
- O filtro combina `prio + projeto` sem estado de sessão.
- Evolução futura: adicionar `slug` em `Projeto` e migrar `?projeto=<slug>` (nova ADR quando ocorrer).

---

## Decisões pendentes de implementação

Esta seção lista decisões **já registradas** neste documento que ainda não foram totalmente implementadas no código.

### 1) Padronização de códigos (internos vs externos)
* **Referência:** 2026-02-03 — Padronização de códigos (internos vs externos)
* **Status atual:** Proposto

### 2) Tipos de equipamento governados por Categoria
* **Referência:** 2026-02-04 — Tipos de equipamento só existem no contexto de uma Categoria
* **Status atual:** Aceito

### 3) Consolidação de itens duplicados na edição de Kit (UX)
* **Status atual:** Em avaliação
* **Pendente:** Caso aceito, registrar ADR específica.

---

## 2026-02-04 — Testes de JavaScript com Jest

**Decisão**
Adotar Jest + jsdom para testar JS puro do frontend (formsets dinâmicos).

**Contexto**
Bugs em linhas adicionadas dinamicamente não são cobertos por testes backend.

**Consequências**
- Node/npm passam a ser dependência de desenvolvimento.
- Testes JS ficam próximos aos arquivos estáticos do app.
- Integração `pytest` + `jest` no fluxo de desenvolvimento (quando aplicável).
<<<<<<< HEAD

---

# 2026-02-07 — Padronização de Chamado Externo

**Status:** Aceito

## Decisão
Padronizar a exibição e uso de identificadores externos de chamados
exclusivamente através dos campos:

- `ticket_externo_sistema`
- `ticket_externo_id`

## Contexto
O ServiceNow será descontinuado e a aplicação já possuía campos genéricos
para integração externa. A UI ainda referenciava um campo específico,
gerando confusão e ocultando dados válidos.

## Consequências
- UI passa a exibir "Chamado Externo" no formato `<sistema>: <id>`
- Filtros e buscas passam a funcionar corretamente
- `servicenow_numero` foi removido do modelo e do banco

---

# 2026-02-07 — Unicidade global do ticket externo

**Status:** Aceito

## Decisão
Garantir que `ticket_externo_id` seja único globalmente em `Chamado`, independentemente de `ticket_externo_sistema`.
A restrição aplica-se apenas quando `ticket_externo_id` estiver preenchido.

## Contexto
Apesar de existirem múltiplos sistemas externos, o identificador do ticket é tratado como único no ecossistema.
Permitir repetição por sistema poderia gerar ambiguidade na busca, na auditoria e em integrações.

## Consequências
- Adição de `UniqueConstraint` condicional em `ticket_externo_id`.
- Testes atualizados para refletir unicidade global.
- `ticket_externo_sistema` permanece como metadado informativo.


---

## 2026-02-07 — Criação do app `rede` para governança e validação de regras de rede

**Status:** Proposto

### Decisão
Criar o app Django `rede` para centralizar regras de rede (legado e segmentado), com foco inicial em:
- Classificação e validação de IP por tipo de equipamento
- Suporte a múltiplos perfis (ex.: LEGACY_FLAT_2023, RD_SEGMENTADO_2024/2025)
- Uso de `bandeira` + `cod_historico` como base para cálculo/validação de prefixo de rede

### Contexto
Hoje existe preenchimento manual de IPs em processos de abertura/rollout/adição. A validação ocorre de forma manual
(e em planilhas), aumentando o risco de erro. As regras de rede são simples, mas dependem de memória e conferência humana.

### Consequências
- Regras deixam de ficar dispersas (HTML/planilha/memória) e passam a existir como domínio versionado no sistema.
- O sistema passa a alertar inconsistências (ex.: “IP típico de TC preenchido em PDV”).
- A transição para fila operacional poderá exigir dados validados (reduzindo erro a ~0 na entrada da fila).

---
## 2026-02-07 — Integração futura entre Cadastro de Equipamentos e Regras de Rede

**Decisão**  
Planejar a integração entre o cadastro de tipos de equipamento e as regras de rede,
introduzindo futuramente uma **FK opcional** de `TipoEquipamento` para
`RegraRedeEquipamento`.

Além disso, **não modelar variações como tipos distintos** (ex.: `PDV1`, `PDV2`);
a diferenciação por índice/unidade será responsabilidade da **instância em execução**,
não do cadastro mestre.

**Contexto**  
As regras de IP variam por perfil de rede e tipo de equipamento, mas o mesmo tipo
(PDV, TC, etc.) pode possuir múltiplas instâncias em campo. Criar tipos artificiais
(`PDV1`, `PDV2`) gera explosão de cadastro, ambiguidade e acoplamento indevido
entre planejamento e execução.

**Consequências**  
- `TipoEquipamento` poderá (no futuro) referenciar `RegraRedeEquipamento`,
  mas a FK será **opcional** (permite cadastro neutro).
- O índice do equipamento (ex.: PDV #1, #2, #3) será tratado **na execução**,
  não no cadastro.
- Validações de IP poderão evoluir de WARN para ERROR conforme maturidade
  do fluxo e aderência do cadastro.


---

## 2026-02-07 — Grupos de Rede descrevem o papel completo na rede

**Status:** Aceito

### Decisão

A entidade atualmente representada como `RegraRedeEquipamento` passa a ser entendida conceitualmente como um **Grupo de Rede**, responsável por descrever **o papel completo de um conjunto de equipamentos na rede**, e não apenas a atribuição de IP.

Cada Grupo de Rede passa a definir, de forma explícita:

* Política de IP (offset fixo, sequencial ou faixa)
* Máscara de rede
* Gateway
* Padrão de hostname

A regra continua sendo **de domínio**, não de instância. A numeração ou indexação de equipamentos (ex.: `PDV1`, `TC3`) pertence exclusivamente à camada de execução e não ao cadastro ou às regras de rede.

---

### Contexto

Na prática operacional, a maioria dos erros de rede não ocorre por IP incorreto, mas por inconsistências associadas, tais como:

* IP correto com máscara incorreta
* IP correto com gateway incorreto
* Hostname fora do padrão esperado (impactando DNS, monitoramento e automação)

O modelo anterior tratava regras de rede como simples políticas de IP, o que exigia conhecimento implícito para completar corretamente a configuração de um equipamento. Isso dificultava validação automática, padronização entre lojas e evolução do domínio.

Além disso, a expansão do domínio de redes no Ciclo 2 exige uma base conceitual que permita evoluir validações futuras sem acoplamento à execução ou à UI.

---

### Consequências

* `RegraRedeEquipamento` evolui conceitualmente para representar um **Grupo de Rede**, descrevendo o papel completo na rede.
* As regras passam a permitir validações multidimensionais (IP, máscara, gateway e hostname), sem conhecimento da instância física do equipamento.
* A consistência entre lojas e perfis de rede (LEGACY vs SEGMENTADO) torna-se explícita e validável.
* O domínio passa a servir também como **documentação viva da topologia de rede**.
* Esta decisão cria a base para automação futura, sem introduzir implementação prematura.

---

### Observações de escopo

Esta decisão **não** inclui:

* Criação de instâncias de equipamentos
* Automação de aplicação de configurações de rede
* UI, fila ou workflow operacional
* Bloqueios de execução

Esses pontos permanecem fora de escopo e serão tratados em ciclos posteriores, quando o domínio e os dados estiverem estabilizados.

---

# ADR — Grupos de Rede definem IP, máscara, gateway e hostname

---

## Data

2026-02-07

---

## Decisão

Os **Grupos de Rede** passam a ser responsáveis por definir, de forma explícita e documentada:

* política e regra de **IP**
* **máscara** de rede
* **gateway**
* **hostname pattern** esperado

Esses elementos compõem o **contrato do grupo**, e não devem ser tratados de forma isolada ou implícita.

---

## Contexto

Historicamente, erros operacionais de rede não se limitam à escolha do IP.
Problemas recorrentes incluem:

* uso de máscara incorreta
* gateway divergente do padrão esperado
* hostname fora do padrão operacional

Tratar apenas o IP como regra de validação é insuficiente e deixa lacunas
que não podem ser detectadas automaticamente.

Para reduzir erro humano e aumentar previsibilidade, o domínio precisa
conhecer **toda a configuração mínima de rede esperada**, e não apenas o endereço IP.

---

## Consequências

* Grupos de rede tornam-se a **fonte de verdade** para configuração lógica de rede.
* Validações futuras poderão abranger IP, máscara, gateway e hostname.
* Evita regressões conceituais onde apenas IP é considerado regra de rede.
* Facilita automação, auditoria e testes de conformidade.

---

## Referência

O grupo **RETAGUARDA_LOJA** é o **primeiro exemplo oficial** que aplica este contrato completo,
servindo como template para todos os grupos futuros.

---

## Status

Aceito



---

# ADR — Grupos de Rede definem IP, máscara, gateway e hostname

---

## Data

2026-02-07

---

## Decisão

Os **Grupos de Rede** passam a ser responsáveis por definir, de forma explícita e documentada:

* política e regra de **IP**
* **máscara** de rede
* **gateway**
* **hostname pattern** esperado

Esses elementos compõem o **contrato do grupo**, e não devem ser tratados de forma isolada ou implícita.

---

## Contexto

Historicamente, erros operacionais de rede não se limitam à escolha do IP.
Problemas recorrentes incluem:

* uso de máscara incorreta
* gateway divergente do padrão esperado
* hostname fora do padrão operacional

Tratar apenas o IP como regra de validação é insuficiente e deixa lacunas
que não podem ser detectadas automaticamente.

Para reduzir erro humano e aumentar previsibilidade, o domínio precisa
conhecer **toda a configuração mínima de rede esperada**, e não apenas o endereço IP.

---

## Consequências

* Grupos de rede tornam-se a **fonte de verdade** para configuração lógica de rede.
* Validações futuras poderão abranger IP, máscara, gateway e hostname.
* Evita regressões conceituais onde apenas IP é considerado regra de rede.
* Facilita automação, auditoria e testes de conformidade.

---

## Referência

O grupo **RETAGUARDA_LOJA** é o **primeiro exemplo oficial** que aplica este contrato completo,
servindo como template para todos os grupos futuros.

---

## Status

* **RETAGUARDA_LOJA**: Grupo fechado e oficial
* **Uso**: Template obrigatório para grupos futuros

---

## Backlog de Testes — RETAGUARDA_LOJA (Contrato Vivo)

Esta seção define a **matriz de cenários de teste** do grupo RETAGUARDA_LOJA.

Os testes **não são implementados neste ciclo**; o objetivo é garantir que o contrato
esteja explícito, testável e alinhado antes de qualquer código.

---

### 1. Regras de IP — Banco12

**Cenários esperados:**

* Aceita IP com **offset .12** dentro do bloco do grupo

**Cenários inválidos:**

* Rejeita offset pertencente a outros itens do grupo (ex.: Gerência, PSB, Farma)
* Rejeita offsets típicos de **TC/PDV** (faixa operacional)

---

### 2. Regras de IP — Gerência / PSB / Farma

**Cenários esperados:**

* Aceitam apenas seus **offsets fixos definidos**

**Cenários inválidos:**

* Rejeitam qualquer IP dentro de **faixa de TC**
* Rejeitam offsets não documentados no contrato do grupo

---

### 3. Máscara e Gateway (por perfil)

**Cenários esperados (quando implementado):**

* Valida máscara correta conforme o perfil de rede:

  * RD_SEGMENTADO_2024/2025 → /27
  * LEGACY_FLAT_2023 → /24
* Valida gateway conforme offset esperado do perfil

**Cenários inválidos:**

* Máscara divergente do perfil aplicado
* Gateway fora do padrão definido para o perfil

---

### 4. Hostname Pattern

**Cenários esperados (quando implementado):**

* Hostname segue o padrão documentado por item

**Cenários inválidos:**

* Hostname fora do pattern
* Hostname válido para outro item do grupo
* Hostname válido para outro grupo

---

### Diretriz de Evolução

* Cada cenário acima deve se tornar **teste automatizado** quando a validação for implementada.
* Inclusão de novos cenários exige atualização deste backlog.
* O backlog de testes é parte do **contrato vivo** do grupo.


---


# ADR — Grupos de Rede definem IP, máscara, gateway e hostname

---

## Data

2026-02-07

---

## Decisão

Os **Grupos de Rede** passam a ser responsáveis por definir, de forma explícita e documentada:

* política e regra de **IP**
* **máscara** de rede
* **gateway**
* **hostname pattern** esperado

Esses elementos compõem o **contrato do grupo**, e não devem ser tratados de forma isolada ou implícita.

---

## Contexto

Historicamente, erros operacionais de rede não se limitam à escolha do IP.
Problemas recorrentes incluem:

* uso de máscara incorreta
* gateway divergente do padrão esperado
* hostname fora do padrão operacional

Tratar apenas o IP como regra de validação é insuficiente e deixa lacunas
que não podem ser detectadas automaticamente.

Para reduzir erro humano e aumentar previsibilidade, o domínio precisa
conhecer **toda a configuração mínima de rede esperada**, e não apenas o endereço IP.

---

## Consequências

* Grupos de rede tornam-se a **fonte de verdade** para configuração lógica de rede.
* Validações futuras poderão abranger IP, máscara, gateway e hostname.
* Evita regressões conceituais onde apenas IP é considerado regra de rede.
* Facilita automação, auditoria e testes de conformidade.

---

## Referência

O grupo **RETAGUARDA_LOJA** é o **primeiro exemplo oficial** que aplica este contrato completo,
servindo como template para todos os grupos futuros.

---

## Status

* **RETAGUARDA_LOJA**: Grupo fechado e oficial
* **Uso**: Template obrigatório para grupos futuros

---

## Backlog de Testes — RETAGUARDA_LOJA (Contrato Vivo)

Esta seção define a **matriz de cenários de teste** do grupo RETAGUARDA_LOJA.

Os testes **não são implementados neste ciclo**; o objetivo é garantir que o contrato
esteja explícito, testável e alinhado antes de qualquer código.

---

### 1. Regras de IP — Banco12

**Cenários esperados:**

* Aceita IP com **offset .12** dentro do bloco do grupo

**Cenários inválidos:**

* Rejeita offset pertencente a outros itens do grupo (ex.: Gerência, PSB, Farma)
* Rejeita offsets típicos de **TC/PDV** (faixa operacional)

---

### 2. Regras de IP — Gerência / PSB / Farma

**Cenários esperados:**

* Aceitam apenas seus **offsets fixos definidos**

**Cenários inválidos:**

* Rejeitam qualquer IP dentro de **faixa de TC**
* Rejeitam offsets não documentados no contrato do grupo

---

### 3. Máscara e Gateway (por perfil)

**Cenários esperados (quando implementado):**

* Valida máscara correta conforme o perfil de rede:

  * RD_SEGMENTADO_2024/2025 → /27
  * LEGACY_FLAT_2023 → /24
* Valida gateway conforme offset esperado do perfil

**Cenários inválidos:**

* Máscara divergente do perfil aplicado
* Gateway fora do padrão definido para o perfil

---

### 4. Hostname Pattern

**Cenários esperados (quando implementado):**

* Hostname segue o padrão documentado por item

**Cenários inválidos:**

* Hostname fora do pattern
* Hostname válido para outro item do grupo
* Hostname válido para outro grupo

---

### Diretriz de Evolução

* Cada cenário acima deve se tornar **teste automatizado** quando a validação for implementada.
* Inclusão de novos cenários exige atualização deste backlog.
* O backlog de testes é parte do **contrato vivo** do grupo.


---


# ADR — Grupos de Rede definem IP, máscara, gateway e hostname

---

## Data

2026-02-07

---

## Decisão

Os **Grupos de Rede** passam a ser responsáveis por definir, de forma explícita e documentada:

* política e regra de **IP**
* **máscara** de rede
* **gateway**
* **hostname pattern** esperado

Esses elementos compõem o **contrato do grupo**, e não devem ser tratados de forma isolada ou implícita.

---

## Contexto

Historicamente, erros operacionais de rede não se limitam à escolha do IP.
Problemas recorrentes incluem:

* uso de máscara incorreta
* gateway divergente do padrão esperado
* hostname fora do padrão operacional

Tratar apenas o IP como regra de validação é insuficiente e deixa lacunas
que não podem ser detectadas automaticamente.

Para reduzir erro humano e aumentar previsibilidade, o domínio precisa
conhecer **toda a configuração mínima de rede esperada**, e não apenas o endereço IP.

---

## Consequências

* Grupos de rede tornam-se a **fonte de verdade** para configuração lógica de rede.
* Validações futuras poderão abranger IP, máscara, gateway e hostname.
* Evita regressões conceituais onde apenas IP é considerado regra de rede.
* Facilita automação, auditoria e testes de conformidade.

---

## Referência

O grupo **RETAGUARDA_LOJA** é o **primeiro exemplo oficial** que aplica este contrato completo,
servindo como template para todos os grupos futuros.

---

## Status

* **RETAGUARDA_LOJA**: Grupo fechado e oficial
* **Uso**: Template obrigatório para grupos futuros

---

## Backlog de Testes — RETAGUARDA_LOJA (Contrato Vivo)

Esta seção define a **matriz mínima de cenários de teste** do grupo RETAGUARDA_LOJA,
separada por **perfil de rede**.

Os testes **não são implementados neste ciclo**; este backlog existe para garantir
que o contrato do grupo seja explícito, verificável e não sofra regressões futuras.

---

## PERFIL: LEGACY_FLAT

### Regras de IP — Itens

**Micro Gerência**

* Aceita offset **.30**
* Rejeita offset **.130**

**Micro Farma**

* Aceita offset **.60**
* Rejeita offset **.131**

**Portal do Saber (RH)**

* Aceita offset **.70**
* Rejeita offset **.129**

**Banco12**

* Aceita offset **.12**
* Rejeita offset **.13**

---

### Gateway e Máscara

**Cenários esperados:**

* Gateway esperado: **.222**
* Máscara esperada: **/24**

**Cenários inválidos:**

* Gateway diferente de .222
* Máscara diferente de /24

---

## PERFIL: RD_SEGMENTADO

### Regras de IP — Itens

**Portal do Saber (RH)**

* Aceita offset **.129**
* Rejeita offset **.70**

**Micro Gerência**

* Aceita offset **.130**
* Rejeita offset **.30**

**Micro Farma**

* Aceita offset **.131**
* Rejeita offset **.60**

**Banco12**

* Aceita offset **.12**
* Rejeita offset **.11** (quando colidir com TC/legado)

---

### Gateway e Máscara — Micros de Retaguarda

**Cenários esperados:**

* Gateway esperado: **.158**
* Máscara esperada: **/27**

**Cenários inválidos:**

* Gateway diferente de .158
* Máscara diferente de /27

---

### Diretriz de Evolução

* Cada cenário listado deve se tornar **teste automatizado** quando a validação for implementada.
* Alterações nos offsets, máscara ou gateway exigem atualização deste backlog.
* O backlog de testes faz parte do **contrato vivo** do grupo.

