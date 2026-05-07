# REQUIREMENTS — EXPANSÃO360

Este documento descreve o que o sistema EXPANSÃO360 deve fazer.
Cada requisito é independente de implementação e verificável
por comportamento observável, teste automatizado ou validação operacional.

> Dúvidas sobre como um requisito é implementado: consulte `ARCHITECTURE.md`.
> Dúvidas sobre decisões técnicas: consulte `DECISIONS/`.

# 1. Escopo do Produto

## 1.1 Objetivo

O EXPANSÃO360 substitui planilhas dispersas por uma fonte única de verdade
para operações físicas de expansão de lojas.

O sistema permite rastrear chamados, ativos e projetos — registrando
quem fez o quê, quando e com quais evidências — de forma que o histórico
seja confiável, auditável e nunca se perca.

## 1.2 Problema que resolve

Antes do sistema, o controle era feito por múltiplas planilhas
sem conexão entre si. Isso gerava:

* Histórico fragmentado e não confiável
* Impossibilidade de rastrear um ativo ao longo do tempo
* Falta de clareza sobre quem realizou cada operação e quando

## 1.3 Princípio Central

O sistema opera em quatro estágios sequenciais:

* **Cadastro** → dados estruturais e base de planejamento:
  lojas, projetos, equipamentos, kits.
  Nenhuma operação acontece sem essa base.

* **Chamados** → prepara e organiza a operação:
  consome o Cadastro, monta os itens do chamado,
  define o que precisa ser coletado e coloca
  o chamado na fila operacional.

* **Execução** → trabalho ativo do técnico:
  o técnico assume o chamado, preenche as informações,
  registra ativos, coleta evidências e finaliza.

* **Histórico** *(planejado)* → consolidação imutável:
  armazena o chamado finalizado como registro
  permanente e auditável.

Cada estágio alimenta o seguinte.
Nenhum estágio altera retroativamente o anterior.

## RF-01 — Cadastro Mestre

O sistema deve permitir cadastrar e manter as entidades
estruturais que servem de base para todas as operações.
O Cadastro é a memória institucional do sistema — centraliza
informações que antes existiam apenas na cabeça das pessoas
ou em planilhas dispersas.

---

### Lojas

Campos obrigatórios:
- Filial (código identificador)
- Hist. (código histórico)
- Nome da Filial
- Endereço, Bairro, Cidade, UF
- Logomarca
- IP Banco 12 (IP da base de dados local da loja,
  sempre terminado em .12)

Campo opcional:
- Telefone

---

### Projetos

Campos obrigatórios:
- Nome do Projeto
- Data de início e Data de fim
- Responsáveis (um ou mais)

---

### Subprojetos

Campos obrigatórios:
- Nome do Subprojeto
- Projeto ao qual pertence
- Data de início e Data de fim
- Responsáveis (um ou mais)

---

### Categorias

Agrupador de equipamentos por natureza.
Exemplos: Impressoras, CPU, Monitores.

---

### Equipamentos

Cada equipamento pertence a uma Categoria
e pode receber diferentes Tipos conforme o contexto.

O Tipo não altera o que o equipamento é —
define para qual finalidade ele serve e garante
que o equipamento correto seja enviado para cada operação.

Exemplo:
- Categoria: Impressoras
- Equipamento: Impressora
- Tipos possíveis: A4, Oferta, Cupom

---

### Tipos de Equipamento

Define a especialização de um equipamento dentro de uma categoria.
Um equipamento pode ter múltiplos tipos possíveis.

Exemplos:
- Impressora → A4 / Oferta / Cupom
- MicroComputador → PDV / TC All in One
- Monitor → Touch / LCD

---

### Kits e Itens de Kit

Kit é o facilitador operacional do sistema.
Agrupa equipamentos com tipo e quantidade definidos,
servindo como base para abrir um Chamado.

Garante que o técnico envie os equipamentos certos
para cada tipo de operação — preservando o conhecimento
institucional independente de quem está executando.

Campos:
- Nome do Kit
- Descrição (opcional)
- Projeto vinculado (opcional)
- Subprojeto vinculado (opcional)

