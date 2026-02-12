"""
Compat layer.

O split moveu a base de testes do domínio Chamado para `chamados.tests._base`.
Mantemos este módulo para não quebrar imports antigos durante a migração.
"""

from chamados.tests._base import *  # noqa: F403,F401
