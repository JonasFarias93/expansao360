from types import SimpleNamespace

from web.execucao.templatetags.execucao_urgencia import urgencia_badge_class, urgencia_label


def test_urgencia_defaults_to_normal_when_missing():
    chamado = SimpleNamespace()
    assert urgencia_label(chamado) == "PADRÃO"
    assert "slate" in urgencia_badge_class(chamado)


def test_urgencia_reads_prioridade_field():
    chamado = SimpleNamespace(prioridade="ALTA")
    assert urgencia_label(chamado) == "ALTO"
    assert "amber" in urgencia_badge_class(chamado)


def test_urgencia_reads_urgencia_field_critica():
    chamado = SimpleNamespace(urgencia="CRITICA")
    assert urgencia_label(chamado) == "CRÍTICO"
    assert "rose" in urgencia_badge_class(chamado)


def test_urgencia_unknown_falls_back_to_normal():
    chamado = SimpleNamespace(prioridade="QUALQUER_COISA")
    assert urgencia_label(chamado) == "NORMAL"
    assert "slate" in urgencia_badge_class(chamado)


def test_urgencia_mais_antigo_is_padrao():
    chamado = SimpleNamespace(prioridade="MAIS_ANTIGO")
    assert urgencia_label(chamado) == "PADRÃO"
