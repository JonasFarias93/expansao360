# web/execucao/urls.py
from django.urls import include, path

app_name = "execucao"

urlpatterns = [
    path("", include(("chamados.urls", "execucao"), namespace="execucao")),
]
