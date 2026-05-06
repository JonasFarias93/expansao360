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
- Tipo: ENVIO (Matriz → Loja) ou RETORNO (Loja → Matriz)
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

## RF-03 — Separação entre Setup e Execução

O Chamado deve possuir estágio explícito de planejamento (`EM_ABERTURA`)
distinto da execução.

Regras:

* Chamado nasce em `EM_ABERTURA`
* Após salvar setup → promovido para `ABERTO`
* Apenas Chamados `ABERTO` em diante aparecem na fila

Fonte:

* `web/execucao/views.py`

---

## RF-04 — Execução em Fila Operacional

O sistema deve permitir execução de Chamados por meio de fila operacional.

Critério de aceitação:

* Chamados `ABERTO+` aparecem na fila
* Templates não contêm regra de negócio

Fonte:

* `web/execucao/templates/`

---

## RF-05 — Evidências vinculadas ao Chamado

O sistema deve permitir anexar evidências a Chamados.

Exemplos:

* Nota Fiscal
* Carta de Conteúdo
* Documentos de exceção

Critério de aceitação:

* Evidência é entidade própria
* Vinculada a um Chamado

Fonte:

* `web/execucao/models.py`

---

## RF-06 — Gates Operacionais

Transições de estado devem ser protegidas por validações objetivas.

Exemplos:

* Liberação de NF exige itens válidos
* Finalização exige pré-condições
* Edição exige sessão ativa

Critério de aceitação:

* Tentativa inválida é bloqueada no backend

Fonte:

* `web/execucao/views.py`
* `web/execucao/tests/`

---

## RF-07 — Fluxo Direto e Inverso

O sistema deve suportar:

* ENVIO (Matriz → Loja)
* RETORNO (Loja → Matriz)

Critério de aceitação:

* Retorno gera novo Chamado
* Histórico não é apagado

Fonte:

* `web/execucao/models.py`

---

## RF-08 — Imutabilidade Operacional

Chamados finalizados não devem ser alterados destrutivamente.

Critério de aceitação:

* Correções geram novo Chamado
* Finalizado permanece histórico

---

## RF-09 — Chamado Externo

O sistema deve permitir registrar identificador externo.

Critério de aceitação:

* `ticket_externo_id` único quando preenchido
* UI exibe formato padronizado

Fonte:

* `web/execucao/models.py`

---

## RF-10 — Autorização por Capabilities

A camada Web deve aplicar autorização baseada em capabilities.

Critério de aceitação:

* Enforcement no backend
* Templates apenas refletem permissões

Fonte:

* `web/iam/`

---

# 3. Requisitos Não Funcionais

## RNF-01 — Separação Arquitetural

O sistema deve manter:

* Domínio independente de Django
* Web como adapter
* Regras fora de templates

Verificação:

* Inspeção arquitetural
* Testes de domínio

---

## RNF-02 — Qualidade de Código (Python)

O projeto deve usar:

* ruff
* black
* pre-commit

Verificação:

* Hooks ativos
* Execução local/CI

---

## RNF-03 — Testes Automatizados (Python)

O projeto deve usar:

* pytest
* pytest-django
* pytest-cov (quando configurado)

Verificação:

* Suíte executável via comando único (`make test-py`)

---

## RNF-04 — Testes JS

O projeto deve testar JavaScript crítico com:

* Jest
* jsdom

Verificação:

* Testes presentes em `web/**/__tests__/`

---

## RNF-05 — Auditoria de Dependências Python

O projeto deve possuir auditoria automatizada para detectar:

* Dependências declaradas e não utilizadas
* Imports utilizados sem dependência declarada

Ferramenta adotada:

* `deptry`

Verificação:

* Execução via `make deps-check`
* Falhas devem ser corrigidas antes de merge

---

# 4. Restrições Técnicas

## RT-01 — Runtime

* Python 3.11
* Ambiente gerenciado por Conda (`environment.yml`)

## RT-02 — Framework Web

* Django

## RT-03 — Frontend leve

* Sem build obrigatório
* Tailwind via CDN

## RT-04 — Tooling JS

* Node/npm apenas para testes JS
* Não faz parte do runtime de produção

---

# 5. Baseline de Dependências

Dependências principais (runtime Python):

* Django
* python-dotenv

Dependências de teste (extra `[test]` no `pyproject.toml`):

* pytest
* pytest-django
* pytest-cov
* psycopg[binary]

Ferramentas de desenvolvimento (extra `[dev]` no `pyproject.toml`):

* ruff
* black
* pre-commit
* deptry

JS (dev):

* Jest
* jsdom

Fonte definitiva:

* Python: `pyproject.toml`
* Base Conda: `environment.yml`
* JS: `package.json` / `package-lock.json`

Snapshots (artefatos gerados, não fonte de verdade):

* `docs/deps/environment.snapshot.yml`
* `docs/deps/pip-freeze.snapshot.txt`

---

# 6. Fora de Escopo Atual

* APIs públicas
* Integrações corporativas
* Multitenancy
* Infra hardening avançado
* Mobile/offline-first

---

# 7. Governança

Se um requisito mudar:

* Atualizar este documento no mesmo PR
* Criar ou atualizar ADR quando necessário

---

**Última revisão:** 2026-02-13
**Fonte:** Código real em `web/` + testes automatizados + `pyproject.toml` + `environment.yml`
