# web/historico/urls.py
from django.urls import path
from historico import views

app_name = "historico"

urlpatterns = [
    path(
        "chamados/<int:chamado_id>/",
        views.HistoricoExecucaoDetalheView.as_view(),
        name="execucao_detalhe",
    ),
    path(
        "lojas/<str:loja_codigo>/",
        views.HistoricoLojaView.as_view(),
        name="loja",
    ),
    path(
        "ativos/<str:ativo>/",
        views.HistoricoAtivoTimelineView.as_view(),
        name="ativo_timeline",
    ),
    path(
    "",
    views.HistoricoBuscaView.as_view(),
    name="busca",
),
]