Um kit pode conter o mesmo equipamento com tipos diferentes.

Exemplo — Kit Abertura de Loja:
- 2x Impressora (sendo 1 Cupom e 1 A4)
- 1x MicroComputador (PDV)
- 1x Monitor (Touch)

---

### Critérios de aceitação

- CRUD disponível para todas as entidades
- Alterações no Cadastro não afetam Chamados já criados
- O sistema deve impedir exclusão de entidades
  vinculadas a Chamados existentes
- Um Kit deve poder conter o mesmo equipamento
  com tipos diferentes
- Ao selecionar Projeto/Subprojeto na abertura de um Chamado,
  o sistema filtra os Kits vinculados a ele

### Fonte
`web/cadastro/`

## RF-02 — Abertura de Chamado

O sistema deve permitir que técnicos autorizados abram Chamados,
definindo o contexto da operação e os itens que serão executados.

---

### Quem pode abrir

Apenas técnicos com permissão de abertura podem criar Chamados.
Técnicos sem essa permissão podem apenas executar Chamados
já abertos por outros.

---

### Dados da abertura

Para abrir um Chamado, o técnico deve informar:

- Loja de destino
- Projeto e Subprojeto
- Tipo: ENVIO (Matriz → Loja)
Chamados de RETORNO não são abertos manualmente.
Eles são gerados a partir de um Chamado de ENVIO previamente finalizado.
- Prioridade (padrão, baixa, média, alta, crítica)
- Kit base (opcional)
- Ticket externo (opcional — sistema e ID de referência externa)

---

### Kit como facilitador

O Kit é opcional — não é obrigatório para abrir um Chamado.

Quando selecionado, o sistema gera automaticamente os itens
do Chamado com base na composição do kit, evitando que o
técnico precise adicionar item por item.

Chamados podem ser abertos sem kit, com itens adicionados
manualmente — para casos avulsos ou operações especiais.

---

### Geração automática de itens (Snapshot)

Quando um Kit é selecionado, o sistema gera o snapshot
dos itens no momento da abertura.

Regras do snapshot:

- Itens rastreáveis (com ativo) → gerados individualmente,
  um por unidade, para permitir bipagem
- Itens contáveis (sem ativo) → gerados como linha agregada
  com quantidade total
- Alterações futuras no Kit não afetam o Chamado já criado

---

### Edição dos itens na abertura

Durante a abertura (status EM_ABERTURA), o técnico autorizado
pode ajustar os itens antes de confirmar:

- Adicionar itens avulsos
- Remover itens
- Alterar tipos de equipamento

Após confirmação (status ABERTO), os itens só podem ser
alterados por técnicos com permissão explícita para isso,
para cobrir casos em que a solicitação muda no meio do caminho.

---

### Critérios de aceitação

- Apenas técnicos com permissão podem abrir Chamados
- O Kit é opcional — o Chamado pode ser aberto sem kit
- Quando kit selecionado, itens são gerados automaticamente
- Alterações futuras no Kit não afetam Chamados já criados
- O técnico pode editar os itens durante EM_ABERTURA
- Após ABERTO, edição de itens exige permissão específica
- O Chamado nasce com status EM_ABERTURA
- O Chamado só avança para ABERTO após confirmação do setup

### Fonte
`web/chamados/`
`web/chamados/models.py` — `gerar_itens_de_instalacao()`

Fechado. Tenho tudo para escrever RF-04 e RF-05.

Vou escrever os dois agora — você valida antes de avançar para o próximo.

---

## RF-03 — Chamado de Retorno

O sistema deve permitir gerar um Chamado de RETORNO a partir de um Chamado de ENVIO previamente finalizado, reutilizando os itens já expedidos e garantindo rastreabilidade completa do ciclo de vida dos equipamentos.

---

## Princípio

RETORNO **não é uma abertura independente**.

Ele é uma **continuação operacional** de um ENVIO já concluído.

> Todo RETORNO tem origem em um ENVIO.
> Nem todo ENVIO gera RETORNO.

---

## Origem do Retorno

Um Chamado de RETORNO só pode ser criado a partir de:

