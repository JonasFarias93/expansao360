# DECISIONS — EXPANSÃO360

Este documento registra decisões técnicas e arquiteturais relevantes, com o objetivo de
evitar ambiguidades, manter rastreabilidade e facilitar onboarding.

Formato recomendado:
- Data (YYYY-MM-DD)
- Decisão
- Contexto
- Consequências

---

## 2026-01-20 — Separação conceitual: Registry x Operation

**Decisão**  
O sistema será modelado com duas camadas conceituais principais:
- **Registry (Cadastro Mestre)**: define “o que existe” e “como deve ser”
- **Operation (Execução de Campo)**: registra “o que foi executado”, com rastreabilidade e histórico

**Contexto**  
Precisamos garantir governança sobre padrões e, ao mesmo tempo, registrar a execução real em campo
sem poluir o cadastro mestre e sem perder histórico.

**Consequências**  
- Operation referencia Registry; Registry não depende de Operation.
- O domínio será desenhado para suportar auditoria e evolução segura.

---

## 2026-01-20 — Estratégia de trabalho: microtarefas + disciplina de versionamento

**Decisão**  
O desenvolvimento seguirá por microtarefas com validação objetiva, usando branches e commits pequenos.

**Contexto**  
Queremos previsibilidade, rastreabilidade e redução de retrabalho.

**Consequências**  
- Cada microtarefa deve resultar em um commit (quando aplicável).
- Push frequente após validação.
- Nomes de branches descritivos (ex: `docs/init`, `feat/...`, `fix/...`).

---

## 2026-01-20 — Branches base: main / develop

**Decisão**  
Usaremos:
- `main` para estabilidade e releases
- `develop` para integração contínua

**Contexto**  
Separar o que está pronto para release do que está em desenvolvimento reduz risco operacional.

**Consequências**  
- Mudanças entram via branches derivadas e são integradas em `develop`.
- `main` recebe apenas conteúdo estável e controlado.


---

## 2026-01-20 — Repositório stack-agnostic (sem framework definido)

**Decisão**  
O projeto permanecerá intencionalmente neutro quanto a stack e framework neste estágio inicial.

**Contexto**  
Durante a preparação do ambiente (Sprint 1), optou-se por evitar acoplamento prematuro a tecnologias
específicas (ex: Django, FastAPI, Node, etc.), permitindo que decisões sejam tomadas com base
em requisitos reais e não por conveniência inicial.

**Consequências**  
- `.gitignore` permanece genérico (Python / Node / OS).
- Nenhuma estrutura de framework é criada antecipadamente.
- A definição de stack será registrada explicitamente em decisão futura.


---

## 2026-01-21 — Stack web definida: Django

**Decisão**  
A camada web do EXPANSÃO360 será implementada utilizando Django.

**Contexto**  
Após a estabilização do core e da CLI, foi necessário definir um framework web
para fornecer interface de usuário, autenticação, persistência e administração.
Django foi escolhido pela maturidade, ecossistema, ORM integrado e velocidade
de entrega para CRUDs e RBAC.

**Consequências**  
- O core permanece independente de framework.
- Django atua apenas como camada de entrega (web/adapters).
- Models Django não contêm regras de negócio.

---

## 2026-01-21 — Nomenclatura em PT-BR no domínio

**Decisão**  
O domínio (core) e os casos de uso utilizarão nomenclatura em português (PT-BR).
A camada web seguirá as convenções do framework (Django).

**Contexto**  
Para reduzir carga cognitiva e facilitar entendimento das regras de negócio,
optou-se por usar português no domínio, mantendo inglês apenas onde imposto
por frameworks, bibliotecas ou padrões consolidados.

**Consequências**  
- Entidades, casos de uso e mensagens do core usam PT-BR.
- Infraestrutura e framework mantêm convenções originais.
- Um glossário será mantido para garantir consistência terminológica.


---

## 2026-01-21 — Entidade operacional “Chamado” substitui “Card”

**Decisão**  
A entidade anteriormente referida como “Card” passa a se chamar **Chamado** no domínio do sistema.

