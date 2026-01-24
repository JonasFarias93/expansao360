from django.views.generic import TemplateView
from iam.mixins import CapabilityRequiredMixin


# Home do Cadastro
class CadastroHomeView(CapabilityRequiredMixin, TemplateView):
    template_name = "cadastro/home.html"
    required_capability = "cadastro.visualizar"


# Lojas
class LojaListView(CapabilityRequiredMixin, TemplateView):
    template_name = "cadastro/lojas_list.html"
    required_capability = "cadastro.visualizar"


class LojaCreateView(CapabilityRequiredMixin, TemplateView):
    template_name = "cadastro/lojas_create.html"
    required_capability = "cadastro.editar"


# Projetos
class ProjetoListView(CapabilityRequiredMixin, TemplateView):
    template_name = "cadastro/projetos_list.html"
    required_capability = "cadastro.visualizar"


class ProjetoCreateView(CapabilityRequiredMixin, TemplateView):
    template_name = "cadastro/projetos_create.html"
    required_capability = "cadastro.editar"


# Kits
class KitListView(CapabilityRequiredMixin, TemplateView):
    template_name = "cadastro/kits_list.html"
    required_capability = "cadastro.visualizar"


class KitCreateView(CapabilityRequiredMixin, TemplateView):
    template_name = "cadastro/kits_create.html"
    required_capability = "cadastro.editar"


# Equipamentos
class EquipamentoListView(CapabilityRequiredMixin, TemplateView):
    template_name = "cadastro/equipamentos_list.html"
    required_capability = "cadastro.visualizar"


class EquipamentoCreateView(CapabilityRequiredMixin, TemplateView):
    template_name = "cadastro/equipamentos_create.html"
    required_capability = "cadastro.editar"
