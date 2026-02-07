# TODO Arquitetural — Integração de Grupos de Rede com Cadastro e Execução

Este documento registra **passos futuros já decididos**, evitando rediscussão e garantindo a evolução consistente do domínio de redes, agora focado no conceito de **Grupos de Rede**.

---

## 1. Onde entra no fluxo (Evolução do Conceito)

### Cadastro (Registry)

* `TipoEquipamento` representa o **tipo lógico** (PDV, TC, CONSULTA_PRECO).
* O cadastro **não possui índices ou instâncias**.

### Grupos de Rede (ex-RegraRedeEquipamento)

* Define o **papel completo** de um conjunto de equipamentos na rede.
* O **Grupo de Rede** passa a ser a fonte da verdade para:

  * Política de IP (offset / faixa)
  * Máscara
  * Gateway
  * Padrão de hostname

### Execução (Operation)

* A **instância real** nasce na execução (ex.: PDV #1).
* O **índice da instância** (definido na execução) é aplicado às regras do Grupo de Rede para derivar os dados finais.
* A execução consulta:

  * Perfil de rede ativo da loja (ex.: LEGACY vs SEGMENTADO)
  * Grupo de Rede vinculado ao tipo de equipamento
  * Índice da instância para cálculo de offsets e composição de hostname

---

## 2. Premissa de Instâncias e Índices

* **Índice sempre pertence à execução**, nunca ao cadastro.
* Equipamentos como `PDV1`, `PDV2` e `PDV3` são **instâncias** de um mesmo Grupo de Rede.
* Manter essa separação:

  * evita explosão de registros no cadastro
  * preserva o domínio como **documentação viva da topologia de rede**
  * evita tratar ativos físicos como entidades de planejamento

---

## 3. Validações Multidimensionais (WARN → ERROR)

A validação deixa de ser apenas sobre endereço IP e passa a cobrir o **papel completo na rede**, prevenindo inconsistências operacionais.

### Fase atual (MVP)

* Validação de **IP, Máscara e Gateway** roda como **service puro**.
* `WARN` **não bloqueia** a execução.

### Fase futura (Grupos de Rede estabilizados)

Quando `TipoEquipamento` estiver vinculado a um Grupo de Rede:

* **ERROR (bloqueante)**:

  * IP fora da regra
  * Máscara divergente do Grupo de Rede
  * Gateway divergente do Grupo de Rede

* **WARN**:

  * Erros de digitação leves
  * Padrões de hostname inconsistentes (dependendo da criticidade)

O objetivo é capturar erros de **conhecimento implícito** (ex.: IP correto com gateway errado) **antes da conclusão da execução**.

---

## 4. Critério para avançar para implementação

A implementação de automação e bloqueios **só deve ocorrer** quando:

* O cadastro de **Grupos de Rede** estiver descrevendo explicitamente:

  * IP
  * Máscara
  * Gateway
  * Hostname
* O **Perfil de rede** (LEGACY / SEGMENTADO) estiver explícito por loja

**Nota de escopo:**
Esta fase foca exclusivamente na **consistência do domínio**. UI, automação de aplicação de rede e fluxos de fila permanecem como passos subsequentes, após a estabilização dos dados.

---

## Histórico de Decisões Integradas

* **2026-02-07** — Substituição do conceito de *Regra de IP* por **Grupo de Rede** (papel completo: IP + Máscara + Gateway + Hostname).
