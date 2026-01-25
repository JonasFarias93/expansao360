from django.urls import path

from .views import AcessoNegadoView

app_name = "iam"

urlpatterns = [
    path("acesso-negado/", AcessoNegadoView.as_view(), name="acesso_negado"),
]
