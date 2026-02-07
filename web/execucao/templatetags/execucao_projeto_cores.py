# web/execucao/templatetag/execucao.py

from __future__ import annotations

from django import template

register = template.Library()

COLOR_TO_CLASS = {
    "SLATE": "bg-slate-200",
    "BLUE": "bg-blue-500",
    "EMERALD": "bg-emerald-500",
    "VIOLET": "bg-violet-500",
    "AMBER": "bg-amber-500",
    "ROSE": "bg-rose-500",
    "CYAN": "bg-cyan-500",
    "LIME": "bg-lime-500",
}


@register.simple_tag
def projeto_color_bar(projeto) -> str:
    """
    Retorna a classe tailwind da faixa de cor do projeto.
    Fallback sempre para SLATE.
    """
    slug = (getattr(projeto, "cor_slug", None) or "SLATE").strip().upper()
    return COLOR_TO_CLASS.get(slug, COLOR_TO_CLASS["SLATE"])
