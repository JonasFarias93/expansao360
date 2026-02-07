# Grupos de Rede — Template Oficial

Este documento define o **contrato padrão** para grupos de rede no EXPANSÃO360.

Um **Grupo de Rede** representa um conjunto lógico de equipamentos que:

* compartilham a mesma intenção operacional
* seguem regras homogêneas de endereçamento
* possuem padrões previsíveis de hostname
* são validados de forma consistente e testável

O grupo **RETAGUARDA_LOJA** é definido como **template oficial**
e deve servir de base para todos os grupos futuros.

---

## Estrutura Padrão de um Grupo de Rede (Contrato)

Todo grupo de rede **DEVE** documentar os campos abaixo.

### 1. Identificação do Grupo

| Campo                        | Descrição                     |
| ---------------------------- | ----------------------------- |
| **Nome do grupo**            | Identificador único e estável |
| **Descrição / Intenção**     | Papel do grupo na operação    |
| **Perfil de Rede aplicável** | `LEGACY_FLAT` ou `SEGMENTADO` |

---

### 2. Configuração Base de Rede

| Campo         | Descrição                                       |
| ------------- | ----------------------------------------------- |
| **Rede base** | IP base derivado de bandeira + código histórico |
| **Máscara**   | Máscara de rede aplicável ao grupo              |
| **Gateway**   | Gateway padrão do grupo                         |

> A rede base **não é um IP fixo**, mas uma derivação padronizada.

---

### 3. Itens do Grupo (Sub-itens)

Cada grupo define **itens internos**, normalmente correspondendo a tipos de equipamento.

Para **cada item**, devem ser definidos:

| Campo                 | Descrição                        |
| --------------------- | -------------------------------- |
| **Nome do item**      | Ex: PDV, TC, SERVIDOR_LOCAL      |
| **Regra de IP**       | OFFSET_FIXO | FAIXA | SEQUENCIAL |
| **Parâmetros de IP**  | Offset / Faixa / Base            |
| **Hostname pattern**  | Padrão esperado de hostname      |
| **Severidade padrão** | ERROR ou WARN                    |

---

## Grupo: RETAGUARDA_LOJA

### 1. Intenção do Grupo

**Retaguarda fixa da loja**, composta por equipamentos de baixo volume (baixo N),
endereçamento previsível e papéis administrativos/operacionais.

Características principais:

* IPs convencionais e estáveis
* Pouca variação de quantidade por loja
* Alta criticidade operacional (impacto administrativo)

---

### 2. Perfis de Rede Suportados

O grupo **RETAGUARDA_LOJA** é aplicável aos seguintes perfis:

#### RD_SEGMENTADO_2024 / 2025

| Campo       | Valor                       |
| ----------- | --------------------------- |
| **Máscara** | /27                         |
| **Gateway** | Offset fixo do bloco (`.1`) |

> Bloco segmentado dedicado à retaguarda, com controle explícito de ocupação.

---

#### LEGACY_FLAT_2023

| Campo       | Valor                       |
| ----------- | --------------------------- |
| **Máscara** | /24                         |
| **Gateway** | Offset legado padrão (`.1`) |

> Mantém compatibilidade com o modelo clássico de rede flat.

---

### 3. Itens do Grupo (Oficiais)

Os itens abaixo são **fixos e obrigatórios** para o grupo RETAGUARDA_LOJA.

---

#### Item: BANCO12

| Campo                         | Valor             |
| ----------------------------- | ----------------- |
| **Regra de IP**               | OFFSET_FIXO       |
| **Offset**                    | .12               |
| **Hostname pattern (padrão)** | `F{codigo}-BDD12` |
| **Severidade**                | ERROR             |

---

#### Item: MICRO_GERENCIA

| Campo                         | Valor              |
| ----------------------------- | ------------------ |
| **Regra de IP**               | OFFSET_FIXO        |
| **Offset**                    | .130               |
| **Hostname pattern (padrão)** | `F{codigo}-GER130` |
| **Severidade**                | ERROR              |

**Exceção Drogasil:**

* Hostname permitido: `GER{cod_historico}`

---

#### Item: PORTAL_DO_SABER (RH)

| Campo                | Valor              |
| -------------------- | ------------------ |
| **Regra de IP**      | OFFSET_FIXO        |
| **Offset**           | .140               |
| **Hostname pattern** | `F{codigo}-PSB140` |
| **Severidade**       | WARN               |

---

#### Item: MICRO_FARMA

| Campo                | Valor              |
| -------------------- | ------------------ |
| **Regra de IP**      | OFFSET_FIXO        |
| **Offset**           | .150               |
| **Hostname pattern** | `F{codigo}-FAR150` |
| **Severidade**       | WARN               |

---

### 4. Observações de Governança

* Todos os itens utilizam **OFFSET_FIXO**, sem crescimento dinâmico.
* Alterações de offset exigem justificativa operacional.
* Novos itens **não podem** ser adicionados ao grupo sem ADR.

---

### Status

* **RETAGUARDA_LOJA**: Grupo fechado e oficial
* **Uso**: Template obrigatório para grupos futuros