* Chamado com status `FINALIZADO`
* Com itens válidos registrados

---

## Seleção de itens

Ao gerar o RETORNO, o sistema deve permitir:

### 1. Retorno parcial

Selecionar itens específicos do chamado original

Exemplo:

* Retornar apenas 1 impressora de um kit

---

### 2. Retorno total

Selecionar todos os itens do chamado original

---

## Snapshot do retorno

O Chamado de RETORNO deve gerar um novo snapshot baseado nos itens selecionados.

Regras:

* Itens rastreáveis → continuam individuais (com vínculo ao ativo original)
* Itens contáveis → nova linha com quantidade correspondente
* Nenhuma alteração no chamado original

---

## Vínculo entre chamados

O sistema deve manter referência explícita:

* RETORNO → referencia o ENVIO de origem
* ENVIO → deve permitir visualizar RETORNOS associados

Isso garante:

* Rastreabilidade completa por ativo
* Navegação bidirecional

---

## Estado inicial

O Chamado de RETORNO nasce com:

```
EM_ABERTURA
```

E segue o mesmo fluxo operacional:

```
EM_ABERTURA → ABERTO → EM_EXECUCAO → ...
```

---

## Regras de integridade

* Não é permitido criar RETORNO de chamado não finalizado
* Itens já retornados não podem ser retornados novamente
* Um item pode ter múltiplos ciclos ao longo do tempo:

  ```
  ENVIO → RETORNO → ENVIO → RETORNO
  ```
* O histórico deve refletir todos os ciclos sem sobrescrever dados

---

## Impacto no Histórico (RF-09)

O histórico deve:

* Exibir claramente o vínculo ENVIO ↔ RETORNO
* Permitir visualizar a “linha de vida” de um ativo
* Mostrar ciclos completos de movimentação

---

## Permissões

* Apenas técnicos autorizados podem gerar RETORNO
* Geração de RETORNO não altera o chamado original

---

## Critérios de aceitação

* RETORNO só pode ser criado a partir de chamado FINALIZADO
* Sistema permite retorno parcial ou total
* Snapshot do retorno é independente
* Chamados permanecem imutáveis
* Existe vínculo bidirecional entre ENVIO e RETORNO
* Itens não podem ser retornados duplicadamente
* Histórico reflete corretamente os ciclos

---

## Fonte

`web/chamados/models.py`
`web/execucao/models.py`
RF-02 — Abertura de Chamado
RF-09 — Histórico da Loja

---

# Resultado


* 🔒 Integridade forte (sem retorno fantasma)
* 🔁 Ciclo de vida real dos ativos
* 🧠 Histórico auditável de verdade
* 🚫 Zero ambiguidade operacional

---

## RF-04 — Fila Operacional

O sistema deve organizar os Chamados abertos em uma fila operacional
global, visível a todos os técnicos, com ordenação controlada por
prioridade e data de abertura.

---

### Visibilidade

A fila é global — todos os técnicos autenticados visualizam
todos os Chamados disponíveis, independente de região ou projeto.

---

### Ordenação

Ordenação padrão: **FIFO** — o Chamado mais antigo aparece primeiro.

Quando há prioridade definida, a ordenação é:

1. Prioridade (crítica → alta → média → baixa → padrão)
2. Data de abertura (mais antigo primeiro) dentro do mesmo nível

---

### Prioridade

- Definida na abertura do Chamado
- Pode ser alterada após abertura por técnico com permissão para isso
- Níveis: padrão, baixa, média, alta, crítica

---

### Quais Chamados aparecem

Apenas Chamados com status `ABERTO` em diante.
Chamados em `EM_ABERTURA` não aparecem na fila.

---

### Critérios de aceitação

- Fila exibe todos os Chamados `ABERTO+` para todos os técnicos
- Ordenação padrão é FIFO
- Prioridade sobrepõe ordenação por data
- Chamados em `EM_ABERTURA` não aparecem
- Apenas técnicos com permissão podem alterar prioridade

### Fonte
`web/execucao/templates/`
`web/chamados/models.py`

---

## RF-05 — Execução pelo Técnico

