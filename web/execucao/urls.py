from django.urls import path

from . import views

app_name = "execucao"

urlpatterns = [
    path("historico/", views.historico, name="historico"),
    path("chamado/<int:chamado_id>/", views.chamado_detalhe, name="chamado_detalhe"),
    path(
        "chamado/<int:chamado_id>/itens/",
        views.chamado_atualizar_itens,
        name="chamado_atualizar_itens",
    ),
    path(
        "chamado/<int:chamado_id>/finalizar/",
        views.chamado_finalizar,
        name="chamado_finalizar",
    ),
]
