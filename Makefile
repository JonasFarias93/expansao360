.PHONY: help fmt lint test test-py test-js check hooks env-create deps-install rebuild-clean cli demo

ENV_NAME ?= expansao360
CONDA ?= conda
PYTHON ?= python

help:
	@echo ""
	@echo "Comandos disponíveis:"
	@echo "  make env-create    -> Criar/atualizar ambiente Conda (environment.yml)"
	@echo "  make deps-install  -> Instalar deps Python via pyproject (pip -e .)"
	@echo "  make rebuild-clean -> Remover env e fazer rebuild limpo + check"
	@echo "  make fmt           -> Formatar código (ruff + black)"
	@echo "  make lint          -> Analisar código (ruff)"
	@echo "  make test          -> Rodar testes (pytest + jest)"
	@echo "  make test-py       -> Rodar testes (pytest)"
	@echo "  make test-js       -> Rodar testes (jest)"
	@echo "  make check         -> Lint + Test"
	@echo "  make hooks         -> Instalar hooks do pre-commit"
	@echo ""

# =========================
# Ambiente / Dependências
# =========================

env-create:
	@echo "🔹 Criando/atualizando ambiente Conda: $(ENV_NAME)"
	@$(CONDA) env create -f environment.yml -n $(ENV_NAME) || true
	@$(CONDA) env update -f environment.yml -n $(ENV_NAME) --prune
	@echo "✅ Ambiente pronto."

deps-install:
	@echo "🔹 Instalando dependências Python via pyproject.toml"
	@$(CONDA) run -n $(ENV_NAME) $(PYTHON) -m pip install --upgrade pip
	@$(CONDA) run -n $(ENV_NAME) $(PYTHON) -m pip install -e .
	@echo "✅ Dependências instaladas."

rebuild-clean:
	@echo "🔥 Removendo ambiente $(ENV_NAME) (se existir)"
	@$(CONDA) env remove -n $(ENV_NAME) -y || true
	@$(MAKE) env-create
	@$(MAKE) deps-install
	@$(MAKE) check
	@echo "🚀 Rebuild limpo concluído."

# =========================
# Qualidade / Testes
# =========================

fmt:
	ruff format .
	black .

lint:
	ruff check .

test-py:
	@# pytest retorna 5 quando não encontra testes; mantemos seu comportamento
	pytest || test $$? -eq 5

test-js:
	npm run test:js

test: test-py test-js

check: lint test

hooks:
	pre-commit install

# =========================
# Utilitários (mantidos)
# =========================

cli:
	python -m expansao360 --help

demo:
	rm -f .expansao360-state.json
	python -m expansao360 location add LOC-001 "Loja A"
	python -m expansao360 mount register LOC-001 jonas
	python -m expansao360 location list
	python -m expansao360 mount list