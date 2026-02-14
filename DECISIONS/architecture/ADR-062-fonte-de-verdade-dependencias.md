# ADR-062 — Fonte de Verdade de Dependências e Rebuild Limpo

- **Data:** 2026-02-13
- **Status:** Proposto

---

## Decisão

O projeto Expansão360 passa a adotar a seguinte definição formal de fonte de verdade de dependências:

- `pyproject.toml` → fonte oficial de dependências Python.
- `environment.yml` → definição do ambiente Conda (base + libs nativas).
- `_env_dump.yml` e `_pip_dump.txt` → snapshots informativos, não são fonte de verdade.
- O CI deve validar rebuild limpo do ambiente antes de considerar a pipeline verde.

Um rebuild limpo deve:

1. Criar ambiente novo via `environment.yml`
2. Instalar dependências Python via `pyproject.toml`
3. Executar `pytest`
4. Validar que o projeto sobe sem dependências implícitas

---

## Contexto

Com a consolidação do PostgreSQL como banco padrão (ADR-061) e aproximação da versão v0.4.0, tornou-se necessário:

- Evitar drift entre ambiente local e CI
- Evitar dependências instaladas manualmente e não declaradas
- Garantir reprodutibilidade total do ambiente
- Formalizar qual arquivo é a fonte oficial

Atualmente o projeto possui:

- `environment.yml`
- `pyproject.toml`
- Snapshots de ambiente
- CI funcional, porém sem rebuild formalizado como gate obrigatório

Essa situação pode gerar inconsistência silenciosa.

---

## Consequências

### Positivas

- Ambiente reproduzível
- CI confiável
- Redução de bugs “funciona na minha máquina”
- Base sólida para v0.4.0 e futura v1.0.0
- Onboarding mais simples

### Negativas

- Aumento leve do tempo de CI
- Necessidade de disciplina na atualização de dependências
- Rebuilds locais podem demorar mais

---

## Observações

Mudanças futuras na estratégia de dependências (ex: migração para Poetry puro ou Docker como padrão primário) exigirão nova ADR.