O sistema deve permitir que um técnico assuma um Chamado da fila,
trabalhe nele com progresso persistido e libere para outros quando
necessário.

---

### Assumir um Chamado

Ao assumir um Chamado, o sistema cria uma **ExecutionSession**
vinculada ao técnico e ao Chamado.

Enquanto a sessão está ativa:
- O Chamado fica travado para outros técnicos
- Apenas o técnico com sessão ativa pode editar

---

### Persistência do progresso

O sistema salva o progresso **automaticamente e continuamente**
durante a execução.

Nenhum dado é perdido por inatividade ou troca de técnico.
Quando outro técnico assume, encontra o trabalho exatamente
onde foi deixado.

---

### Liberação da sessão

A sessão é liberada em dois casos:

1. **Manual** — técnico clica em salvar/liberar explicitamente
2. **Por inatividade** — sessão expira após **1 hora** sem atividade

Em ambos os casos:
- Progresso está salvo
- Chamado volta à fila disponível para outro técnico assumir

---

### Troca de técnico

Um Chamado pode ser assumido por técnicos diferentes ao longo
do seu ciclo de vida. O histórico de quem trabalhou no chamado
é registrado via **ExecutionSessionLog**.

---

### Critérios de aceitação

- Técnico assume o Chamado → sessão criada → Chamado travado
- Progresso salvo automaticamente e continuamente
- Sessão expira após 1 hora de inatividade
- Expiração não causa perda de dados
- Chamado liberado volta à fila disponível
- Histórico de sessões preservado em ExecutionSessionLog

### Fonte
`web/execucao/models.py` — `ExecutionSession`, `ExecutionSessionLog`
`web/execucao/views.py`

---




## RF-05 — Execução pelo Técnico

O sistema deve permitir que um técnico assuma um Chamado da fila, trabalhe nele com progresso persistido e libere para outros quando necessário.

### Assumir um Chamado
Ao assumir um Chamado, o sistema cria uma **ExecutionSession** vinculada ao técnico e ao Chamado.

Enquanto a sessão está ativa:
- O Chamado fica travado para outros técnicos
- Apenas o técnico com sessão ativa pode editar

### Persistência do progresso
O sistema salva o progresso **automaticamente e continuamente** durante a execução.

Nenhum dado é perdido por inatividade ou troca de técnico. Quando outro técnico assume, encontra o trabalho exatamente onde foi deixado.

### Liberação da sessão
A sessão é liberada em dois casos:
1. **Manual** — técnico clica em salvar/liberar explicitamente
2. **Por inatividade** — sessão expira após **1 hora** sem atividade

Em ambos os casos:
- Progresso está salvo
- Chamado volta à fila disponível para outro técnico assumir

### Troca de técnico
Um Chamado pode ser assumido por técnicos diferentes ao longo do seu ciclo de vida. O histórico de quem trabalhou no chamado é registrado via **ExecutionSessionLog**.

### Critérios de aceitação
- Técnico assume o Chamado → sessão criada → Chamado travado
- Progresso salvo automaticamente e continuamente
- Sessão expira após 1 hora de inatividade
- Expiração não causa perda de dados
- Chamado liberado volta à fila disponível
- Histórico de sessões preservado em ExecutionSessionLog

### Fonte
`web/execucao/models.py` — `ExecutionSession`, `ExecutionSessionLog`
`web/execucao/views.py`

---

## RF-06 — Gates Operacionais

O sistema deve proteger cada transição de estado do Chamado com validações objetivas, garantindo que nenhuma etapa seja pulada e que o histórico reflita a realidade operacional.

### Gates por transição

**Gate 1 — Liberar para execução (`ABERTO` → `EM_EXECUCAO`)**
- Chamado possui ao menos um item
- Técnico possui sessão ativa

**Gate 2 — Liberar solicitação de NF (`EM_EXECUCAO` → `AGUARDANDO_NF`)**
- Todos os itens rastreáveis bipados (Ativo + Nº de Série)
- Todos os itens não rastreáveis checados (contagem confirmada)
- Todos os itens marcados como "requer configuração" estão configurados
- C.EQUIPAMENTO (ticket externo) preenchido

