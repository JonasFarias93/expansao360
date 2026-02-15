from types import SimpleNamespace

from web.execucao.templatetags.execucao_projeto_cores import projeto_color_bar


class TestProjetoCoresTemplateTags:
    def test_projeto_color_bar_fallback_to_slate_when_missing(self):
        projeto = SimpleNamespace(cor_slug=None)
        assert projeto_color_bar(projeto) == "bg-slate-200"

    def test_projeto_color_bar_maps_known_color(self):
        projeto = SimpleNamespace(cor_slug="blue")
        assert projeto_color_bar(projeto) == "bg-blue-500"

    def test_projeto_color_bar_unknown_color_fallback(self):
        projeto = SimpleNamespace(cor_slug="unknown")
        assert projeto_color_bar(projeto) == "bg-slate-200"
