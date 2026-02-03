from django.urls import path

from . import views

app_name = "registry"

urlpatterns = [
    # HOME do Cadastro
    path("", views.CadastroHomeView.as_view(), name="home"),
    # ======================
    # GESTÃO (listas)
    # ======================
    # Lojas
    path("lojas/", views.LojaListView.as_view(), name="loja_list"),
    # Projetos
    path("projetos/", views.ProjetoListView.as_view(), name="projeto_list"),
    path("subprojetos/", views.SubprojetoListView.as_view(), name="subprojeto_list"),
    # kits
    path("kits/", views.KitListView.as_view(), name="kit_list"),
    # Equipamento
    path("equipamentos/", views.EquipamentoListView.as_view(), name="equipamento_list"),
    # ======================
    # CADASTROS (novo)
    # ======================
    # Lojas
    path("lojas/novo/", views.LojaCreateView.as_view(), name="loja_create"),
    # Projetos
    path("projetos/novo/", views.ProjetoCreateView.as_view(), name="projeto_create"),
    path(
        "subprojetos/novo/",
        views.SubprojetoCreateView.as_view(),
        name="subprojeto_create",
    ),
    # Kits
    path("kits/novo/", views.KitCreateView.as_view(), name="kit_create"),
    # Equipamento
    path(
        "equipamentos/novo/",
        views.EquipamentoCreateView.as_view(),
        name="equipamento_create",
    ),
    # ======================
    # EDIÇÃO
    # ======================
    path("lojas/<int:pk>/editar/", views.LojaUpdateView.as_view(), name="loja_update"),
    path(
        "projetos/<int:pk>/editar/",
        views.ProjetoUpdateView.as_view(),
        name="projeto_update",
    ),
    path(
        "subprojetos/<int:pk>/editar/",
        views.SubprojetoUpdateView.as_view(),
        name="subprojeto_update",
    ),
    path("kits/<int:pk>/editar/", views.KitUpdateView.as_view(), name="kit_update"),
    path(
        "equipamentos/<int:pk>/editar/",
        views.EquipamentoUpdateView.as_view(),
        name="equipamento_update",
    ),
    # ======================
    # CATEGORIAS (quick-create)
    # ======================
    path(
        "categorias/novo/quick/",
        views.CategoriaCreateQuickView.as_view(),
        name="categoria_create_quick",
    ),
]
