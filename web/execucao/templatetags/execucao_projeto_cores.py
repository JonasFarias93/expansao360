from __future__ import annotations

from django import template

register = template.Library()

COLOR_TO_BAR_CLASS = {
    "SLATE": "bg-slate-200",
    "BLUE": "bg-blue-500",
    "EMERALD": "bg-emerald-500",
    "VIOLET": "bg-violet-500",
    "AMBER": "bg-amber-500",
    "ROSE": "bg-rose-500",
    "CYAN": "bg-cyan-500",
    "LIME": "bg-lime-500",
}

COLOR_TO_BG_ACTIVE_CLASS = {
    "SLATE": "bg-slate-100",
    "BLUE": "bg-blue-100",
    "EMERALD": "bg-emerald-100",
    "VIOLET": "bg-violet-100",
    "AMBER": "bg-amber-100",
    "ROSE": "bg-rose-100",
    "CYAN": "bg-cyan-100",
    "LIME": "bg-lime-100",
}

COLOR_TO_TEXT_ACTIVE_CLASS = {
    "SLATE": "text-slate-800",
    "BLUE": "text-blue-800",
    "EMERALD": "text-emerald-800",
    "VIOLET": "text-violet-800",
    "AMBER": "text-amber-800",
    "ROSE": "text-rose-800",
    "CYAN": "text-cyan-800",
    "LIME": "text-lime-800",
}


def _slug(projeto) -> str:
    return (getattr(projeto, "cor_slug", None) or "SLATE").strip().upper()


@register.simple_tag
def projeto_color_bar(projeto) -> str:
    """
    Retorna a classe tailwind da faixa de cor do projeto.
    Fallback sempre para SLATE.
    """
    slug = _slug(projeto)
    return COLOR_TO_BAR_CLASS.get(slug, COLOR_TO_BAR_CLASS["SLATE"])


@register.simple_tag
def projeto_color_bg_active(projeto) -> str:
    """
    Retorna a classe tailwind de background quando o card estiver ativo.
    Ex.: bg-blue-100
    """
    slug = _slug(projeto)
    return COLOR_TO_BG_ACTIVE_CLASS.get(slug, COLOR_TO_BG_ACTIVE_CLASS["SLATE"])


@register.simple_tag
def projeto_color_text_active(projeto) -> str:
    """
    Retorna a classe tailwind de texto quando o card estiver ativo.
    Ex.: text-blue-800
    """
    slug = _slug(projeto)
    return COLOR_TO_TEXT_ACTIVE_CLASS.get(slug, COLOR_TO_TEXT_ACTIVE_CLASS["SLATE"])