**Contexto**  
O termo “Card” é genérico e pode causar ambiguidade com elementos visuais da interface.
“Chamado” é um termo consolidado em contextos operacionais e de TI, representando uma
unidade de trabalho com status, histórico e rastreabilidade.

**Consequências**  
- O domínio e os casos de uso passam a utilizar o termo “Chamado”.
- A CLI e a Web expõem o conceito como “Chamado”.
- Caso necessário, aliases temporários podem ser mantidos para compatibilidade.

---
## 2026-01-21 — Equipamentos rastreáveis vs contáveis (`tem_ativo`)

**Decisão**  
Equipamentos passam a ser classificados como:
- **Rastreáveis** (`tem_ativo=True`): exigem Ativo e Número de Série na execução.
- **Contáveis** (`tem_ativo=False`): não possuem Ativo/Série, apenas confirmação e contagem.

**Contexto**  
Alguns itens (ex.: micro, monitor) exigem rastreabilidade individual,
enquanto outros (ex.: hub USB, cabos) precisam apenas ser contabilizados
para controle de consumo e estatísticas.

**Consequências**  
- O cadastro do Equipamento define se ele é rastreável ou contável.
- A execução (Chamado) valida campos obrigatórios conforme `tem_ativo`.
- Relatórios podem diferenciar ativos físicos de consumíveis.

---

## 2026-01-21 — Layout base web com Tailwind e estrutura de templates

**Decisão**  
A camada web do EXPANSÃO360 adotará um layout base padronizado utilizando Tailwind CSS via CDN, com uma estrutura fixa de templates composta por base.html, partials/ e components/.

**Contexto**  
Com a estabilização do core e da CLI, iniciou-se a implementação da camada web em Django.
Era necessário definir uma estrutura de layout consistente desde o início para evitar duplicação de HTML, decisões visuais ad-hoc e divergência entre apps (cadastro, execucao, iam).
Além disso, optou-se por uma solução de baixo custo inicial para estilização, permitindo foco no fluxo e nas regras antes de investir em pipeline de build de frontend.

**Consequências**
- Todas as páginas web herdam de `base.html`.
- Fragmentos reutilizáveis ficam concentrados em `partials/`.
- Elementos de UI mais semânticos e reutilizáveis ficam em `components/`.
- Tailwind via CDN reduz o custo inicial de setup.
- O layout passa a ser tratado como decisão arquitetural explícita, evitando reavaliações constantes.



---


## 2026-01-21 — Camada Web como adapter (UI e persistência)

**Decisão**  
A camada Web do EXPANSÃO360 será tratada exclusivamente como um adapter,
responsável por interface de usuário, orquestração de casos de uso e persistência,
sem conter regras de negócio do domínio.

**Contexto**  
Com a evolução do projeto, passaram a coexistir múltiplas interfaces
(CLI e Web). Era necessário registrar explicitamente que o core de domínio
permanece independente de frameworks, evitando que regras de negócio
migrem para a camada web por conveniência.

**Consequências**  
- Regras de negócio permanecem no core.
- A Web (Django) atua apenas como camada de entrega.
- CLI e Web compartilham o mesmo domínio e casos de uso.
- Facilita testes, manutenção e evolução futura (API, mobile, etc.).



---

## 2026-01-21 — Fluxo inverso de execução (Loja → Matriz) via novo Chamado

**Decisão**  
Quando um Chamado finalizado precisar de correção operacional ou retorno de itens
para a matriz, o sistema **não permitirá edição destrutiva do histórico**.
Em vez disso, será criado **um novo Chamado**, representando o fluxo inverso
(**Loja → Matriz**), vinculado ao Chamado original.

Além disso, Chamados de retorno possuirão **regras específicas de finalização**,
exigindo confirmação explícita do destino dos itens (retorno efetivo ou exceção).

---

**Contexto**  
Chamados representam eventos operacionais e contábeis com impacto real
(rastreabilidade, ativos, NF, contabilidade).
Permitir reabertura ou edição direta de um Chamado finalizado quebraria:
- rastreabilidade histórica
- consistência contábil
- auditoria de processos

