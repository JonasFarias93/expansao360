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
	pytest || test $$? -eq 5

check: lint test

hooks:
	pre-commit install


cli:
	python -m expansao360 --help

demo:
	rm -f .expansao360-state.json
	python -m expansao360 location add LOC-001 "Loja A"
	python -m expansao360 mount register LOC-001 jonas
	python -m expansao360 location list
	python -m expansao360 mount list
