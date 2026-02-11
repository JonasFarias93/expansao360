# Inventário — Entidades com campo `codigo` (governança)

## Objetivo
Remover digitação manual do campo **`codigo`** nos cadastros e padronizar a geração de códigos:
- únicos
- legíveis
- organizados por domínio/categoria
- estáveis (imutáveis após criação)

Isso torna `codigo` uma **identidade de negócio** confiável para dashboard e relatórios.

> Importante: `codigo` **não é** o `id` do banco e deve ter unicidade garantida no BD.

---

## Escopo (o que procurar)
Listar telas/models que hoje possuem `codigo`:
- editável (input no form) ou
- gerado manualmente em algum fluxo.

Classificar cada “`codigo`” em:
1) **Obrigatório e deve ser automático**
2) **Pode ser automático mas opcional**
3) **Não é código de negócio** (virar slug/nome)

---

## Inventário inicial (a confirmar no código)

### Registry (Cadastro Mestre)
Entidades de cadastro que normalmente alimentam seletores, regras e padronização:

- **Loja**
  - Provável: `codigo` (ex: "12", "003500")
  - Sugestão de prefixo: `LOJ-000000`

- **Projeto**
  - Possível: `codigo` (se existir) ou slug
  - Sugestão: se for identidade de negócio → `PRO-000000`
  - Se for apenas URL/organização → usar `slug` e manter `nome`

- **Subprojeto**
  - Possível: `codigo`
  - Sugestão: `SUB-000000` (se virar identidade de negócio)

- **Kit**
  - Possível: `codigo`
  - Sugestão: `KIT-000000` (se houver consumo por dashboard e integrações)

- **Equipamento / TipoEquipamento / CategoriaEquipamento**
  - Indícios: existe “Novo equipamento” com campo Código manual
  - Sugestão:
    - Equipamento (catálogo/mestre): `EQP-000000`
    - Categoria: `CAT-000000` (se for exibida/filtrada em relatórios)
    - Tipo/Grupo (rede): somente se houver consumo como “chave” no dashboard → `TRE-000000` (exemplo)

- **Regras/Grupos de Rede (se existirem como entidade)**
  - Ex: GrupoRede / RegraRedeEquipamento
  - Normalmente não precisa de “código humano” se não for exposto no dashboard.
  - Candidato forte a “não é código de negócio”, a menos que o time use como identificador externo.

### Operation (Execução / Transacional)
Entidades operacionais com rastreabilidade e histórico:

- **Chamado**
  - Indícios: entidade central operacional
  - Sugestão: `CHA-000000`

- **Itens do Chamado / Execução**
  - Em geral, não precisa de “código humano” (usa ID interno + referência ao Chamado).
  - Se for necessário “código de rastreio” (ex: etiqueta/romaneio), tratar como outro identificador.

---

## Classificação inicial (proposta)

### 1) Obrigatório e deve ser automático
- Loja (se `codigo` já é chave do negócio)
- Chamado
- Equipamento (catálogo mestre) — motivo: evitar colisão e manter padronização

### 2) Pode ser automático mas opcional
- Kit (depende se o dashboard usa como chave)
- Categoria/Tipo (depende se são expostos em BI/relatórios)
- Projeto/Subprojeto (depende se já existe um padrão de código no negócio)

### 3) Não é código de negócio (slug/nome)
- Entidades puramente internas (regras, grupos técnicos) sem consumo em dashboard/BI
- Entidades onde o “código” atual é só um apelido local e muda com frequência

---

## Microtarefas para confirmar no repositório (checklist)
> Objetivo: transformar o “inventário inicial” em inventário **confirmado**.

1) **Buscar campo `codigo` nos models**
   - `rg -n "codigo" web/**/models.py`
   - mapear Model → tipo (Registry/Operation)

2) **Buscar formulários onde `codigo` aparece como input**
   - `rg -n "fields\s*=.*codigo|codigo" web/**/forms.py web/**/admin.py web/**/templates/**/*.html`

3) **Buscar validações/uso do `codigo` em queries**
   - `rg -n "codigo=" web/**`
   - identificar se já é chave de negócio (ex: filtros, integrações, relatórios)

4) Atualizar este documento com:
   - lista final de Models
   - decisão de classificação por entidade (1/2/3)
   - links para os arquivos/linhas relevantes (quando aplicável)

---

## Próxima decisão (ADR)
Quando formos implementar geração automática e imutabilidade, criar um ADR cobrindo:
- estratégia `PREFIXO + SEQUÊNCIA`
- atomicidade/concorrência (backend)
- unique constraint + index
- política de imutabilidade e exceções controladas
- migração de dados existentes (backfill)