Na prática, quando um item apresenta problema após a execução
(ex.: defeito, devolução, erro de envio),
o processo correto é um **retorno físico e contábil** do item,
que precisa ser registrado como **uma nova operação**.

Adicionalmente, retornos podem:
- demorar para acontecer
- não acontecer (extravio, perda, descarte)
- ficar esquecidos em status intermediário

Era necessário garantir que o sistema:
- evidencie retornos pendentes
- force uma decisão explícita
- evite chamados “abertos para sempre” sem resolução clara

---

**Consequências**  

### 1) Criação de novo Chamado
- Chamados finalizados permanecem imutáveis.
- Correções geram um **novo Chamado**.
- O novo Chamado:
  - representa o fluxo **Loja → Matriz**
  - referencia explicitamente o Chamado de origem

---

### 2) Regra de finalização para Chamado de retorno
Chamados do tipo **Loja → Matriz** **não podem ser finalizados automaticamente**.

Para finalizar, será obrigatório indicar **o desfecho dos itens**, com uma das opções:

- **Retorno confirmado para a matriz**
- **Não retornado (extravio / perda / descarte / exceção)**

Essa decisão:
- é explícita
- é registrada
- não pode ser omitida

---

### 3) Auditoria e governança
- Chamados de retorno pendentes ficam visíveis no sistema
- Evita esquecimento de retornos abertos
- Permite relatórios claros:
  - itens retornados
  - itens não retornados
  - perdas / exceções operacionais

---

### 4) Contabilidade e rastreabilidade
- A contabilidade passa a ter dois registros claros:
  - envio (Matriz → Loja)
  - retorno ou baixa (Loja → Matriz)
- O sistema mantém histórico completo, sem reprocessamento destrutivo.
- A UI poderá exibir, no Chamado original, um atalho para o Chamado de retorno.


---

## 2026-01-22 — Evidências (anexos) por Chamado

**Decisão**  
O sistema permitirá o upload e a gestão de **evidências (anexos)** vinculadas a um Chamado,
como forma de comprovação operacional e contábil.
Essas evidências serão utilizadas tanto no fluxo normal
(**Matriz → Loja**) quanto no fluxo inverso (**Loja → Matriz**).

---

**Contexto**  
Durante a execução e o retorno de itens, é comum a existência de documentos físicos,
como:
- Nota Fiscal (NF)
- Carta de Conteúdo assinada na coleta
- Outros documentos de exceção (extravio, perda, descarte)

Nem toda operação gera NF, especialmente quando envolve itens contáveis
(sem ativo), como teclados, mouses e suportes.
Nesses casos, a **Carta de Conteúdo** é a evidência válida da movimentação.

Era necessário que o sistema:
- armazenasse essas evidências
- mantivesse vínculo com o Chamado
- evitasse esquecimento de operações pendentes
- suportasse exceções sem perder rastreabilidade

---

**Consequências**  

### 1) Evidências como entidade própria
- Evidências serão registradas como entidades próprias,
  vinculadas a um Chamado.
- Cada evidência terá:
  - tipo (ex.: NF, Carta de Conteúdo, Exceção)
  - arquivo anexado
  - data de registro

---

### 2) Tipos de evidência suportados
Inicialmente, o sistema suportará:
- NF de saída
- NF de retorno
- Carta de Conteúdo
- Documento de exceção (extravio, perda, descarte)

---

### 3) Regra de finalização com evidências
- A finalização de um Chamado poderá exigir pelo menos uma evidência,
  conforme o tipo de fluxo.
- Para Chamados de retorno (Loja → Matriz),
  será obrigatória a indicação explícita do desfecho:
  - retorno confirmado
  - não retornado (extravio / exceção)

---

### 4) Governança e auditoria
- Evidências ficam visíveis no detalhe do Chamado.
- Evita Chamados finalizados sem comprovação.
- Mantém histórico completo para auditoria e contabilidade.

---

### 5) Evolução futura
- O mecanismo de evidências poderá ser reutilizado
  para fotos, assinaturas, termos ou outros documentos,
  sem alteração do modelo conceitual.
