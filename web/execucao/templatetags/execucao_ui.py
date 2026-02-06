from __future__ import annotations

from django import template

from .execucao_projeto_cores import projeto_color_bar as _projeto_color_bar

register = template.Library()


@register.simple_tag
def projeto_color_bar(projeto) -> str:
    return _projeto_color_bar(projeto)
