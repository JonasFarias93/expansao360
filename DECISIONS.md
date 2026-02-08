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
# DECISIONS — EXPANSÃO360

Este documento registra decisões técnicas e arquiteturais relevantes do projeto, com o objetivo de evitar ambiguidades, manter rastreabilidade e facilitar onboarding.

## Formato padrão de cada decisão

* **Data** (YYYY-MM-DD)
* **Decisão**
* **Contexto**
* **Consequências**
* **Status** (opcional: Proposto | Aceito | Deprecado)

---

## 2026-02-06 — Cards-resumo interativos na Fila Operacional (prioridade)

**Status:** Aceito

### Decisão

Adicionar um header na tela de **Fila Operacional** contendo **cards-resumo clicáveis** para:

* Total de chamados na fila
* Quantidade por prioridade (Crítico/Alto/Médio/Baixo)

Os cards funcionam também como **filtro rápido** via querystring:
`?prio=CRITICO|ALTO|MEDIO|BAIXO`.

### Contexto

A fila operacional precisa oferecer leitura imediata da carga de trabalho e reduzir o custo de “caçar” chamados. A UI já é baseada em cards e ações rápidas; faltava uma visão agregada e um mecanismo direto de filtragem.

### Consequências

* A view da fila expõe contadores agregados (`counts`) e o filtro atual (`prio_selected`).
* Filtragem stateless (URL), facilitando compartilhamento e testes.
* Template só renderiza; regra de filtro/agregações ficam na view.

---

## 2026-02-06 — Filtro por projeto na Fila via `projeto_id` (temporário)

**Status:** Aceito

### Decisão

Implementar o filtro de projeto na Fila Operacional via querystring usando o **PK do Projeto**:

* `?projeto=<id>`

Mantendo compatibilidade com o filtro por prioridade (`?prio=`) e abordagem stateless (URL).

### Contexto

O modelo `Projeto` não possui `slug` no schema atual, e o projeto já utiliza `?projeto=<id>` em endpoints auxiliares (ex.: carregamento de subprojetos). Para entregar valor incremental sem migrações, adotamos `id` como identificador.

### Consequências

* A view expõe `projects` com `{id, nome, count, url, active, projeto}` para UI.
* O filtro combina `prio + projeto` sem estado de sessão.
* Evolução futura: adicionar `slug` em `Projeto` e migrar para `?projeto=<slug>` (nova ADR quando ocorrer).

---

## 2026-02-04 — Testes de JavaScript com Jest

**Status:** Aceito

### Decisão

Adotar **Jest + jsdom** para testar JS puro do frontend (ex.: formsets dinâmicos).

### Contexto

Bugs em linhas adicionadas dinamicamente não são cobertos por testes backend e tendem a reaparecer durante refactors de templates.

### Consequências

* Node/npm passam a ser dependência de desenvolvimento.
* Testes JS ficam próximos aos arquivos estáticos do app.
* Integração com o fluxo de desenvolvimento/CI deve incluir execução de testes JS quando aplicável.

---

## 2026-02-07 — Padronização de Chamado Externo

**Status:** Aceito

### Decisão

Padronizar a exibição e uso de identificadores externos de chamados exclusivamente através dos campos:

* `ticket_externo_sistema`
* `ticket_externo_id`

### Contexto

O ServiceNow será descontinuado e a aplicação já possuía campos genéricos para integração externa. A UI ainda referenciava um campo específico, gerando confusão e ocultando dados válidos.

### Consequências

* UI passa a exibir “Chamado Externo” no formato `<sistema>: <id>`.
* Filtros e buscas passam a funcionar corretamente.
* Campo legado específico foi removido do modelo e do banco.

---

## 2026-02-07 — Unicidade global do ticket externo

**Status:** Aceito

### Decisão

Garantir que `ticket_externo_id` seja **único globalmente** em `Chamado`, independentemente de `ticket_externo_sistema`.

A restrição aplica-se apenas quando `ticket_externo_id` estiver preenchido.

### Contexto

Apesar de existirem múltiplos sistemas externos, o identificador do ticket é tratado como único no ecossistema. Permitir repetição por sistema geraria ambiguidade na busca, auditoria e integrações.

### Consequências

* Adição de `UniqueConstraint` condicional em `ticket_externo_id`.
* Testes atualizados para refletir unicidade global.
* `ticket_externo_sistema` permanece como metadado informativo.

---

