# Requisitos — EXPANSÃO360

## 1. Contexto

O **EXPANSÃO360** é uma plataforma para gestão de expansão e operação de campo,
baseada na separação clara e intencional entre:

### Registry (Cadastro Mestre)
Define **o que existe** e **como deve ser padronizado**.

Exemplos:
- Lojas
- Projetos e Subprojetos
- Equipamentos
- Kits e seus itens

### Operation (Execução de Campo)
Registra **o que foi executado na prática**, com histórico,
rastreabilidade e impacto operacional e contábil.

Exemplos:
- Chamados
- Itens de Execução
- Evidências
- Fluxos diretos e inversos

---

## 2. Definições de Domínio

### Loja (Registry)
Unidade física cadastrada onde a execução ocorre.

---

### Projeto / Subprojeto (Registry)
Contexto organizacional da execução.

- **Projeto**: iniciativa macro (ex.: rollout, refresh, piloto).
- **Subprojeto**: recorte operacional do projeto (ex.: fase, região, tipo de loja).

> Detalhamento funcional do Subprojeto será definido em etapa posterior.

---

### Equipamento (Registry)
Item padronizado utilizado na execução.

Classificação:
- **Rastreável (`tem_ativo=True`)**
- **Contável (`tem_ativo=False`)**

---

### Kit (Registry)
Conjunto padronizado de equipamentos e quantidades
previstos para execução.

O Kit representa **planejamento aprovado**.

---

### Chamado (Operation)
Unidade central de execução operacional.

Representa:
- Envio
- Instalação
- Retorno
- Correção operacional

Possui status, histórico, itens e evidências.

---

### Item de Execução (Operation)
Instância operacional de um equipamento dentro de um Chamado,
gerada automaticamente a partir de um Kit.

Funciona como um **snapshot operacional** do planejamento.

---

## 3. Regras de Negócio (Core)

### RN-001 — Execução depende do cadastro mestre

Um Chamado **só pode ser criado** se existirem previamente:

- Loja válida
- Projeto válido
- Kit válido

**Critério de Aceite**
- Dado que algum cadastro obrigatório não exista  
- Quando tentar criar um Chamado  
- Então o sistema deve **recusar** a criação  

---

### RN-002 — Geração automática de Itens de Execução

Ao criar um Chamado associado a um Kit,
o sistema deve gerar automaticamente os Itens de Execução
com base nos Itens do Kit.

**Critério de Aceite**
- Cada `ItemKit` gera exatamente um `Item de Execução`.
- Equipamento, tipo, quantidade e flags devem ser preservados.
- Alterações futuras no Kit **não impactam Chamados já criados**.

---

### RN-003 — Rastreabilidade por tipo de equipamento

Equipamentos são classificados como:

#### Rastreáveis (`tem_ativo=True`)
- Exigem:
  - Ativo
  - Número de Série

#### Contáveis (`tem_ativo=False`)
- Exigem confirmação explícita de execução.

**Critério de Aceite**
- Um Chamado **não pode ser finalizado** se:
  - existir Item rastreável sem Ativo ou Série
  - existir Item contável não confirmado

---

### RN-004 — Workflow de status do Chamado

Todo Chamado segue o fluxo básico:

- **ABERTO**
- **EM_EXECUCAO**
- **FINALIZADO**

**Critério de Aceite**
- Todo Chamado inicia em **ABERTO**.
- Ao salvar itens, pode transitar para **EM_EXECUCAO**.
- Apenas Chamados válidos podem ser **FINALIZADOS**.

---

### RN-005 — Identificação e rastreabilidade do Chamado

Todo Chamado deve possuir:

- Protocolo único (gerado automaticamente)
- Referências externas únicas (quando informadas):
  - ServiceNow
  - Contabilidade
  - NF de saída

**Critério de Aceite**
- Protocolos não podem se repetir.
- Referências externas não podem ser duplicadas no sistema.

---

### RN-006 — Fluxo inverso de execução (retorno)

Correções ou retornos **não alteram Chamados finalizados**.

Um novo Chamado deve ser criado,
representando o fluxo inverso (**Loja → Matriz**).

**Critério de Aceite**
- Chamados finalizados são imutáveis.
- Chamados de retorno:
  - referenciam o Chamado de origem
  - exigem decisão explícita na finalização:
    - Retornado para a matriz
    - Não retornado (extravio / perda / exceção)

---

### RN-007 — Evidências por Chamado

Chamados podem (ou devem) possuir evidências,
conforme o tipo de operação.

Exemplos:
- NF de saída
- NF de retorno
- Carta de Conteúdo
- Documento de exceção

**Critério de Aceite**
- Evidências ficam vinculadas ao Chamado.
- Chamados de retorno exigem evidência ou decisão explícita.

---

## 4. Princípios Não Funcionais

- O core de domínio **não depende de frameworks**.
- Interfaces (CLI / Web / futuras APIs):
  - apenas orquestram casos de uso
  - não contêm regras de negócio
- Persistência pode variar sem impacto nas regras do core.
- Histórico operacional **nunca é apagado**.

---

## 5. Fora de Escopo (por enquanto)

- Campos definitivos de Subprojeto
- Regras específicas por tipo de Projeto
- Integração com ERP / ServiceNow
- API pública
- Mobile / offline-first
