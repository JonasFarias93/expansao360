.PHONY: help fmt lint test test-py test-js check hooks \
        env-create deps-install deps-install-dev rebuild-clean \
        deps-snapshot deps-check cli demo

ENV_NAME ?= expansao360
CONDA ?= conda
PYTHON ?= python

help:
	@echo ""
	@echo "Comandos disponíveis:"
	@echo "  make env-create        -> Criar/atualizar ambiente Conda (environment.yml)"
	@echo "  make deps-install      -> Instalar deps Python (web+test) via pyproject (pip -e .[web,test])"
	@echo "  make deps-install-dev  -> Instalar deps Python (dev+web+test) via pyproject (pip -e .[dev,web,test])"
	@echo "  make rebuild-clean     -> Remover env e fazer rebuild limpo + check (dev+web+test)"
	@echo "  make deps-snapshot     -> Gerar snapshots em docs/deps/"
	@echo "  make deps-check        -> Auditoria deps Python (deptry) no pacote expansao360/"
	@echo "  make fmt               -> Formatar código (ruff + black)"
	@echo "  make lint              -> Analisar código (ruff)"
	@echo "  make test              -> Rodar testes (pytest + jest)"
	@echo "  make test-py           -> Rodar testes (pytest)"
	@echo "  make test-js           -> Rodar testes (jest)"
	@echo "  make check             -> Lint + deps-check + testes"
	@echo "  make hooks             -> Instalar hooks do pre-commit"
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
	@echo "🔹 Instalando dependências Python (web+test) via pyproject.toml"
	@$(CONDA) run -n $(ENV_NAME) $(PYTHON) -m pip install --upgrade pip
	@$(CONDA) run -n $(ENV_NAME) $(PYTHON) -m pip install -e ".[web,test]"
	@echo "✅ Dependências (web+test) instaladas."

deps-install-dev:
	@echo "🔹 Instalando dependências Python (dev+web+test) via pyproject.toml"
	@$(CONDA) run -n $(ENV_NAME) $(PYTHON) -m pip install --upgrade pip
	@$(CONDA) run -n $(ENV_NAME) $(PYTHON) -m pip install -e ".[dev,web,test]"
	@echo "✅ Dependências (dev+web+test) instaladas."

rebuild-clean:
	@echo "🔥 Rebuild limpo iniciado..."
	@bash -lc ' \
		if [ "$$CONDA_DEFAULT_ENV" = "$(ENV_NAME)" ]; then \
			echo "❌ Você está com o env $(ENV_NAME) ativado. Rode: conda deactivate"; \
			exit 2; \
		fi \
	'
	@echo "🔹 Removendo ambiente $(ENV_NAME) (se existir)"
	@$(CONDA) env remove -n $(ENV_NAME) -y || true
	@$(MAKE) env-create
	@$(MAKE) deps-install-dev
	@$(MAKE) check
	@echo "🚀 Rebuild limpo concluído."

deps-snapshot:
	@echo "📦 Gerando snapshots versionáveis em docs/deps/..."
	@mkdir -p docs/deps
	@$(CONDA) env export -n $(ENV_NAME) --no-builds > docs/deps/environment.snapshot.yml
	@$(CONDA) run -n $(ENV_NAME) $(PYTHON) -m pip freeze > docs/deps/pip-freeze.snapshot.txt
	@echo "✅ Snapshots atualizados em docs/deps/"

deps-check:
	@echo "🔎 Auditando dependências Python (deptry)..."
	@$(CONDA) run -n $(ENV_NAME) deptry expansao360 \
		--ignore DEP002:Django \
		--ignore DEP002:python-dotenv \
		--ignore DEP002:psycopg

# =========================
# Qualidade / Testes
# =========================

fmt:
	@$(CONDA) run -n $(ENV_NAME) ruff format .
	@$(CONDA) run -n $(ENV_NAME) black .

lint:
	@$(CONDA) run -n $(ENV_NAME) ruff check .

test-py:
	@# pytest retorna 5 quando não encontra testes; mantemos seu comportamento
	@$(CONDA) run -n $(ENV_NAME) pytest || test $$? -eq 5

test-js:
	npm run test:js

test: test-py test-js

check: lint deps-check test

hooks:
	@$(CONDA) run -n $(ENV_NAME) pre-commit install

ptw:
	@$(CONDA) run -n $(ENV_NAME) ptw

ptw-fast:
	@$(CONDA) run -n $(ENV_NAME) ptw -c -- -q
# =========================
# Utilitários (mantidos)
# =========================

cli:
	@$(CONDA) run -n $(ENV_NAME) python -m expansao360 --help

demo:
	rm -f .expansao360-state.json
	@$(CONDA) run -n $(ENV_NAME) python -m expansao360 location add LOC-001 "Loja A"
	@$(CONDA) run -n $(ENV_NAME) python -m expansao360 mount register LOC-001 jonas
	@$(CONDA) run -n $(ENV_NAME) python -m expansao360 location list
	@$(CONDA) run -n $(ENV_NAME) python -m expansao360 mount list