from types import SimpleNamespace

from web.execucao.templatetags.execucao_ui import projeto_color_bar


class TestExecucaoUiFacadeTemplateTags:
    def test_reexport_projeto_color_bar(self):
        projeto = SimpleNamespace(cor_slug="blue")
        assert projeto_color_bar(projeto) == "bg-blue-500"
