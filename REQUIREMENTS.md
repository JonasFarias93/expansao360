# Requisitos — EXPANSÃO360

## Contexto
O EXPANSÃO360 é uma plataforma para gestão de expansão e operação de campo,
baseada na separação clara entre:

- **Registry (Cadastro Mestre):**
  Define o que existe e como deve ser padronizado
  (ex.: lojas, projetos, kits, equipamentos).

- **Operation (Execução de Campo):**
  Registra o que foi executado na prática, com histórico,
  rastreabilidade e impacto operacional/contábil.

---

## Definições

- **Loja (Registry):**
  Unidade física cadastrada onde a execução ocorre.

- **Projeto / Subprojeto (Registry):**
  Contexto organizacional da execução.

- **Equipamento (Registry):**
  Item padronizado, podendo ser rastreável ou contável.

- **Kit (Registry):**
  Conjunto de equipamentos e quantidades previstos para execução.

- **Chamado (Operation):**
  Unidade central de execução operacional.
  Representa uma operação de envio, instalação ou retorno de itens,
  com status, histórico e validações.

- **Item de Execução (Operation):**
  Instância de um equipamento dentro de um Chamado,
  derivada de um Kit.

---

## Regras de Negócio (Core)

### RN-001 — Execução depende do cadastro mestre
Um Chamado **só pode ser criado** se existir:
- Loja válida
- Projeto válido
- Kit válido

**Critério de Aceite**
- Dado que algum cadastro obrigatório não exista,
  quando tentar criar um Chamado,
  então o sistema deve **recusar** a criação.

---

### RN-002 — Geração automática de itens de execução
Ao criar um Chamado associado a um Kit,
o sistema deve gerar automaticamente os itens de execução
conforme o cadastro do Kit.

**Critério de Aceite**
- Cada ItemKit gera um Item de Execução correspondente.
- Quantidade e tipo devem ser preservados.

---

### RN-003 — Rastreabilidade por tipo de equipamento
Equipamentos são classificados como:

- **Rastreáveis (`tem_ativo=True`)**
  - Exigem Ativo e Número de Série.

- **Contáveis (`tem_ativo=False`)**
  - Exigem confirmação explícita de execução.

**Critério de Aceite**
- Chamado não pode ser finalizado se:
  - Item rastreável estiver sem Ativo ou Série.
  - Item contável não estiver confirmado.

---

### RN-004 — Workflow de status do Chamado
Todo Chamado segue o fluxo:

**Critério de Aceite**
- Um Chamado inicia como **ABERTO**.
- Ao salvar itens, passa para **EM_EXECUCAO**.
- Apenas Chamados válidos podem ser **FINALIZADOS**.

---

### RN-005 — Identificação e rastreabilidade do Chamado
Todo Chamado deve possuir:
- Protocolo único gerado automaticamente
- Referências externas únicas (quando informadas):
  - ServiceNow
  - Contabilidade
  - NF de saída

**Critério de Aceite**
- Protocolos não podem se repetir.
- Referências externas não podem ser duplicadas.

---

### RN-006 — Fluxo inverso de execução (retorno)
Quando for necessário corrigir uma execução ou retornar itens,
o sistema deve registrar um **novo Chamado**,
representando o fluxo inverso (**Loja → Matriz**).

**Critério de Aceite**
- Chamados finalizados não são reabertos.
- Chamados de retorno devem referenciar o Chamado de origem.
- A finalização do retorno exige decisão explícita:
  - Retornado para matriz
  - Não retornado (extravio / exceção)

---

## Observações
- O core de domínio permanece independente de frameworks.
- Interfaces (CLI / Web / futuras APIs) apenas orquestram casos de uso.
- Persistência pode variar sem impacto nas regras de negócio.
