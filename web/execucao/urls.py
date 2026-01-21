from django.urls import path

from . import views

app_name = "execucao"

urlpatterns = [
    path("historico/", views.historico, name="historico"),
]
