# web/execucao/urls.py
from django.urls import path

from . import views

app_name = "execucao"

urlpatterns = [
    path("", views.ChamadoFilaView.as_view(), name="fila"),
    path("historico/", views.HistoricoView.as_view(), name="historico"),
    # CHAMADO
    path("chamados/novo/", views.ChamadoCreateView.as_view(), name="chamado_create"),
    path(
        "chamados/<int:chamado_id>/setup/",
        views.ChamadoSetupView.as_view(),
        name="chamado_setup",
    ),
    path(
        "chamados/<int:chamado_id>/",
        views.ChamadoDetailView.as_view(),
        name="chamado_detalhe",
    ),
    path(
        "chamados/<int:chamado_id>/itens/",
        views.ChamadoAtualizarItensView.as_view(),
        name="chamado_atualizar_itens",
    ),
    path(
        "chamados/<int:chamado_id>/contabil/",
        views.ChamadoInformarContabilView.as_view(),
        name="chamado_informar_contabil",
    ),
    path(
        "chamados/<int:chamado_id>/nf-saida/",
        views.ChamadoInformarNFSaidaView.as_view(),
        name="chamado_informar_nf_saida",
    ),
    path(
        "chamados/<int:chamado_id>/confirmar-coleta/",
        views.ChamadoConfirmarColetaView.as_view(),
        name="chamado_confirmar_coleta",
    ),
    path(
        "chamados/<int:chamado_id>/finalizar/",
        views.ChamadoFinalizarView.as_view(),
        name="chamado_finalizar",
    ),
    path("ajax/subprojetos/", views.subprojetos_por_projeto, name="ajax_subprojetos"),
    # EVIDÊNCIAS
    path(
        "chamados/<int:chamado_id>/evidencias/add/",
        views.ChamadoAdicionarEvidenciaView.as_view(),
        name="chamado_adicionar_evidencia",
    ),
    path(
        "chamados/<int:chamado_id>/evidencias/<int:evidencia_id>/remover/",
        views.EvidenciaRemoverView.as_view(),
        name="evidencia_remover",
    ),
    # ITENS
    path(
        "chamados/<int:chamado_id>/itens/<int:item_id>/status/",
        views.ItemSetStatusConfiguracaoView.as_view(),
        name="item_set_status_configuracao",
    ),
]
