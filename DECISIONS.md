# DECISIONS — EXPANSÃO360

Este documento registra decisões técnicas e arquiteturais relevantes do projeto,
com o objetivo de evitar ambiguidades, manter rastreabilidade e facilitar onboarding.

## Formato padrão de cada decisão
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
O desenvolvimento seguirá por microtarefas com validação objetiva,
usando branches e commits pequenos.

**Contexto**  
Queremos previsibilidade, rastreabilidade e redução de retrabalho.

**Consequências**  
- Cada microtarefa deve resultar em um commit (quando aplicável).
- Push frequente após validação.
- Branches com nomes descritivos (`docs/`, `feat/`, `fix/`).

---

## 2026-01-20 — Branches base: main / develop

**Decisão**  
Usaremos:
- `main` para estabilidade e releases
- `develop` para integração contínua

**Contexto**  
Separar o que está pronto para release do que está em desenvolvimento reduz risco operacional.

**Consequências**  
- Mudanças entram via branches derivadas.
- `main` recebe apenas conteúdo estável.

---

## 2026-01-20 — Repositório stack-agnostic (fase inicial)

**Decisão**  
O projeto permanecerá neutro quanto a stack e framework no estágio inicial.

**Contexto**  
Evitar acoplamento prematuro permite decisões baseadas em requisitos reais.

**Consequências**  
- `.gitignore` genérico
- Nenhuma estrutura de framework antecipada
- Stack definida posteriormente via ADR

---

## 2026-01-21 — Stack Web definida: Django

**Decisão**  
A camada Web será implementada em **Django**.

**Contexto**  
Após estabilização do core e da CLI, era necessário um framework maduro
para UI, autenticação, ORM e velocidade de entrega.

**Consequências**  
- Core permanece independente
- Django atua como adapter
- Models Django não contêm regras de negócio

---

## 2026-01-21 — Nomenclatura em PT-BR no domínio

**Decisão**  
O domínio e casos de uso utilizam nomenclatura em português (PT-BR).

**Contexto**  
Reduzir carga cognitiva e aproximar o código do negócio real.

**Consequências**  
- Core em PT-BR
- Framework/infra seguem convenções originais
- Glossário mantido para consistência

---

## 2026-01-21 — Entidade operacional “Chamado”

**Decisão**  
O termo **Chamado** substitui “Card” como entidade operacional.

**Contexto**  
“Card” é ambíguo e visual. “Chamado” representa melhor uma unidade operacional.

**Consequências**  
- Domínio, CLI e Web utilizam “Chamado”
- Possíveis aliases temporários para compatibilidade

---

## 2026-01-21 — Equipamentos rastreáveis vs contáveis (`tem_ativo`)

**Decisão**  
Equipamentos são classificados como:
- **Rastreáveis** (`tem_ativo=True`)
- **Contáveis** (`tem_ativo=False`)

**Contexto**  
Nem todos os itens exigem ativo/número de série.

**Consequências**  
- Execução valida campos conforme tipo
- Relatórios diferenciam ativos e consumíveis

---

## 2026-01-21 — Layout base Web com Tailwind (CDN)

**Decisão**  
Adotar Tailwind via CDN e estrutura base de templates (`base`, `partials`, `components`).

**Contexto**  
Padronizar UI desde o início sem custo de build frontend.

**Consequências**  
- Layout tratado como decisão arquitetural
- Evita HTML duplicado e decisões visuais ad-hoc

---

## 2026-01-21 — Camada Web como adapter

**Decisão**  
A Web atua apenas como adapter (UI + persistência + orquestração).

**Contexto**  
Evitar migração de regras de negócio para a camada Web.

**Consequências**  
- Core independente
- CLI e Web compartilham domínio
- Facilita API e mobile no futuro

---

## 2026-01-21 — Fluxo inverso via novo Chamado (Loja → Matriz)

**Decisão**  
Correções e retornos geram **novo Chamado**, nunca edição destrutiva.

**Contexto**  
Chamados representam eventos operacionais e contábeis reais.

**Consequências**  
- Histórico imutável
- Retornos exigem desfecho explícito
- Auditoria e contabilidade preservadas

---

## 2026-01-22 — Evidências (anexos) por Chamado

**Decisão**  
Evidências são entidades próprias vinculadas a Chamados.

**Contexto**  
NF, Carta de Conteúdo e documentos de exceção são parte do processo real.

**Consequências**  
- Finalização pode exigir evidência
- Auditoria fortalecida
- Modelo extensível (fotos, assinaturas, etc.)

---

## 2026-01-22 — IAM mínimo por capabilities

**Decisão**  
Adoção de **Capability-Based Access Control** na camada Web.

**Contexto**  
Precisamos restringir ações sensíveis sem acoplar IAM ao domínio.

**Consequências**  
- Backend valida permissões
- Templates apenas refletem
- Core permanece permission-agnostic

---

