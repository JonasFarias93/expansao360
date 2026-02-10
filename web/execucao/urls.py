# web/execucao/urls.py
from django.urls import path

from . import views
from .api_views import loja_lookup_por_codigo

app_name = "execucao"

urlpatterns = [
    # ======================
    # FILA / HISTÓRICO
    # ======================
    path("", views.ChamadoFilaView.as_view(), name="fila"),
    path("historico/", views.HistoricoView.as_view(), name="historico"),
    # ======================
    # CHAMADO
    # ======================
    # Abertura
    path(
        "chamados/novo/",
        views.ChamadoCreateView.as_view(),
        name="chamado_create",
    ),
    # Setup (planejamento) — status ABERTO
    path(
        "chamados/<int:chamado_id>/setup/",
        views.ChamadoSetupView.as_view(),
        name="chamado_setup",
    ),
    # Detalhe / Execução — status != ABERTO
    path(
        "chamados/<int:chamado_id>/",
        views.ChamadoExecucaoView.as_view(),
        name="chamado_detalhe",  # mantido por compatibilidade
    ),
    path("api/lojas/lookup/", loja_lookup_por_codigo, name="api_loja_lookup"),
    path(
        "chamados/<int:chamado_id>/take-session/",
        views.chamado_take_session,
        name="chamado_take_session",
    ),
    # ======================
    # ITENS DO CHAMADO
    # ======================
    path(
        "chamados/<int:chamado_id>/itens/",
        views.ChamadoAtualizarItensView.as_view(),
        name="chamado_atualizar_itens",
    ),
    path(
        "chamados/<int:chamado_id>/itens/<int:item_id>/status/",
        views.ItemSetStatusConfiguracaoView.as_view(),
        name="item_set_status_configuracao",
    ),
    path("chamados/<int:chamado_id>/abrir/", views.chamado_abrir, name="chamado_abrir"),
    # ======================
    # AÇÕES OPERACIONAIS
    # ======================
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
    path(
        "chamado/<int:chamado_id>/salvar-dados-fiscais/",
        views.ChamadoSalvarDadosFiscaisView.as_view(),
        name="chamado_salvar_dados_fiscais",
    ),
    path(
        "chamados/<int:chamado_id>/salvar/",
        views.ChamadoSalvarExecucaoView.as_view(),
        name="chamado_salvar_execucao",
    ),
    path(
        "itens/<int:item_id>/configurar/",
        views.ItemMarcarConfiguradoView.as_view(),
        name="item_configurar",
    ),
    # ======================
    # EVIDÊNCIAS
    # ======================
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
    # ======================
    # AJAX
    # ======================
    path(
        "ajax/subprojetos/",
        views.subprojetos_por_projeto,
        name="ajax_subprojetos",
    ),
]
