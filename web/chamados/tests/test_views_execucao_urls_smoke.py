from __future__ import annotations

import pytest
from django.urls import resolve, reverse

from chamados import views as chamados_views


@pytest.mark.parametrize(
    "url_name, kwargs, expected_view_class, expected_module_prefix",
    [
        ("execucao:fila", None, chamados_views.ChamadoFilaView, "chamados.views.fila"),
        (
            "execucao:historico",
            None,
            chamados_views.HistoricoView,
            "chamados.views.historico",
        ),
        (
            "execucao:chamado_create",
            None,
            chamados_views.ChamadoCreateView,
            "chamados.views.abertura",
        ),
        (
            "execucao:chamado_setup",
            {"chamado_id": 123},
            chamados_views.ChamadoSetupView,
            "chamados.views.setup",
        ),
        (
            "execucao:chamado_detalhe",
            {"chamado_id": 123},
            chamados_views.ChamadoExecucaoView,
            "chamados.views.execucao",
        ),
    ],
)
def test_quando_reverse_resolve_rotas_principais_entao_view_e_modulo_corretos(
    url_name: str,
    kwargs: dict | None,
    expected_view_class,
    expected_module_prefix: str,
) -> None:
    """
    Contrato: após split (chamados/views.py -> chamados/views/*),
    as rotas principais continuam resolvendo para as views esperadas.
    """
    url = reverse(url_name, kwargs=kwargs)
    match = resolve(url)

    assert hasattr(match.func, "view_class")
    assert match.func.view_class is expected_view_class
    assert match.func.view_class.__module__.startswith(expected_module_prefix)


def test_quando_reverse_resolve_ajax_subprojetos_entao_function_view_esperada() -> None:
    """
    Contrato: endpoint function-based continua resolvendo após split.
    """
    url = reverse("execucao:ajax_subprojetos")
    match = resolve(url)

    assert match.func is chamados_views.subprojetos_por_projeto
    assert match.func.__module__.startswith("chamados.views.abertura")