## ADR — 2026-01-24 — CBVs + CapabilityRequiredMixin

**Status:** Aceito  
**Contexto:** Sprint 3 — Execução / Fluxo Inverso / IAM

**Decisão**
- Migrar views críticas para CBVs
- Centralizar autorização em `CapabilityRequiredMixin`

**Consequências**
- Menos repetição
- Padrão consistente
- Migração incremental segura

---

## 2026-01-24 — Abertura de Chamado via UI

**Decisão**  
Chamados podem ser abertos via UI, gerando automaticamente Itens de Execução
a partir do Kit (snapshot operacional).

**Contexto**  
Necessidade de testes end-to-end e uso real do sistema.

**Consequências**  
- Chamado nasce do Registry
- Itens são imutáveis conceitualmente
- Planejamento e execução ficam claramente separados

---

**Chamados sempre nascem como eventos operacionais derivados do Registry.**



---

## 2026-01-25 — Introdução de Subprojetos no Registry

**Decisão**  
Introduzir a entidade **Subprojeto** no **Registry (Cadastro Mestre)** como
recorte organizacional obrigatório quando existente, vinculado a um **Projeto**,
e referenciado por **Chamados** para fins de rastreabilidade, governança
e consolidação histórica.

**Contexto**  
Projetos reais de expansão (especialmente *ROLLOUT* e *ADIÇÃO*) exigem
segmentação operacional por linhas de entrega, fases, regiões ou áreas
(ex.: Sala Sua Saúde, Impressoras, Tablets).

Sem Subprojetos:
- o histórico fica dependente de texto livre
- dashboards exigem inferência ou regras frágeis
- não há governança explícita sobre “para onde” a execução está indo

A introdução de Subprojetos resolve esse problema sem violar o princípio
central do sistema: **Registry define intenção, Operation registra execução**.

**Consequências**
- Subprojeto passa a ser uma entidade do **Registry**, nunca da Operation.
- Todo Subprojeto pertence a exatamente um Projeto.
- Projetos podem existir sem Subprojetos.
- Quando um Projeto possuir Subprojetos cadastrados:
  - Chamados **devem** referenciar um Subprojeto válido e ativo.
- Alterações em Subprojetos (nome, status) **não afetam Chamados já existentes**.
- Subprojetos não são deletados destrutivamente se houver Chamados associados;
  apenas inativados ou encerrados.
- Dashboards e relatórios passam a operar por `Projeto → Subprojeto`
  sem inferência semântica.

---
## 2026-02-02 — Mapeamento operacional: “Filial” (base externa) como “Java” (UI) no Cadastro de Lojas

**Decisão**  
No cadastro de **Lojas (Registry)**, adotaremos a nomenclatura operacional utilizada no dia a dia:
- Exibir **Filial** como **Java** na UI e na comunicação com usuários.
- Exibir **Nome Filial** como **Nome loja** na UI.

Para compatibilidade com a base externa, o sistema deve aceitar o layout:
`Filial;Hist.;Nome Filial;Endereço;Bairro;Cidade;UF;Logomarca;Telefone;IP Banco 12`
e mapear esses campos para os atributos internos do cadastro de loja.

**Contexto**  
A base de dados externa/legada fornece campos com nomenclatura “Filial” e “Nome Filial”.
Na operação real, os usuários estão acostumados com os termos **Java** e **Nome loja**.
Até aqui o cadastro foi simplificado para acelerar desenvolvimento, mas agora precisamos
refinar para condizer com a realidade do dia a dia sem perder compatibilidade com a base.

**Consequências**  
- O importador/sincronização deve mapear explicitamente:
  - `Filial` → identificador da loja (exibido como “Java”)
  - `Nome Filial` → nome de exibição da loja (exibido como “Nome loja”)
  - demais colunas conforme layout oficial
- Templates e formulários devem refletir os labels operacionais (“Java”, “Nome loja”).
- Testes devem validar o mapeamento do layout e o recebimento correto dos campos no cadastro.
---
## 2026-02-02 — Padronização de Logomarca no Cadastro de Lojas

**Decisão**  
Padronizar o campo **Logomarca** no cadastro de Lojas para reduzir inconsistência:
- Normalizar valores para **maiúsculo** no salvamento.
- (Opcional) Preferir seleção via dropdown (RAIA/DROGASIL) no cadastro manual.

**Contexto**  
O valor de Logomarca vem padronizado na base externa (ex.: RAIA, DROGASIL),
mas no cadastro manual pode haver variações e erros de digitação.

## 2026-02-02 — Padronização de Logomarca no Cadastro de Lojas

**Decisão**  
Padronizar o campo **Logomarca** no cadastro de Lojas para reduzir inconsistência:
- Normalizar valores para **maiúsculo** no salvamento.
- (Opcional) Preferir seleção via dropdown (RAIA/DROGASIL) no cadastro manual.