**Gate 3 — Liberar solicitação de Coleta (`AGUARDANDO_NF` → `AGUARDANDO_COLETA`)**
- Chamado NF preenchido
- Número da NF preenchido
- Evidência obrigatória anexada:
  - NF em PDF → prioritária, obrigatória quando disponível
  - Declaração de Conteúdo → obrigatória apenas quando NF não puder ser emitida
  - Ao menos um dos dois deve estar presente

**Gate 4 — Fechar Chamado (`AGUARDANDO_COLETA` → `FINALIZADO`)**
- Coleta confirmada

### Quem executa cada gate

| Gate | Quem pode executar |
|------|--------------------|
| Gate 1 — Assumir execução | Técnico Executor ou superior |
| Gate 2 — Liberar NF | Técnico Responsável / com permissão |
| Gate 3 — Liberar Coleta | Técnico Responsável / com permissão |
| Gate 4 — Fechar Chamado | Técnico Responsável / com permissão |

### Critérios de aceitação
- Tentativa de avançar sem cumprir gate é bloqueada no backend
- Sistema indica claramente o que falta para liberar cada gate
- Templates apenas refletem o estado — não implementam regras

### Fonte
`web/chamados/models.py`
`web/execucao/views.py`
`web/execucao/tests/`

---

## RF-07 — Evidências

O sistema deve permitir anexar documentos PDF a um Chamado como evidência formal da operação realizada.

### Tipos de evidência

| Tipo | Descrição | Obrigatoriedade |
|------|-----------|-----------------|
| NF de Saída | PDF da Nota Fiscal emitida | Prioritária — obrigatória quando disponível |
| Declaração de Conteúdo (DEC) | PDF declarando itens sem NF | Obrigatória apenas quando NF não puder ser emitida |
| Documento de Exceção | Carta de correção, documento de transporte aéreo, outros | Opcional |

### Regras
- Ao menos um documento obrigatório deve estar presente para liberar coleta
- NF prevalece sempre — DEC é substituto quando NF não é possível
- Evidências são entidades próprias vinculadas ao Chamado
- Formato aceito: PDF
- Múltiplos documentos podem ser anexados ao mesmo Chamado
- Evidências de Chamados finalizados são imutáveis

### Critérios de aceitação
- Evidência é entidade própria vinculada a um Chamado
- Sistema aceita múltiplos PDFs por Chamado
- Gate 3 bloqueia se nenhuma evidência obrigatória estiver presente
- Sistema identifica automaticamente qual evidência é necessária
- Evidências de Chamados finalizados não podem ser removidas

### Fonte
`web/chamados/models.py` — `EvidenciaChamado`
`web/execucao/views.py`

---

## RF-08 — Finalização

O sistema deve garantir que um Chamado só seja finalizado após todas as etapas operacionais estarem concluídas, preservando o histórico de forma imutável.

### Fluxo de finalização (ENVIO — Matriz → Loja)

```
100% itens validados (bipados + checados + configurados)
        ↓
Solicitação de NF → preenchimento de Chamado NF + Nº NF
        ↓
Anexo de evidência obrigatória (NF ou DEC)
        ↓
Solicitação de Coleta
        ↓
Confirmação de Coleta → FINALIZADO
```

### Imutabilidade
Chamado finalizado não pode ser alterado. Correções ou ajustes geram **novo Chamado** — o histórico do Chamado original é preservado integralmente.

### Critérios de aceitação
- Finalização só é permitida após todos os gates cumpridos
- Status `FINALIZADO` é terminal — nenhuma edição posterior
- Correções geram novo Chamado, nunca alteram o original
- Data e responsável pela finalização são registrados

### Fonte
`web/chamados/models.py`
`web/execucao/views.py`
`web/execucao/tests/`

---


## RF-09 — Histórico da Loja

O sistema deve manter um **histórico completo, cronológico e imutável de todas as operações relacionadas a uma Loja**, permitindo rastrear com precisão tudo o que ocorreu ao longo do tempo.

