# web/chamados/urls.py
from django.urls import path
from execucao import views as execucao_views

from chamados import views as chamados_views
from chamados.api_views import loja_lookup_por_codigo

app_name = "chamados"

urlpatterns = [
    # ======================
    # FILA / HISTÓRICO
    # ======================
    path("", chamados_views.ChamadoFilaView.as_view(), name="fila"),
    path("historico/", chamados_views.HistoricoView.as_view(), name="historico"),
    # ======================
    # CHAMADO
    # ======================
    # Abertura
    path(
        "chamados/novo/",
        chamados_views.ChamadoSelecaoView.as_view(),
        name="chamado_selecao",
    ),
    path(
        "chamados/novo/projeto/",
        chamados_views.ChamadoCreateView.as_view(),
        name="chamado_create_projeto",
    ),
    path(
        "chamados/novo/avulso/",
        chamados_views.ChamadoCreateAvulsoView.as_view(),
        name="chamado_create_avulso",
    ),
    
    # Setup (planejamento) — status ABERTO
    path(
        "chamados/<int:chamado_id>/setup/",
        chamados_views.ChamadoSetupView.as_view(),
        name="chamado_setup",
    ),
    # Detalhe / Execução — status != ABERTO
    path(
        "chamados/<int:chamado_id>/",
        chamados_views.ChamadoExecucaoView.as_view(),
        name="chamado_detalhe",  # mantido por compatibilidade
    ),
    path("api/lojas/lookup/", loja_lookup_por_codigo, name="api_loja_lookup"),
    # ======================
    # SESSÃO / LOCKING (mantido por enquanto em execucao_views)
    # ======================
    path(
        "chamados/<int:chamado_id>/take-session/",
        execucao_views.chamado_take_session,
        name="chamado_take_session",
    ),
    path(
        "chamados/<int:chamado_id>/abrir/",
        execucao_views.chamado_abrir,
        name="chamado_abrir",
    ),
    # ======================
    # ITENS DO CHAMADO
    # ======================
    path(
        "chamados/<int:chamado_id>/itens/",
        chamados_views.ChamadoAtualizarItensView.as_view(),
        name="chamado_atualizar_itens",
    ),
    path(
        "chamados/<int:chamado_id>/itens/<int:item_id>/status/",
        chamados_views.ItemSetStatusConfiguracaoView.as_view(),
        name="item_set_status_configuracao",
    ),
    # ======================
    # AÇÕES OPERACIONAIS
    # ======================
    path(
        "chamados/<int:chamado_id>/contabil/",
        chamados_views.ChamadoInformarContabilView.as_view(),
        name="chamado_informar_contabil",
    ),
    path(
        "chamados/<int:chamado_id>/nf-saida/",
        chamados_views.ChamadoInformarNFSaidaView.as_view(),
        name="chamado_informar_nf_saida",
    ),
    path(
        "chamados/<int:chamado_id>/confirmar-coleta/",
        chamados_views.ChamadoConfirmarColetaView.as_view(),
        name="chamado_confirmar_coleta",
    ),
    path(
        "chamados/<int:chamado_id>/finalizar/",
        chamados_views.ChamadoFinalizarView.as_view(),
        name="chamado_finalizar",
    ),
    path(
        "chamado/<int:chamado_id>/salvar-dados-fiscais/",
        chamados_views.ChamadoSalvarDadosFiscaisView.as_view(),
        name="chamado_salvar_dados_fiscais",
    ),
    path(
        "chamados/<int:chamado_id>/salvar/",
        chamados_views.ChamadoSalvarExecucaoView.as_view(),
        name="chamado_salvar_execucao_ajax",
    ),
    path(
        "itens/<int:item_id>/configurar/",
        chamados_views.ItemMarcarConfiguradoView.as_view(),
        name="item_configurar",
    ),
    path(
    "chamados/<int:chamado_id>/cancelar/",
    chamados_views.ChamadoCancelarView.as_view(),
    name="chamado_cancelar",
),
    # ======================
    # EVIDÊNCIAS
    # ======================
    path(
        "chamados/<int:chamado_id>/evidencias/add/",
        chamados_views.ChamadoAdicionarEvidenciaView.as_view(),
        name="chamado_adicionar_evidencia",
    ),
    path(
        "chamados/<int:chamado_id>/evidencias/<int:evidencia_id>/remover/",
        chamados_views.EvidenciaRemoverView.as_view(),
        name="evidencia_remover",
    ),
    # ======================
    # AJAX
    # ======================
    path(
        "ajax/subprojetos/",
        chamados_views.subprojetos_por_projeto,
        name="ajax_subprojetos",
    ),
]
