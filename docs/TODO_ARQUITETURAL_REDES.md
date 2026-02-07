# TODO Arquitetural — Integração de Regras de Rede com Cadastro e Execução

Este documento registra **passos futuros já decididos**, evitando rediscussão
e garantindo evolução consistente do domínio de redes.

---

## 1. Onde entra no fluxo

### Cadastro (Registry)
- `TipoEquipamento` representa apenas o **tipo lógico** (PDV, TC, CONSULTA_PRECO).
- Não contém índice, quantidade ou numeração.
- Futuramente poderá ter **FK opcional** para `RegraRedeEquipamento`.

### Execução (Operation)
- A **instância real** do equipamento (ex.: PDV #1, PDV #2) nasce na execução.
- O índice da instância define offsets/IPs derivados conforme a regra.
- A execução consulta:
  - Perfil de rede ativo da loja
  - Regra de rede do tipo de equipamento
  - Índice da instância

---

## 2. Por que NÃO criar PDV1 / PDV2 / PDV3

- Tipos diferentes representam **coisas diferentes** no mundo real.
- PDV1/PDV2 são apenas **instâncias** do mesmo tipo.
- Modelar isso no cadastro:
  - explode o número de registros
  - dificulta manutenção
  - mistura planejamento com execução

Decisão:  
➡️ **Índice sempre pertence à execução, nunca ao cadastro.**

---

## 3. Evolução da validação (WARN → ERROR)

### Fase atual (MVP)
- Validação de IP roda como **service puro**
- WARN não bloqueia
- ERROR indica erro estrutural (ex.: IP fora da loja)

### Fase futura
- Quando `TipoEquipamento` estiver ligado a `RegraRedeEquipamento`:
  - IP inválido para regra → **ERROR bloqueante**
  - Typo (`.111` vs `.11`) pode continuar como WARN
- O ponto de bloqueio será:
  - setup do chamado
  - ou validação final antes de concluir execução

---

## 4. Critério para avançar para implementação

Só implementar quando:
- Cadastro de tipos estiver estabilizado
- Perfil de rede estiver explícito na loja/projeto
- Regras cobrirem mais de um tipo além de TC

Até lá:
- Service atual é a fonte da verdade
- Testes são o contrato