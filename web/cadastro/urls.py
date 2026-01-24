from django.urls import path

from . import views

app_name = "registry"

urlpatterns = [
    # GESTÃO (listas)
    path("lojas/", views.LojaListView.as_view(), name="loja_list"),
    path("projetos/", views.ProjetoListView.as_view(), name="projeto_list"),
    path("kits/", views.KitListView.as_view(), name="kit_list"),
    path("equipamentos/", views.EquipamentoListView.as_view(), name="equipamento_list"),
    # CADASTROS (novo)
    path("lojas/novo/", views.LojaCreateView.as_view(), name="loja_create"),
    path("projetos/novo/", views.ProjetoCreateView.as_view(), name="projeto_create"),
    path("kits/novo/", views.KitCreateView.as_view(), name="kit_create"),
    path("equipamentos/novo/", views.EquipamentoCreateView.as_view(), name="equipamento_create"),
]
