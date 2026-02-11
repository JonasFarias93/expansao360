# Auditoria de Dependências Python — EXPANSÃO360

Este documento registra todas as dependências Python utilizadas
no projeto EXPANSÃO360, sua responsabilidade arquitetural
e seu impacto no sistema.

> Regra de governança:
> Nenhuma dependência entra no projeto sem ser documentada aqui.
> Dependências não registradas são consideradas não autorizadas.

---

# 1. Source of Truth

As dependências Python devem ser verificadas em:

* `environment.yml` (ambiente Conda)
* `requirements*.txt` ou `pyproject.toml` (se existirem)
* `pre-commit-config.yaml`
* Importações reais no código (`grep -R "import "`)

---

# 2. Dependências por Camada

---

## 2.1 Domínio (Core)

Responsabilidade:

* Regras de negócio puras
* Services independentes de framework

### Status atual

✔ O domínio não depende de Django
✔ Services são testáveis sem infraestrutura

Dependências explícitas:

| Dependência   | Justificativa                |
| ------------- | ---------------------------- |
| Python stdlib | Dataclasses, Enum, ipaddress |

Decisão arquitetural:

* O domínio deve permanecer framework-agnostic.

---

## 2.2 Camada Web (Django)

Responsabilidade:

* HTTP
* ORM
* Templates
* Permissões

| Dependência | Justificativa           | Origem                 |
| ----------- | ----------------------- | ---------------------- |
| Django      | Framework web principal | ADR (adoção do Django) |

Observações:

* Models Django não devem conter regra de negócio estrutural.
* A lógica crítica deve permanecer no domínio/service layer.

---

## 2.3 Testes

Responsabilidade:

* Contrato vivo do sistema
* Garantia de regressão

| Dependência         | Justificativa              |
| ------------------- | -------------------------- |
| pytest              | Runner principal de testes |
| pytest-django       | Integração pytest ↔ Django |
| coverage (se ativo) | Métrica de cobertura       |

Regra:

* Quebra de teste = regressão
* Testes são parte do contrato do sistema

---

## 2.4 Qualidade (Lint / Format / Hooks)

Responsabilidade:

* Padronização automática
* Redução de divergência entre desenvolvedores

| Dependência | Justificativa                                   |
| ----------- | ----------------------------------------------- |
| ruff        | Lint + formatação unificada                     |
| black       | Legado / compatibilidade (avaliar consolidação) |
| pre-commit  | Execução automática antes de commit             |

Requisito não funcional derivado:

* O sistema deve impor padronização automática antes do commit.

---

## 2.5 CLI (Legado / Sprint Inicial)

Responsabilidade:

* Interface inicial de linha de comando

Dependências possíveis:

| Dependência       | Status                   |
| ----------------- | ------------------------ |
| argparse (stdlib) | Confirmado               |
| click             | Confirmar se ainda ativo |

⚠ Caso CLI deixe de ser parte ativa do produto,
essa seção deve ser reavaliada via ADR.

---

## 2.6 Infra / Dev Tooling

Ferramentas que não fazem parte do runtime do sistema.

| Ferramenta | Papel                  |
| ---------- | ---------------------- |
| conda      | Isolamento de ambiente |
| make       | Atalhos de automação   |
| git        | Versionamento          |

Observação:

* Nenhuma dessas ferramentas é requisito do sistema em produção.

---

# 3. Dependências Implícitas (Auditoria Técnica)

Dependências detectadas devem ser validadas via:

```
pip freeze
grep -R "import " web/
```

Toda dependência externa encontrada deve:

1. Estar documentada aqui
2. Ter justificativa arquitetural
3. Ser classificada por camada

---

# 4. Dependências que Geram Requisitos

Algumas dependências impõem requisitos sistêmicos:

## 4.1 RNF-QA-001 — Testabilidade

O sistema deve suportar:

* Testes automatizados de domínio
* Testes de integração Django
* (Opcional) Testes JS

---

## 4.2 RNF-QA-002 — Padronização de Código

O sistema deve impor:

* Lint automático
* Formatação automática
* Bloqueio de commit em caso de erro

---

# 5. Decisões em Aberto

* Consolidar Ruff como único formatador?
* Remover Black definitivamente?
* Manter CLI como parte ativa?
* Adotar fonte única de dependências (Conda vs pip)?

Qualquer decisão estrutural exige ADR.

---

# 6. Status da Auditoria

* [x] Dependências principais identificadas
* [x] Camadas classificadas
* [x] Requisitos derivados explicitados
* [ ] Confirmar alinhamento entre `environment.yml` e imports reais
* [ ] Consolidar fonte única de dependências

---

Última revisão: 2026-02-11
Fonte: estrutura do repositório + imports reais + ferramentas configuradas
