# Create your views here.
from django.views.generic import TemplateView


class AcessoNegadoView(TemplateView):
    template_name = "iam/acesso_negado.html"