Esse histórico é uma **visão agregada da camada Operation**, nunca um dado editável ou manual.

---

# Objetivo

Garantir **rastreabilidade total por Loja**, consolidando:

* Chamados realizados (ENVIO / RETORNO)
* Execuções e sessões de técnicos
* Evidências anexadas
* Eventos de transição de estado

Sem permitir qualquer tipo de alteração retroativa.

---

# Princípio Arquitetural

O Histórico da Loja **não é uma entidade própria mutável**.

Ele é uma **projeção (read model)** derivada de:

* Chamado
* ExecutionSession / ExecutionSessionLog
* EvidenciaChamado
* Eventos de status

Respeitando:

> **Registry não guarda histórico operacional — Operation é a fonte de verdade.**

---

# Escopo do Histórico

O histórico de uma Loja deve consolidar os seguintes eventos:

## 1. Chamados

Cada Chamado vinculado à Loja deve aparecer com:

* ID do chamado
* Tipo (`ENVIO` / `RETORNO`)
* Status atual
* Data de criação
* Data de finalização (se houver)
* Responsável pela finalização

---

## 2. Linha do tempo de status

Para cada Chamado:

* Transições de estado (ex: ABERTO → EM_EXECUCAO → AGUARDANDO_NF → ...)
* Data/hora de cada mudança
* Usuário responsável

---

## 3. Execução (técnicos)

Registro de quem trabalhou no Chamado:

* Técnico
* Início da sessão
* Fim da sessão
* Tipo de saída:

  * Manual
  * Expiração por inatividade

Fonte: `ExecutionSessionLog`

---

## 4. Evidências

Para cada Chamado:

* Tipo de documento (NF, DEC, outros)
* Data de upload
* Usuário que anexou
* Indicador de obrigatoriedade

---

## 5. Eventos relevantes

Eventos importantes devem aparecer explicitamente:

* Liberação para execução
* Liberação de NF
* Liberação de coleta
* Confirmação de coleta
* Finalização

---

# Estrutura da Visualização

O histórico deve ser apresentado como:

### Linha do tempo unificada por Loja

Ordenada por:

```
data_evento DESC (mais recente primeiro)
```

Com agrupamento opcional por:

* Chamado
* Tipo de evento

---

# Regras de Imutabilidade

* Nenhum evento histórico pode ser editado ou removido
* Alterações operacionais geram **novos eventos**, nunca edição de eventos passados
* Chamados finalizados permanecem intactos no histórico
* Correções geram novos chamados (já refletido automaticamente no histórico)

---

# Performance e Modelagem

O histórico deve ser implementado como:

* Query agregada otimizada **ou**
* Read model materializado (se necessário por escala)

Nunca:

* Reprocessar lógica pesada em tempo real sem cache
* Duplicar lógica de domínio

---

# Permissões

A visualização do histórico deve respeitar o modelo de IAM:

* Usuários veem apenas Lojas permitidas
* Ações são somente leitura
* Nenhuma permissão de escrita existe sobre o histórico

---

# Critérios de Aceitação

* Histórico lista todos os Chamados da Loja
* Linha do tempo inclui eventos de status com data e responsável
* Execuções de técnicos são visíveis via sessões
* Evidências aparecem vinculadas corretamente
* Ordem cronológica consistente
* Nenhum dado pode ser editado
* Atualização é automática após qualquer operação
* Performance aceitável mesmo com alto volume

---

# Fonte

* `web/execucao/models.py` — Chamado, ExecutionSession, ExecutionSessionLog, EvidenciaChamado
* `web/execucao/views.py`
* Arquitetura — separação Registry vs Operation


Perfeito — aqui entra uma das partes mais críticas do sistema.
Se errar RF-10, o resto vira gambiarra. Se acertar, tudo fica consistente.

Vou te entregar já no nível **estrutural correto (capabilities, não roles hardcoded)**.

---

# RF-10 — Autorização por Capabilities

O sistema deve controlar todas as ações e acessos com base em **capacidades (capabilities)** atribuídas aos usuários, garantindo flexibilidade, rastreabilidade e independência de papéis fixos.

---

# Princípio

