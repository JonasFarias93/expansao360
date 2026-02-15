from types import SimpleNamespace

from web.execucao.templatetags.execucao_urgencia import (
    urgencia_badge_class,
    urgencia_label,
)


class TestUrgenciaTemplateTags:
    def test_urgencia_defaults_to_normal_when_missing(self):
        chamado = SimpleNamespace()
        assert urgencia_label(chamado) == "PADRÃO"
        assert "slate" in urgencia_badge_class(chamado)

    def test_urgencia_reads_prioridade_field(self):
        chamado = SimpleNamespace(prioridade="ALTA")
        assert urgencia_label(chamado) == "ALTO"
        assert "amber" in urgencia_badge_class(chamado)

    def test_urgencia_reads_urgencia_field_critica(self):
        chamado = SimpleNamespace(urgencia="CRITICA")
        assert urgencia_label(chamado) == "CRÍTICO"
        assert "rose" in urgencia_badge_class(chamado)

    def test_urgencia_unknown_falls_back_to_normal(self):
        chamado = SimpleNamespace(prioridade="QUALQUER_COISA")
        assert urgencia_label(chamado) == "NORMAL"
        assert "slate" in urgencia_badge_class(chamado)

    def test_urgencia_mais_antigo_is_padrao(self):
        chamado = SimpleNamespace(prioridade="MAIS_ANTIGO")
        assert urgencia_label(chamado) == "PADRÃO"
