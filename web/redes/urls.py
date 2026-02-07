from django.urls import include, path

app_name = "redes"

urlpatterns = [
    path("", include("execucao.urls")),
    path("cadastro/", include("cadastro.urls")),
]