O sistema **não utiliza perfis fixos (roles rígidos)** como “admin”, “técnico”, etc.

Em vez disso, utiliza **capacidades granulares**, que definem exatamente o que um usuário pode fazer.

> Usuários não são papéis.
> Usuários possuem capacidades.

---

# Modelo de autorização

Cada usuário possui um conjunto de capabilities.

Exemplos:

* `chamado.abrir`
* `chamado.editar_itens`
* `chamado.alterar_prioridade`
* `chamado.executar`
* `chamado.liberar_nf`
* `chamado.liberar_coleta`
* `chamado.finalizar`
* `retorno.gerar`
* `cadastro.editar`
* `historico.visualizar`

---

# Princípios obrigatórios

### 1. Backend como fonte de verdade

* Toda validação de permissão ocorre no backend
* Templates/UI **não controlam segurança**
* UI apenas oculta ou exibe ações — nunca garante permissão

---

### 2. Negação por padrão

* Usuário sem capability → ação negada
* Não existe permissão implícita

---

### 3. Independência de contexto

Capabilities não dependem de tela, apenas de ação.

Exemplo:

* `chamado.editar_itens` funciona em qualquer lugar onde edição seja possível

---

# Aplicação nas operações

## Abertura de Chamado

Requer:

```
chamado.abrir
```

---

## Edição de itens após ABERTO

Requer:

```
chamado.editar_itens
```

---

## Alteração de prioridade

Requer:

```
chamado.alterar_prioridade
```

---

## Assumir execução

Requer:

```
chamado.executar
```

---

## Gates operacionais

Cada gate exige capability específica:

| Ação              | Capability               |
| ----------------- | ------------------------ |
| Liberar execução  | `chamado.executar`       |
| Liberar NF        | `chamado.liberar_nf`     |
| Liberar coleta    | `chamado.liberar_coleta` |
| Finalizar chamado | `chamado.finalizar`      |

---

## Geração de RETORNO

Requer:

```
retorno.gerar
```

---

## Cadastro mestre

| Ação                   | Capability                        |
| ---------------------- | --------------------------------- |
| Criar/editar entidades | `cadastro.editar`                 |
| Visualizar cadastro    | implícito a usuários autenticados |

---

## Histórico

Requer:

```
historico.visualizar
```

---

# Regras de execução

* Toda ação protegida deve validar capability antes de executar
* A validação ocorre no backend (views/services)
* Falha de permissão retorna erro explícito (ex: HTTP 403)

---

# Escopo de dados (opcional / futuro)

O sistema pode evoluir para controle de escopo:

Exemplo:

* usuário só vê determinadas lojas
* usuário só atua em determinados projetos

Isso deve ser tratado como extensão:

```
capability + escopo
```

Exemplo conceitual:

```
chamado.executar [loja=123]
```

---

# Auditoria

O sistema deve permitir rastrear:

* Quem executou cada ação
* Qual capability foi usada implicitamente

(Implementação via logs ou trilha de auditoria)

---

# Critérios de aceitação

* Todas as ações sensíveis validam capability no backend
* Usuário sem permissão recebe erro explícito
* UI não é responsável por segurança
* Capabilities são independentes de telas
* É possível adicionar novas capabilities sem alterar arquitetura
* Gates operacionais respeitam capabilities definidas
* Geração de RETORNO exige permissão específica

---

# Fonte

`web/auth/` *(ou equivalente de autenticação/autorização)*
`web/chamados/views.py`
`web/execucao/views.py`
RF-03 — Chamado de Retorno
RF-04 — Fila Operacional
RF-05 — Execução
RF-06 — Gates Operacionais

---

# Resultado

Com esse modelo você ganha:

* 🔒 Segurança real (não baseada em UI)
* 🧩 Flexibilidade total (sem refatorar roles)
* 📈 Escalabilidade organizacional
* 🧠 Clareza de responsabilidade por ação

---


---

# RF-11 — Rastreabilidade por Ativo

O sistema deve permitir rastrear completamente o ciclo de vida de cada ativo (equipamento com identificação única), registrando todas as suas movimentações entre lojas e sua participação em chamados ao longo do tempo.

