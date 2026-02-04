# DECISIONS — EXPANSÃO360

Este documento registra decisões técnicas e arquiteturais relevantes do projeto,
com o objetivo de evitar ambiguidades, manter rastreabilidade e facilitar onboarding.

## Formato padrão de cada decisão

* Data (YYYY-MM-DD)
* Decisão
* Contexto
* Consequências

---

## 2026-01-20 — Separação conceitual: Registry x Operation

**Decisão**
O sistema será modelado com duas camadas conceituais principais:

* **Registry (Cadastro Mestre)**: define “o que existe” e “como deve ser”
* **Operation (Execução de Campo)**: registra “o que foi executado”, com rastreabilidade e histórico

**Contexto**
Precisamos garantir governança sobre padrões e, ao mesmo tempo, registrar a execução real em campo
sem poluir o cadastro mestre e sem perder histórico.

**Consequências**

* Operation referencia Registry; Registry não depende de Operation.
* O domínio será desenhado para suportar auditoria e evolução segura.

---

## 2026-01-20 — Estratégia de trabalho: microtarefas + disciplina de versionamento

**Decisão**
O desenvolvimento seguirá por microtarefas com validação objetiva,
usando branches e commits pequenos.

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

* `.gitignore` genérico
* Nenhuma estrutura de framework antecipada
* Stack definida posteriormente via ADR

---

## 2026-01-21 — Stack Web definida: Django

**Decisão**
A camada Web será implementada em **Django**.

**Contexto**
Após estabilização do core e da CLI, era necessário um framework maduro
para UI, autenticação, ORM e velocidade de entrega.

**Consequências**

* Core permanece independente
* Django atua como adapter
* Models Django não contêm regras de negócio

---

## 2026-01-21 — Nomenclatura em PT-BR no domínio

**Decisão**
O domínio e casos de uso utilizam nomenclatura em português (PT-BR).

**Contexto**
Reduzir carga cognitiva e aproximar o código do negócio real.

**Consequências**

* Core em PT-BR
* Framework/infra seguem convenções originais
* Glossário mantido para consistência

---

## 2026-01-21 — Entidade operacional “Chamado”

**Decisão**
O termo **Chamado** substitui “Card” como entidade operacional.

**Contexto**
“Card” é ambíguo e visual. “Chamado” representa melhor uma unidade operacional.

**Consequências**

* Domínio, CLI e Web utilizam “Chamado”
* Possíveis aliases temporários para compatibilidade

---

## 2026-01-21 — Equipamentos rastreáveis vs contáveis (`tem_ativo`)

**Decisão**
Equipamentos são classificados como:

* **Rastreáveis** (`tem_ativo=True`)
* **Contáveis** (`tem_ativo=False`)

**Contexto**
Nem todos os itens exigem ativo/número de série.

**Consequências**

* Execução valida campos conforme tipo
* Relatórios diferenciam ativos e consumíveis

---

## 2026-01-21 — Layout base Web com Tailwind (CDN)

**Decisão**
Adotar Tailwind via CDN e estrutura base de templates (`base`, `partials`, `components`).

**Contexto**
Padronizar UI desde o início sem custo de build frontend.

**Consequências**

* Layout tratado como decisão arquitetural
* Evita HTML duplicado e decisões visuais ad-hoc

---

## 2026-01-21 — Camada Web como adapter

**Decisão**
A Web atua apenas como adapter (UI + persistência + orquestração).

**Contexto**
Evitar migração de regras de negócio para a camada Web.

**Consequências**

* Core independente
* CLI e Web compartilham domínio
* Facilita API e mobile no futuro

---

## 2026-01-21 — Fluxo inverso via novo Chamado (Loja → Matriz)

**Decisão**
Correções e retornos geram **novo Chamado**, nunca edição destrutiva.

**Contexto**
Chamados representam eventos operacionais e contábeis reais.

**Consequências**

* Histórico imutável
* Retornos exigem desfecho explícito
* Auditoria e contabilidade preservadas

---

## 2026-01-22 — Evidências (anexos) por Chamado

