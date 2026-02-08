# Grupos de Rede — Template Oficial

Este documento define o **contrato padrão** para grupos de rede no EXPANSÃO360.

Um **Grupo de Rede** representa um conjunto lógico de equipamentos que:

- compartilham a mesma intenção operacional
- seguem regras homogêneas de endereçamento
- possuem padrões previsíveis de hostname
- são validados de forma consistente e testável

O grupo **RETAGUARDA_LOJA** é o **primeiro grupo oficial**
e serve como **referência prática** deste template.

---

## Estrutura Padrão de um Grupo de Rede (Contrato)

Todo grupo de rede **DEVE** documentar os campos abaixo.

---

### 1. Identificação do Grupo

| Campo | Descrição |
|-----|----------|
| **Nome do grupo** | Identificador único e estável |
| **Descrição / Intenção** | Papel do grupo na operação |
| **Perfis de Rede suportados** | Ex.: `LEGACY_FLAT`, `RD_SEGMENTADO` |

---

### 2. Configuração de Rede (por Perfil)

Cada grupo **DEVE** explicitar suas configurações **por perfil de rede**.

Para cada perfil:

| Campo | Descrição |
|-----|----------|
| **Máscara padrão** | Máscara esperada para o grupo |
| **Gateway padrão** | Gateway esperado |
| **Observações** | Restrições ou exceções do perfil |

> Caso um item **divirja** da máscara/gateway padrão do perfil,  
> isso **DEVE** ser documentado no nível do item.

---

### 3. Itens do Grupo (Sub-itens)

Cada grupo define seus **itens internos**, normalmente associados
a tipos de equipamento ou papéis funcionais.

Para **cada item**, devem ser definidos:

| Campo | Descrição |
|-----|----------|
| **Nome do item** | Ex.: Banco12, Gerência, RH |
| **Perfil aplicável** | LEGACY / SEGMENTADO / ambos |
| **Regra de IP** | OFFSET_FIXO \| FAIXA \| SEQUENCIAL |
| **Parâmetros de IP** | Offset / Faixa / Base |
| **Hostname pattern** | Padrão esperado de hostname |
| **Máscara / Gateway próprios** | Opcional, se divergir do perfil |
| **Severidade padrão** | ERROR ou WARN |
| **Observações de domínio** | Exceções semânticas ou históricas |

---

### 4. Regras de Governança

- Todo novo grupo **DEVE** seguir este contrato.
- Todo novo item **DEVE** ser documentado explicitamente.
- Divergências físicas vs semânticas **DEVEM** ser registradas.
- Alterações estruturais exigem **ADR**.
- O grupo + seu backlog de testes formam um **contrato vivo**.

---

## Referência Oficial

- **Grupo exemplo:** `RETAGUARDA_LOJA`
- **Status:** Grupo oficial fechado
- **Uso:** Base obrigatória para criação de novos grupos

Este template, aliado ao ADR  
**“Grupos de Rede definem IP, máscara, gateway e hostname”**,  
protege o domínio contra regressões conceituais e validações parciais.