## 2026-02-07 — App `redes` para governança e validação de regras de rede

**Status:** Aceito

### Decisão

Consolidar o domínio de rede no app Django `redes`, com foco inicial em:

* Perfis de rede (ex.: `LEGACY_FLAT_2023`, `RD_SEGMENTADO_2024/2025`)
* Regras por tipo de equipamento (ex.: `TC`, `PDV`)
* Service puro para **classificação/validação de IP** com TDD como contrato

### Contexto

O preenchimento de rede era manual (planilhas/memória) e a validação era feita por conferência humana. As regras são simples, porém recorrentes e propensas a erro.

### Consequências

* Regras deixam de ficar dispersas e passam a existir como domínio versionado.
* O sistema passa a alertar inconsistências e reduzir erros de entrada.
* Testes unitários passam a proteger o comportamento (regressão vira falha de teste).

---

## 2026-02-07 — Integração futura entre Cadastro de Equipamentos e Grupos de Rede

**Status:** Aceito

### Decisão

Planejar a integração entre o cadastro de tipos de equipamento e as regras de rede, introduzindo futuramente uma **FK opcional** de `TipoEquipamento` para o conceito de **Grupo de Rede** (atualmente representado por `RegraRedeEquipamento`).

Além disso, **não modelar variações como tipos distintos** (ex.: `PDV1`, `PDV2`); a diferenciação por índice/unidade será responsabilidade da **instância em execução**.

### Contexto

As regras variam por perfil e tipo, mas o mesmo tipo (PDV, TC, etc.) pode possuir múltiplas instâncias em campo. Criar tipos artificiais (`PDV1`, `PDV2`) gera explosão de cadastro e mistura planejamento com execução.

### Consequências

* `TipoEquipamento` poderá (no futuro) referenciar um Grupo de Rede, mas a FK será opcional.
* O índice do equipamento (ex.: PDV #1, #2) será tratado na execução.
* A severidade (WARN → ERROR) poderá evoluir conforme maturidade do domínio e aderência do cadastro.

---

## 2026-02-07 — Grupos de Rede descrevem o papel completo na rede

**Status:** Aceito

### Decisão

O conceito de regra de rede evolui para **Grupo de Rede**, que descreve o papel completo na rede, não apenas o IP.

Cada Grupo de Rede deve definir explicitamente:

* IP (policy + offsets/faixa)
* Máscara
* Gateway
* Hostname (pattern)

A regra continua sendo **de domínio**, não de instância. Instâncias (`PDV1`, `TC3`) pertencem exclusivamente à execução.

### Contexto

Na prática, erros comuns incluem IP correto com máscara/gateway incorretos e hostname fora do padrão, o que não é detectável quando a regra trata apenas IP. Para reduzir erro humano e permitir validações futuras completas, o domínio precisa conhecer a configuração mínima esperada.

### Consequências

* O domínio passa a suportar validações multidimensionais (IP, máscara, gateway e hostname).
* Grupos tornam-se documentação viva e base para automação futura.
* A evolução será feita sem UI e sem acoplamento à execução, mantendo service puro e TDD.

---

## 2026-02-08 — Busca server-side na Lista de Lojas com estado na URL

**Status:** Aceito

### Decisão

Implementar a busca da Lista de Lojas de forma **server-side**, persistindo estado via querystring (ex.: `?q=paulista&page=2&per_page=25`).

A UI terá input “Buscar” com submit por Enter e botão “Buscar” (MVP sem debounce/JS).

### Contexto

A listagem possui milhares de lojas; filtrar no browser exigiria carregar todos os registros e degradaria performance. O time precisa copiar links e manter estado ao navegar/voltar, facilitando suporte e debugging.

### Consequências

* Busca passa a ser filtro no backend (QuerySet).
* Parâmetro `q` é preservado na paginação.
* Mantém `per_page` atual.
* MVP sem debounce; se necessário, evoluir para debounce via JS posteriormente.

---

## Decisões pendentes de implementação

Esta seção lista decisões **já registradas** que ainda não foram totalmente implementadas no código.

### 2026-02-03 — Padronização de códigos (internos vs externos)

**Status:** Proposto

### 2026-02-04 — Tipos de equipamento governados por Categoria

**Status:** Aceito

### Consolidação de itens duplicados na edição de Kit (UX)

**Status:** Em avaliação
**Nota:** Caso aceito, registrar ADR específica.