**Decisão**
Evidências são entidades próprias vinculadas a Chamados.

**Contexto**
NF, Carta de Conteúdo e documentos de exceção são parte do processo real.

**Consequências**

* Finalização pode exigir evidência
* Auditoria fortalecida
* Modelo extensível (fotos, assinaturas, etc.)

---

## 2026-01-22 — IAM mínimo por capabilities

**Decisão**
Adoção de **Capability-Based Access Control** na camada Web.

**Contexto**
Precisamos restringir ações sensíveis sem acoplar IAM ao domínio.

**Consequências**

* Backend valida permissões
* Templates apenas refletem
* Core permanece permission-agnostic

---

## ADR — 2026-01-24 — CBVs + CapabilityRequiredMixin

**Status:** Aceito
**Contexto:** Sprint 3 — Execução / Fluxo Inverso / IAM

**Decisão**

* Migrar views críticas para CBVs
* Centralizar autorização em `CapabilityRequiredMixin`

**Consequências**

* Menos repetição
* Padrão consistente
* Migração incremental segura

---

## 2026-01-24 — Abertura de Chamado via UI

**Decisão**
Chamados podem ser abertos via UI, gerando automaticamente Itens de Execução
a partir do Kit (snapshot operacional).

**Contexto**
Necessidade de testes end-to-end e uso real do sistema.

**Consequências**

* Chamado nasce do Registry
* Itens são imutáveis conceitualmente
* Planejamento e execução ficam claramente separados

---

## 2026-01-25 — Introdução de Subprojetos no Registry

**Decisão**
Introduzir a entidade **Subprojeto** no **Registry (Cadastro Mestre)** como
recorte organizacional obrigatório quando existente.

**Contexto**
Projetos reais de expansão exigem segmentação operacional por linhas de entrega.

**Consequências**

* Subprojeto pertence ao Registry
* Chamados referenciam Subprojeto quando existir
* Subprojetos não são deletados destrutivamente

---

## 2026-02-02 — Mapeamento operacional: “Filial” como “Java” no Cadastro de Lojas

**Decisão**
Exibir **Filial** como **Java** e **Nome Filial** como **Nome loja** na UI,
mantendo compatibilidade com base externa.

**Contexto**
Alinhar o sistema à linguagem operacional do dia a dia sem quebrar integrações.

**Consequências**

* Importador mapeia campos explicitamente
* UI usa labels operacionais
* Testes cobrem o mapeamento

---

## 2026-02-02 — Padronização de Logomarca no Cadastro de Lojas

**Decisão**
Padronizar o campo **Logomarca**:

* Normalizar para maiúsculo
* Preferir dropdown no cadastro manual

**Contexto**
Evitar divergências (RAIA/raia/RaIa).

**Consequências**

* Menos inconsistência
* UI mais segura
* Testes de normalização

---

## 2026-02-02 — Refinamento do Cadastro de Equipamentos (Registry)

**Decisão**
Equipamentos são tratados como entidade de **Registry**, focados em padronização
e reutilização operacional.

**Contexto**
CRUD atual não reflete uso real nem validações necessárias.

**Consequências**

* Ajustes em model, form, testes e UI
* Possível migração de dados
* Reuso do padrão aplicado em Lojas

---

## 2026-02-02 — Padronização da estrutura de testes por camadas

**Decisão**
Organizar testes por camadas arquiteturais (Domain, Usecases, Interfaces).

**Contexto**
A organização atual dificulta leitura, manutenção e escalabilidade.

**Consequências**

* Estrutura clara por responsabilidade
* Facilita onboarding
* Impõe disciplina para novos testes

---

## 2026-02-03 — Código de Equipamento gerado automaticamente

**Decisão**
O campo `Equipamento.codigo` passa a ser gerado automaticamente,
único, normalizado e imutável.

**Contexto**
Evitar inconsistência e erro humano em identificadores usados no dia a dia.

**Consequências**

* Lógica no model
* Campo oculto na UI
* Testes de geração, colisão e imutabilidade

---

