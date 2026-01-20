.PHONY: help fmt lint test check hooks

help:
	@echo ""
	@echo "Comandos disponíveis:"
	@echo "  make fmt     -> Formatar código (ruff + black)"
	@echo "  make lint    -> Analisar código (ruff)"
	@echo "  make test    -> Rodar testes (pytest)"
	@echo "  make check   -> Lint + Test"
	@echo "  make hooks   -> Instalar hooks do pre-commit"
	@echo ""

fmt:
	ruff format .
	black .

lint:
	ruff check .

test:
	pytest

check: lint test

hooks:
	pre-commit install
