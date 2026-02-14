from types import SimpleNamespace

from web.execucao.templatetags.execucao_ui import projeto_color_bar


def test_execucao_ui_reexports_projeto_color_bar():
    projeto = SimpleNamespace(cor_slug="blue")
    assert projeto_color_bar(projeto) == "bg-blue-500"