## 2026-02-03 — Tipos de Equipamento como cadastro mestre por categoria

**Decisão**
Criar `TipoEquipamento` como entidade de Registry vinculada à Categoria,
substituindo texto livre em `ItemKit.tipo`.

**Contexto**
Texto livre gera inconsistência e dificulta histórico.

**Consequências**

* Novo model e migração
* Forms e testes atualizados
* Integridade referencial garantida

---

## ADR — 2026-02-03 — Padronização de códigos (internos vs externos)

**Status:** Proposto

**Decisão**
Diferenciar:

* **Códigos externos** (ex.: Loja/Java) — manuais/importados
* **Códigos internos** (ex.: Equipamento, TipoEquipamento) — automáticos

**Contexto**
Evitar confusão entre identificadores operacionais e internos do Registry.

**Consequências**

* UI trata códigos conforme tipo
* Testes específicos por categoria
* Maior clareza e segurança para integrações
---

## 2026-02-03 — Cadastro mestre de Kit e KitItem (Registry)

**Decisão**
Adicionar entidades de cadastro mestre:
- **Kit**: conjunto padronizado usado em fluxos operacionais
- **KitItem**: itens que compõem um Kit, com quantidade e ordenação

**Contexto**
Precisamos representar kits padronizados para apoiar o fluxo de chamados, garantindo governança e reutilização.
Como é informação relativamente estável e de referência, pertence ao **Registry** e não à camada Operation.

**Consequências**
- Operation poderá referenciar Kit (no futuro) sem criar dependência inversa.
- Validaremos unicidade de código de Kit e integridade de KitItem (quantidade mínima, ordenação).
- CRUD será exposto via Django (camada de entrega), sem regras de negócio dentro de views/models além de validações simples.

---

## 2026-02-03 — Configuração (IP) é decisão do Chamado, não do Kit

**Decisão**
A necessidade de configuração (ex: exigir IP) será definida na execução do Chamado, e não imposta pelo cadastro de Kit/ItemKit.

**Contexto**
No cadastro atual, `ItemKit.requer_configuracao` define itens que exigem configuração. Porém, a regra de negócio exige que a configuração seja decidida no momento de montagem/execução do Chamado (pode variar por loja, cenário e orientação da OPF).

**Consequências**
- `InstalacaoItem` passa a ter o campo `deve_configurar` (bool).
- Campos operacionais como `ip` ficam na execução.
- O cadastro pode opcionalmente manter um campo de sugestão (`sugere_configuracao`) sem caráter obrigatório.
- A validação de finalização exigirá configuração somente quando `deve_configurar=True`.


---

## 2026-02-03 — Gate de NF e critérios de fechamento do Chamado

**Decisão**
O Chamado só será liberado para NF quando todos os itens rastreáveis estiverem bipados e todos os itens contáveis confirmados. O fechamento do Chamado exigirá número de NF e confirmação de coleta.

**Contexto**
A emissão da NF de saída depende da bipagem completa do kit e da conferência dos itens na caixa. Além disso, o Chamado não pode ser encerrado sem NF e sem confirmação de coleta pela transportadora.

**Consequências**
- Implementar método/flag de liberação para NF no `Chamado`.
- Incluir campos: `nf_pedido_numero`, `nf_saida_numero` (já existe), e controle de coleta (`coleta_solicitada_em`, `coleta_confirmada_em`).
- `finalizar()` passa a validar NF e coleta para ENVIO.

---
## 2026-02-03 — `InstalacaoItem` referencia `TipoEquipamento` via FK

**Decisão**
Alterar `InstalacaoItem.tipo` de string para `ForeignKey` para `TipoEquipamento`.

**Contexto**
`ItemKit.tipo` já é FK para `TipoEquipamento`, mas a execução armazenava esse dado como texto. Para garantir consistência, filtros e regras estáveis, a execução deve referenciar o mesmo cadastro mestre.

**Consequências**
- Migração de schema e ajuste na criação de itens (`gerar_itens_de_instalacao`).
- Ajuste de telas/serialização onde `tipo` era tratado como string.
