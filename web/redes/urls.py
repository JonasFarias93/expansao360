from django.urls import include, path

app_name = "redes"

urlpatterns = [
    path("", include("chamados.urls")),
    path("cadastro/", include("cadastro.urls")),
]
