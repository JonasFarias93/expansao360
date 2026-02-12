"""
Compat layer para templatetags.

Mantém imports legados como:
- execucao.templatetags.execucao_ui
- web.execucao.templatetags.execucao_ui

Source of truth: chamados.templatetags.execucao_ui
"""

from chamados.templatetags.execucao_ui import *  # noqa: F403,F401