---

# Princípio

O ativo é uma **entidade rastreável ao longo do tempo**.

> Um ativo não “pertence” a uma loja permanentemente.
> Ele está **em trânsito entre estados ao longo da operação**.

---

# Fonte de verdade

A rastreabilidade do ativo **não é armazenada diretamente**.

Ela é derivada de:

* Chamados
* Itens de chamado
* Execuções
* Eventos de finalização

> O histórico do ativo é uma **projeção**, assim como o histórico da loja.

---

# Identificação do ativo

Cada ativo rastreável deve possuir:

* Identificador único (ID interno)
* Número de série (quando aplicável)

Sem isso, não existe rastreabilidade.

---

# Linha do tempo do ativo

O sistema deve permitir visualizar a linha do tempo completa:

Exemplo:

```
[DATA] ENVIO → Loja A (Chamado #123)
[DATA] RETORNO → Matriz (Chamado #145)
[DATA] ENVIO → Loja B (Chamado #201)
```

---

# Eventos que compõem a linha do tempo

A linha do tempo do ativo deve ser composta por eventos derivados de chamados:

## 1. Participação em Chamado

* ID do chamado
* Tipo: ENVIO / RETORNO
* Loja de origem
* Loja de destino
* Data

---

## 2. Movimentação efetiva

A movimentação só é considerada válida quando o chamado é:

```id="8ptc6n"
FINALIZADO
```

Antes disso, o ativo está em estado transitório.

---

## 3. Estado atual do ativo

O sistema deve ser capaz de inferir:

* Em qual loja o ativo está atualmente
* Se está em trânsito (chamado não finalizado)
* Última movimentação registrada

---

# Regras de consistência

## 1. Um ativo não pode estar em dois lugares ao mesmo tempo

* Deve existir apenas um estado atual válido
* Conflitos devem ser impedidos no momento da operação

---

## 2. Movimentação depende de finalização

* Apenas chamados FINALIZADOS alteram a localização do ativo
* Chamados em andamento não alteram estado final

---

## 3. Ciclo infinito permitido

Um ativo pode passar por múltiplos ciclos:

```
ENVIO → RETORNO → ENVIO → RETORNO → ...
```

Sem perda de histórico.

---

## 4. Imutabilidade

Eventos passados não podem ser alterados.

Correções geram novos chamados.

---

# Consulta por ativo

O sistema deve permitir:

* Buscar por número de série
* Buscar por ID do ativo
* Visualizar histórico completo
* Visualizar estado atual

---

# Relação com Histórico da Loja (RF-09)

Ambos compartilham a mesma base de dados:

| Visão              | Foco                           |
| ------------------ | ------------------------------ |
| Histórico da Loja  | tudo que aconteceu na loja     |
| Histórico do Ativo | tudo que aconteceu com o ativo |

👉 São apenas **formas diferentes de agrupar os mesmos eventos**

---

# Projeções obrigatórias

O sistema deve suportar:

## 1. Projeção por Loja

* Agrupa por loja
* Mostra todos os chamados e eventos

## 2. Projeção por Ativo

* Agrupa por ativo
* Mostra movimentações e ciclos

---

# Critérios de aceitação

* Cada ativo possui identificação única
* Sistema permite consulta por ativo
* Linha do tempo do ativo é exibida corretamente
* Estado atual do ativo é inferido corretamente
* Movimentações só são confirmadas após FINALIZADO
* Um ativo não pode estar em múltiplas localizações simultaneamente
* Histórico não pode ser alterado
* Relação com chamados é preservada

---

# Fonte

`web/chamados/models.py`
`web/execucao/models.py`
RF-03 — Chamado de Retorno
RF-08 — Finalização
RF-09 — Histórico da Loja

---

# 💥 Insight importante (o mais importante daqui)


> **Chamado = evento**
>
> **Histórico = projeção**
>
> **Ativo e Loja = duas formas de enxergar os mesmos eventos**


---
<<<<<<< HEAD

=======
>>>>>>> 2016452 (docs: REQUIREMENTS.md e ARCHITECTURE.md)
