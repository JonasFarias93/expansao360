# EXPANSÃO360

Plataforma para gestão de expansão, padronização e **operação de campo**,
com separação rigorosa entre **cadastro mestre (Registry)** e **execução operacional (Operation)**,
garantindo rastreabilidade, histórico e governança de ponta a ponta.

---

## Objetivo

O EXPANSÃO360 tem como objetivo estruturar e padronizar a expansão de operações físicas,
assegurando que o que foi definido no planejamento seja corretamente executado em campo,
com evidências, histórico auditável e regras claras de operação.

---

## Status do Projeto

🚀 **Release atual: v0.3.0 — Fluxo Operacional Completo**  
🚧 **Sprint atual: Sprint 4 — UX Operacional & Views**

O projeto já possui uma base sólida com:

- Arquitetura limpa (Domain / Application / Infrastructure)
- Core de domínio independente de framework
- Regras de negócio explícitas e testadas (TDD)
- Execução operacional baseada em **Chamados**
- Suporte a **fluxo direto e fluxo inverso**
- Registro de **itens operacionais** e **evidências**
- IAM mínimo baseado em **capabilities**
- Camada Web (Django) funcional
- CLI funcional (modo apresentação)
- Testes automatizados e hooks de qualidade

---

## Conceito Central

O sistema é baseado em uma separação clara e intencional de camadas:

### Registry (Cadastro Mestre)
Define **o que existe** e **como deve ser padronizado**  
(ex.: lojas, projetos, equipamentos, kits).

Características:
- Fonte da verdade
- Alterações controladas
- Versionamento e governança

### Operation (Execução de Campo)
Registra **o que foi executado**, **quando**, **por quem** e **com quais evidências**.

Características:
- Histórico imutável
- Rastreabilidade completa
- Suporte a exceções e auditoria

Essa separação reduz ambiguidade, melhora governança e permite evolução segura do sistema.

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


Web (Django)

A camada Web fornece:

- Cadastro administrativo (Registry)

- Execução operacional via Chamados

- Suporte a fluxo direto e inverso

- Registro e visualização de evidências

- Interface administrativa (Django Admin)

### Comandos principais

```bash
# aplicar migrations
python web/manage.py migrate

# rodar servidor
python web/manage.py runserver

# rodar testes
python web/manage.py test
