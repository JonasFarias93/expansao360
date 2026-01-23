# REQUIREMENTS — EXPANSÃO360

## 1. Contexto

O **EXPANSÃO360** é uma plataforma para gestão de **expansão e operação de campo**,
projetada para garantir **governança, rastreabilidade e auditoria** em operações
logísticas e técnicas.

O sistema é baseado na separação explícita entre:

- **Registry (Cadastro Mestre)**  
  Define *o que existe* e *como deve ser padronizado*
  (lojas, projetos, equipamentos, kits).

- **Operation (Execução de Campo)**  
  Registra *o que foi executado na prática*, com histórico imutável,
  evidências e impacto operacional e contábil.

---

## 2. Definições de Domínio

- **Loja (Registry)**  
  Unidade física onde a execução ocorre.

- **Projeto / Subprojeto (Registry)**  
  Contexto organizacional da execução.

- **Equipamento (Registry)**  
  Item padronizado, classificado como:
  - rastreável (`tem_ativo=True`)
  - contável (`tem_ativo=False`)

- **Kit (Registry)**  
  Conjunto padronizado de equipamentos, tipos, quantidades
  e regras de configuração.

- **ItemKit (Registry)**  
  Associação entre Kit e Equipamento, definindo:
  - tipo
  - quantidade
  - se requer configuração técnica naquele contexto.

- **Chamado (Operation)**  
  Unidade central da execução operacional.
  Representa uma operação de envio, instalação ou retorno,
  com status, validações e histórico.

- **Item de Execução (Operation)**  
  Snapshot operacional de um ItemKit dentro de um Chamado,
  representando o estado real da execução.

- **Evidência (Operation)**  
  Documento ou arquivo que comprova a execução
  (NF, Carta de Conteúdo, exceção).

---

## 3. Requisitos Funcionais (Core)

### RF-001 — Criação de Chamado depende do Cadastro Mestre

Um Chamado **só pode ser criado** se existirem:
- Loja válida
- Projeto válido
- Kit válido

**Critério de Aceite**
- Dado que algum cadastro obrigatório não exista,
  quando tentar criar um Chamado,
  então o sistema deve **recusar** a criação.

---

### RF-002 — Geração automática de Itens de Execução

Ao acessar um Chamado associado a um Kit,
o sistema deve gerar automaticamente os Itens de Execução
com base no Kit.

**Critério de Aceite**
- Cada ItemKit gera um Item de Execução correspondente.
- Quantidade, tipo e regras são preservadas.
- A geração ocorre apenas uma vez por Chamado.

---

### RF-003 — Snapshot operacional imutável

Os Itens de Execução devem armazenar um **snapshot**
do estado do cadastro no momento da execução.

**Critério de Aceite**
- Alterações futuras no Registry não afetam Chamados existentes.
- Itens de Execução não refletem mudanças posteriores no Kit ou Equipamento.

---

### RF-004 — Rastreabilidade por tipo de equipamento

Equipamentos são classificados como:

- **Rastreáveis (`tem_ativo=True`)**
  - Exigem Ativo e Número de Série.

- **Contáveis (`tem_ativo=False`)**
  - Exigem confirmação explícita da execução.

**Critério de Aceite**
- Um Chamado não pode ser finalizado se:
  - existir item rastreável sem Ativo ou Série;
  - existir item contável não confirmado.

---

### RF-005 — Controle de configuração técnica por item

Itens podem exigir configuração técnica,
definida no contexto do Kit.

Estados possíveis:
- AGUARDANDO
- EM_CONFIGURACAO
- CONFIGURADO

**Critério de Aceite**
- Apenas itens marcados como configuráveis possuem status.
- O Chamado não pode ser finalizado enquanto
  houver itens configuráveis não configurados.

---

### RF-006 — Workflow de status do Chamado

Todo Chamado segue o fluxo:


**Critério de Aceite**
- Chamado inicia como **ABERTO**.
- Ao salvar itens, passa para **EM_EXECUCAO**.
- Apenas Chamados válidos podem ser **FINALIZADOS**.
- Chamados finalizados tornam-se imutáveis.

---

### RF-007 — Identificação e unicidade do Chamado

Todo Chamado deve possuir:
- Protocolo único gerado automaticamente.
- Referências externas únicas (quando informadas):
  - ServiceNow
  - Contabilidade
  - NF de saída

**Critério de Aceite**
- Protocolos não podem se repetir.
- Referências externas não podem ser duplicadas.

---

### RF-008 — Evidências por Chamado

O sistema deve permitir anexar evidências a um Chamado.

Tipos iniciais:
- NF de saída
- NF de retorno
- Carta de Conteúdo
- Documento de exceção

**Critério de Aceite**
- Evidências ficam vinculadas ao Chamado.
- Evidências não podem ser removidas após finalização.
- Evidências são visíveis no detalhe do Chamado.

---

### RF-009 — Regra de finalização com evidências

A finalização de um Chamado pode exigir evidência,
dependendo do tipo de fluxo.

**Critério de Aceite**
- Chamados de retorno exigem decisão explícita:
  - retorno confirmado
  - não retornado (extravio / exceção)

---

### RF-010 — Fluxo inverso de execução (Loja → Matriz)

Quando houver correção ou retorno de itens,
o sistema deve criar **um novo Chamado**.

**Critério de Aceite**
- Chamados finalizados não podem ser reabertos.
- Chamados de retorno referenciam o Chamado original.
- O histórico do Chamado original permanece imutável.

---

### RF-011 — IAM mínimo baseado em capacidades

O sistema deve suportar permissões mínimas para ações críticas.

Capacidades iniciais:
- CONFIGURAR_ITEM
- TRAVAR_CONFIGURACAO
- EXECUTAR_ITEM
- FINALIZAR_EXECUCAO
- VISUALIZAR_HISTORICO

**Critério de Aceite**
- Usuários sem capacidade não podem executar ações sensíveis.
- A UI apenas reflete permissões; não decide regras.

---

## 4. Requisitos Não Funcionais

### RNF-001 — Imutabilidade operacional
- Chamados finalizados não podem ser alterados.
- Correções exigem nova execução.

### RNF-002 — Auditoria e rastreabilidade
- Todas as operações relevantes são registradas.
- Histórico completo deve ser preservado.

### RNF-003 — Independência de framework
- O core de domínio não depende de Django ou outras interfaces.

### RNF-004 — Evolução segura
- O sistema deve permitir evolução (API, mobile, RBAC)
  sem refatoração estrutural.

---

## 5. Fora de Escopo (neste momento)
- API pública
- Mobile
- RBAC avançado
- Eventos assíncronos
- Versionamento explícito de configuração

Esses itens estão **arquiteturalmente previstos**,
mas não implementados.

---

## 6. Observações Finais
- Interfaces (Web / CLI) apenas orquestram casos de uso.
- Regras de negócio pertencem ao domínio.
- Todas as decisões relevantes estão registradas em `DECISIONS.md`.
