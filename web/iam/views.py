# Create your views here.
from django.shortcuts import render
from django.views.generic import TemplateView


class AcessoNegadoView(TemplateView):
    template_name = "iam/acesso_negado.html"


def acesso_negado_403(request, exception=None):
    return render(
        request,
        "iam/acesso_negado.html",
        {"acao": "executar esta ação"},
        status=403,
    )
