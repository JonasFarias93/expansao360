# Documentação (docs/) — Expansão360

Este diretório concentra documentação operacional, técnica e de governança
que **não são ADRs**.

> ADRs oficiais ficam em: `DECISIONS/`
> Índice dos ADRs: `DECISIONS/README.md`

---

# 🎯 Papel do diretório `docs/`

* **docs/** = Manual vivo (como funciona, como usar, como testar, como operar)
* **DECISIONS/** = ADRs (por que decidimos + consequências)

📌 Regra estrutural:

* Se o conteúdo responde "por que decidimos isso" → vira ADR.
* Se o conteúdo responde "como funciona / como usar" → fica em `docs/`.

---

# 🧭 Estrutura Atual

## Backlog / Governança

* `backlog/decisoes-pendentes.md`
* `backlog/docs-pendentes.md` (quando existir)

## Dependências

* `deps/dependencias.md`
* `deps/dependencias-frontend.md`

## Inventários

* `inventory/entidades-com-codigo.md`

## Redes

* `redes/README.md`
* `redes/validacao-ip-mvp.md`
* `redes/validacao.md`
* `redes/todo-arquitetural-redes.md`
* `redes/grupos-de-rede-template.md`

## Testes

* `testing/auditoria-teste.md`

## UI / Execução

* `ui/templates-contrato-execucao.md`

---

# 📊 Mapa de Manutenção (As-Is)

Este quadro controla o estado real da documentação.

| Documento                         | Owner    | Escopo                             | Source of Truth                            | Última revisão | Status     |
| --------------------------------- | -------- | ---------------------------------- | ------------------------------------------ | -------------- | ---------- |
| redes/validacao-ip-mvp.md         | Redes    | Contrato atual de validação IP     | `web/redes/services/validacao.py` + testes | 2026-02-11     | OK         |
| redes/validacao.md                | Redes    | Ponte para contrato atual          | `validacao-ip-mvp.md`                      | 2026-02-11     | OK         |
| redes/todo-arquitetural-redes.md  | Redes    | Evolução futura                    | ADR-046–050                                | 2026-02-11     | INCOMPLETO |
| ui/templates-contrato-execucao.md | Execução | Contrato de templates e estados    | `web/execucao/templates/*` + views         | 2026-02-11     | OK         |
| testing/auditoria-teste.md        | Core     | Estado e padrão da suíte de testes | `pytest` + `web/*/tests`                   | 2026-02-11     | OK         |
| deps/dependencias.md              | Core     | Dependências Python                | environment + imports reais                | 2026-02-11     | OK         |
| deps/dependencias-frontend.md     | Core     | Stack JS ativa                     | `web/**/__tests__/`                        | 2026-02-11     | OK         |

Status possíveis:

* **OK** — Reflete comportamento atual comprovado
* **DESATUALIZADO** — Diverge do código
* **INCOMPLETO** — Falta governança ou fonte explícita
* **AMBÍGUO** — Não aplicável diretamente
* **REMOVER** — Sem propósito atual

---

# 🔎 Ritual Oficial de Auditoria

Documentação boa nasce de provas do repositório, não da memória.

Para cada documento relevante:

1. Extrair afirmações verificáveis.
2. Localizar implementação real no código.
3. Confirmar existência de testes que provem o comportamento.
4. Classificar:

   * OK
   * DESATUALIZADO
   * INCOMPLETO
   * AMBÍGUO
5. Atualizar minimamente (sem transformar em tutorial gigante).
6. Registrar rodapé padrão:

```
---
Última revisão: YYYY-MM-DD
Fonte: <módulo/teste/ADR relacionado>
```

---

# ✅ Definição de Pronto (Documentação)

Um documento só pode ser marcado como **OK** quando:

* Todas as afirmações possuem fonte verificável.
* Caminhos e comandos batem com o repositório.
* Não existem "TODO" soltos.
* Existe data de revisão.
* Existe referência a módulo, teste ou ADR.

---

# 📌 Regra de Governança

Mudou comportamento do sistema?

→ Atualizar documentação e/ou ADR **no mesmo PR**.

Sem isso, o PR não está completo.

---

Última revisão: 2026-02-11
Fonte: Estrutura real do repositório + auditorias nível 2 realizadas