**Contexto**  
O valor de Logomarca vem padronizado na base externa (ex.: RAIA, DROGASIL),
mas no cadastro manual pode haver variações e erros de digitação.

**Consequências**  
- Menos divergência de dados (RAIA/raia/RaIa).
- UI pode evoluir para dropdown sem afetar importação.
- Testes devem cobrir a normalização (quando aplicada).

---
## 2026-02-02 — Refinamento do Cadastro de Equipamentos (Registry)

### Decisão
O cadastro de **Equipamentos** será tratado como entidade de **Registry (Cadastro Mestre)**,
com foco em padronização, rastreabilidade e uso no dia a dia operacional.

O modelo deve representar:
- O que o equipamento **é**
- Como ele é **identificado**
- Em quais contextos ele pode ser **utilizado**

E **não**:
- Onde ele está instalado atualmente
- Eventos, histórico ou execução em campo

---

### Contexto
O cadastro atual de Equipamentos atende o CRUD básico, mas não reflete totalmente
o uso real no dia a dia operacional, gerando:
- Campos ambíguos
- Falta de validações importantes
- Dificuldade de reutilização em operações (Chamados, Instalações, Kits)

Assim como feito no refinamento de **Lojas**, queremos:
- Tornar o cadastro mais explícito
- Reduzir estados inválidos
- Garantir que o modelo represente a realidade do negócio

---

### Diretrizes adotadas

- Equipamento pertence ao **Registry**
- Equipamento **não depende** de Chamado, Instalação ou Loja para existir
- Identificação clara (ex: ativo, serial, tipo)
- Campos obrigatórios devem refletir uso real, não conveniência técnica
- Regras de negócio validadas **primeiro em testes**

---

### Consequências

- Ajustes em:
  - Model
  - Form
  - Testes
  - UI (somente após validação de domínio)
- Possível migração de dados
- Commits pequenos e rastreáveis
- Reuso do padrão já aplicado em Lojas
---
## 2026-02-02 — Padronização da estrutura de testes por camadas

### Decisão
Adotar uma estrutura de testes organizada por **camadas arquiteturais** (Domain, Application/Usecases e Interfaces),
para melhorar legibilidade, escalabilidade e onboarding.

Regras principais:
- Testes de **Domain** e **Usecases** ficam em `tests/` (framework-agnostic).
- Testes **Django/Web** ficam dentro de cada app Django, em `web/<app>/tests/`.
- Testes de **CLI** e smoke ficam em `tests/cli/`.
- A reorganização inicial será apenas de **movimentação/renomeação** (sem refatorar conteúdo),
mantendo o suite 100% verde durante todo o processo.

---

### Contexto
Atualmente os testes estão misturados entre:
- arquivos únicos por app (`web/<app>/tests.py`)
- testes do core em `tests/` com nomes variados
- um caminho inconsistente em `tests/expansao360/domain/test/...`

Mesmo com a suíte verde, a organização atual:
- dificulta localizar responsabilidades
- aumenta o custo de repetir padrões (ex.: Equipamentos, Kits, Chamados)
- atrapalha manutenção e leitura rápida do projeto

Queremos um layout onde seja possível entender o sistema “só olhando a árvore de testes”.

---

### Estrutura alvo

#### 1) Domain (regras puras)
`tests/domain/`
- `tests/domain/value_objects/`
- `tests/domain/entities/`
- `tests/domain/contracts/`

Regras:
- sem Django
- sem fixtures de banco
- foco em invariantes e regras do domínio

#### 2) Application / Usecases (orquestração)
`tests/usecases/`
- `tests/usecases/registry/`
- `tests/usecases/operation/`

Regras:
- valida fluxo e coordenação
- usa repositórios fake/in-memory quando necessário
- não testa detalhes de UI/framework

#### 3) Interfaces (Django Web)
`web/<app>/tests/`
- `test_models.py`
- `test_forms.py`
- `test_views.py` (ou `test_flows.py` quando fizer sentido)

Regras:
- testes Django ficam no app correspondente
- arquivos menores e mais específicos (evitar `tests.py` gigante)

#### 4) CLI e integração leve
`tests/cli/`
- `test_cli_smoke.py`
- `test_cli_errors.py`

---

### Consequências
- Melhor rastreabilidade por camada e responsabilidade
- Facilita criação de novos módulos (ex.: Equipamentos) mantendo padrão consistente
- Reduz “testes perdidos” e duplicidade conceitual
- Exige ajuste de imports e caminhos, mas sem mudar lógica de testes nesta fase
- Impõe disciplina: novos testes devem nascer no lugar correto

---

### Plano de adoção (incremental, com suíte verde)
A mudança será feita em microtarefas, com commits pequenos:
1) Criar diretórios e mover testes do Domain
2) Mover testes de Usecases
3) Organizar testes Django por app em `web/<app>/tests/`
4) Mover testes de CLI para `tests/cli/`
5) Ajustar `pytest`/imports e garantir `pytest` verde ao final de cada commit
