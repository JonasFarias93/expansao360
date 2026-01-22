# EXPANSÃO360

Plataforma para gestão de expansão, padronização e operação de campo, separando claramente
cadastro administrativo (mestre) da execução operacional, com rastreabilidade completa.

> **Última versão estável:** `v0.2.0` — Web v1 (Registry + Chamado)

## Objetivo

O EXPANSÃO360 tem como objetivo estruturar e padronizar a expansão de operações físicas,
garantindo que o que foi definido no planejamento seja corretamente executado em campo,
com histórico, evidências e governança.

## Status do Projeto

🚧 **Sprint 2 — Cadastro e Execução Base (Web + CLI)**

O projeto já possui:
- Arquitetura limpa (Domain / Application / Infrastructure)
- Core de domínio independente de framework
- Casos de uso testados (TDD)
- CLI funcional
- Camada Web (Django) em evolução
- Execução via Chamados (UI inicial)
- Persistência local e ORM
- Testes automatizados e pre-commit hooks


## Conceito Central

O sistema é baseado em uma separação clara de camadas:

- **Registry (Cadastro Mestre)**  
  Define *o que existe* e *como deve ser* (ex: lojas, projetos, layouts, padrões).

- **Operation (Execução de Campo)**  
  Registra *o que foi executado*, *quando*, *por quem* e *com quais evidências*.

Essa separação garante rastreabilidade, auditoria e evolução segura do sistema.

---

## Como rodar o projeto localmente

### Pré-requisitos
- Git
- Conda (Miniforge / Miniconda)
- GNU Make

### Setup do ambiente

```bash
# criar o ambiente
conda env create -f environment.yml

# ativar
conda activate expansao360
```

---

## CLI (modo apresentação)

A CLI permite cadastrar Locations (Registry) e registrar operações (Operation) **sem API**.


### Ajuda


```bash
python -m expansao360 --help
python -m expansao360 location --help
python -m expansao360 mount --help
```

---
### Fluxo completo (exemplo)

```
# (opcional) limpar estado local
rm -f .expansao360-state.json

# 1) cadastrar Location no Registry
python -m expansao360 location add LOC-001 "Loja A"

# 2) registrar uma operação (somente se a Location existir)
python -m expansao360 mount register LOC-001 jonas

# 3) listar
python -m expansao360 location list
python -m expansao360 mount list
```


## Web (Django)

A camada Web fornece:
- Cadastro administrativo (Registry)
- Execução operacional via Chamados
- Interface administrativa (Django Admin)

### Comandos principais

```bash
# aplicar migrations
python web/manage.py migrate

# rodar servidor
python web/manage.py runserver

# rodar testes
python web/manage.py test
