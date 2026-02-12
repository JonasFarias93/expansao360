from types import SimpleNamespace

from execucao.templatetags.execucao_ui import projeto_color_bar


def test_projeto_color_bar_fallback_slate():
    assert projeto_color_bar(SimpleNamespace(cor_slug=None)) == "bg-slate-200"


def test_projeto_color_bar_blue():
    assert projeto_color_bar(SimpleNamespace(cor_slug="BLUE")) == "bg-blue-500"
