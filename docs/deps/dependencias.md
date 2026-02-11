# Auditoria de Dependências — EXPANSÃO360

Este documento registra **todas as dependências Python do projeto**, sua origem
e responsabilidade, evitando acoplamento acidental e crescimento descontrolado
da stack.

> Regra: nenhuma dependência entra no projeto sem estar documentada aqui.

---

## 1. Fontes auditadas

### 1.1 environment.yml
- Status: ⬜ auditado | ⬜ não auditado
- Observação: ambiente base de desenvolvimento (conda)

### 1.2 requirements*.txt / pyproject.toml
- Status: ⬜ inexistente | ⬜ auditado
- Observação: dependências Python diretas do projeto

### 1.3 Dependências implícitas
- Instaladas manualmente (`pip install …`)
- Introduzidas por decisões arquiteturais
- Ferramentas de qualidade / hooks

---

## 2. Dependências por responsabilidade

### 2.1 Core / Domínio
Dependências necessárias para regras de negócio puras,
independentes de framework e UI.

| Dependência | Origem | Justificativa | Observações |
|------------|-------|---------------|-------------|
| _(vazio)_  | —     | —             | Core permanece framework-agnostic |

🧠 Decisão atual:
- O **domínio não depende de Django**
- Services são testáveis sem infra

---

### 2.2 Web (Django)
Dependências usadas exclusivamente na camada web.

| Dependência | Origem | Justificativa |
|------------|-------|---------------|
| Django | ADR 2026-01-21 | Framework web principal |
| django-templatetags | decisão implícita | Extensão de UI (templatetags) |

📌 Observação:
- Models Django **não contêm regra de negócio**
- CBVs e templatetags são considerados decisão arquitetural

---

### 2.3 Testes
Ferramentas de teste e validação automática.

| Dependência | Origem | Justificativa |
|------------|-------|---------------|
| pytest | decisão técnica | Testes unitários e de contrato |
| pytest-django | implícita | Integração com Django |
| coverage | _(se existir)_ | Métrica de cobertura |

🧠 Regra:
- Testes são **contrato vivo**
- Quebra de teste = regressão

---

### 2.4 Qualidade (Lint / Format / Hooks)
Ferramentas que **impõem padrão**, não opcionais.

| Dependência | Origem | Justificativa |
|------------|-------|---------------|
| ruff | decisão técnica | Lint + format unificado |
| black | legado | Formatação (a avaliar consolidação) |
| pre-commit | decisão técnica | Garantir qualidade antes do commit |

📌 Observação:
- Formatação automática **é requisito**, não preferência pessoal

---

### 2.5 CLI
Dependências usadas no modo CLI (Sprint inicial).

| Dependência | Origem | Justificativa |
|------------|-------|---------------|
| argparse / click | _(confirmar)_ | Interface CLI |

---

### 2.6 Infra / Dev Tooling
Ferramentas de suporte ao desenvolvimento.

| Dependência | Origem | Justificativa |
|------------|-------|---------------|
| conda | decisão inicial | Isolamento de ambiente |
| make | opcional | Atalhos de automação |
| git | obrigatório | Versionamento |

---

## 3. Dependências não documentadas (achados)

> Lista de dependências que **apareceram no meio do caminho**
> e precisam ser validadas, mantidas ou removidas.

| Dependência | Onde apareceu | Ação |
|------------|--------------|------|
| _(exemplo)_ jest | assets JS | Avaliar necessidade |
| _(exemplo)_ requests | script local | Remover / documentar |

---

## 4. Dependências que viram requisitos do sistema

Estas dependências **geram requisitos funcionais ou não funcionais**.

### 4.1 Requisitos explícitos

- O sistema **deve impor formatação automática** antes de aceitar commits
- O sistema **deve suportar testes automatizados** desde o domínio até a web

### 4.2 Requisitos em avaliação

- ⬜ Suporte a testes JS (ex.: Jest)
- ⬜ Padronização completa em Ruff (substituir Black)

---

## 5. Próximos passos (bloqueios)

Antes de iniciar o **Ciclo 2**:

- [ ] Confirmar conteúdo do `environment.yml`
- [ ] Decidir fonte única de dependências (conda vs pip)
- [ ] Consolidar stack de qualidade (Ruff vs Black)
- [ ] Atualizar REQUIREMENTS.md com impactos

---

## Status
- Documento criado: ⬜
- Auditoria concluída: ⬜
- Aprovado para início do Ciclo 2: ⬜