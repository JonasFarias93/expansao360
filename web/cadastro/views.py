# web/cadastro/views.py
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
from iam.mixins import CapabilityRequiredMixin

from .forms import (
    EquipamentoForm,
    ItemKitFormSet,
    KitForm,
    LojaForm,
    ProjetoForm,
    SubprojetoForm,
)
from .models import Categoria, Equipamento, Kit, Loja, Projeto, Subprojeto


class CadastroHomeView(CapabilityRequiredMixin, TemplateView):
    template_name = "cadastro/home.html"
    required_capability = "cadastro.visualizar"


# -----------------------
# LOJAS
# -----------------------
class LojaListView(CapabilityRequiredMixin, ListView):
    model = Loja
    template_name = "cadastro/lojas_list.html"
    context_object_name = "lojas"
    ordering = ["codigo"]
    required_capability = "cadastro.visualizar"


class LojaCreateView(CapabilityRequiredMixin, CreateView):
    model = Loja
    form_class = LojaForm
    template_name = "cadastro/lojas_form.html"
    success_url = reverse_lazy("registry:loja_list")
    required_capability = "cadastro.editar"

    def form_valid(self, form):
        messages.success(self.request, "Loja cadastrada com sucesso.")
        return super().form_valid(form)


class LojaUpdateView(CapabilityRequiredMixin, UpdateView):
    model = Loja
    form_class = LojaForm
    template_name = "cadastro/lojas_form.html"
    success_url = reverse_lazy("registry:loja_list")
    required_capability = "cadastro.editar"

    def form_valid(self, form):
        messages.success(self.request, "Loja atualizada com sucesso.")
        return super().form_valid(form)


# -----------------------
# PROJETOS
# -----------------------
class ProjetoListView(CapabilityRequiredMixin, ListView):
    model = Projeto
    template_name = "cadastro/projetos_list.html"
    context_object_name = "projetos"
    ordering = ["codigo"]
    required_capability = "cadastro.visualizar"


class ProjetoCreateView(CapabilityRequiredMixin, CreateView):
    model = Projeto
    form_class = ProjetoForm
    template_name = "cadastro/projetos_form.html"
    success_url = reverse_lazy("registry:projeto_list")
    required_capability = "cadastro.editar"

    def form_valid(self, form):
        messages.success(self.request, "Projeto cadastrado com sucesso.")
        return super().form_valid(form)


class ProjetoUpdateView(CapabilityRequiredMixin, UpdateView):
    model = Projeto
    form_class = ProjetoForm
    template_name = "cadastro/projetos_form.html"
    success_url = reverse_lazy("registry:projeto_list")
    required_capability = "cadastro.editar"

    def form_valid(self, form):
        messages.success(self.request, "Projeto atualizado com sucesso.")
        return super().form_valid(form)


# -----------------------
# SUBPROJETOS
# -----------------------
class SubprojetoListView(CapabilityRequiredMixin, ListView):
    model = Subprojeto
    template_name = "cadastro/subprojetos_list.html"
    context_object_name = "subprojetos"
    required_capability = "cadastro.visualizar"

    def get_queryset(self):
        qs = (
            Subprojeto.objects.select_related("projeto").all().order_by("projeto__codigo", "codigo")
        )

        projeto_id = self.request.GET.get("projeto")
        if projeto_id:
            qs = qs.filter(projeto_id=projeto_id)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["projetos"] = Projeto.objects.all().order_by("codigo", "nome")
        ctx["projeto_selected"] = (self.request.GET.get("projeto") or "").strip()
        return ctx


class SubprojetoCreateView(CapabilityRequiredMixin, CreateView):
    model = Subprojeto
    form_class = SubprojetoForm
    template_name = "cadastro/subprojetos_form.html"
    success_url = reverse_lazy("registry:subprojeto_list")
    required_capability = "cadastro.editar"

    def get_initial(self):
        initial = super().get_initial()
        projeto_id = self.request.GET.get("projeto")
        if projeto_id:
            initial["projeto"] = projeto_id
        return initial

    def form_valid(self, form):
        messages.success(self.request, "Subprojeto cadastrado com sucesso.")
        return super().form_valid(form)


class SubprojetoUpdateView(CapabilityRequiredMixin, UpdateView):
    model = Subprojeto
    form_class = SubprojetoForm
    template_name = "cadastro/subprojetos_form.html"
    success_url = reverse_lazy("registry:subprojeto_list")
    required_capability = "cadastro.editar"

    def form_valid(self, form):
        messages.success(self.request, "Subprojeto atualizado com sucesso.")
        return super().form_valid(form)


# -----------------------
# EQUIPAMENTOS
# -----------------------
class EquipamentoListView(CapabilityRequiredMixin, ListView):
    model = Equipamento
    template_name = "cadastro/equipamentos_list.html"
    context_object_name = "equipamentos"
    ordering = ["codigo"]
    required_capability = "cadastro.visualizar"


class EquipamentoCreateView(CapabilityRequiredMixin, CreateView):
    model = Equipamento
    form_class = EquipamentoForm
    template_name = "cadastro/equipamentos_create.html"
    success_url = reverse_lazy("registry:equipamento_list")
    required_capability = "cadastro.editar"

    def get_initial(self):
        initial = super().get_initial()
        categoria_id = self.request.GET.get("categoria")
        if categoria_id:
            initial["categoria"] = categoria_id
        return initial

    def form_valid(self, form):
        messages.success(self.request, "Equipamento cadastrado com sucesso.")
        return super().form_valid(form)


class EquipamentoUpdateView(CapabilityRequiredMixin, UpdateView):
    model = Equipamento
    form_class = EquipamentoForm
    template_name = "cadastro/equipamentos_form.html"
    success_url = reverse_lazy("registry:equipamento_list")
    required_capability = "cadastro.editar"

    def form_valid(self, form):
        messages.success(self.request, "Equipamento atualizado com sucesso.")
        return super().form_valid(form)


# -----------------------
# CATEGORIAS (quick-create no modal)
# -----------------------
class CategoriaCreateQuickView(CapabilityRequiredMixin, View):
    required_capability = "cadastro.editar"

    def post(self, request, *args, **kwargs):
        nome = (request.POST.get("nome") or "").strip()
        next_url = request.POST.get("next") or reverse("registry:equipamento_create")

        if not nome:
            messages.error(request, "Informe o nome da categoria.")
            return redirect(next_url)

        categoria, created = Categoria.objects.get_or_create(nome=nome)

        if created:
            messages.success(request, "Categoria cadastrada com sucesso.")
        else:
            messages.info(request, "Categoria já existia. Selecionamos ela para você.")

        sep = "&" if "?" in next_url else "?"
        return redirect(f"{next_url}{sep}categoria={categoria.id}")


# -----------------------
# KITS (com itens inline)
# -----------------------
class KitListView(CapabilityRequiredMixin, ListView):
    model = Kit
    template_name = "cadastro/kits_list.html"
    context_object_name = "kits"
    ordering = ["nome"]
    required_capability = "cadastro.visualizar"


class KitCreateView(CapabilityRequiredMixin, CreateView):
    model = Kit
    form_class = KitForm
    template_name = "cadastro/kits_create.html"
    required_capability = "cadastro.editar"

    def get_success_url(self):
        # após criar, já vai pra tela de editar (pra adicionar itens)
        return reverse_lazy("registry:kit_update", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Kit criado. Agora adicione os itens do kit.")
        return super().form_valid(form)


class KitUpdateView(CapabilityRequiredMixin, UpdateView):
    model = Kit
    form_class = KitForm
    template_name = "cadastro/kits_update.html"
    success_url = reverse_lazy("registry:kit_list")
    required_capability = "cadastro.editar"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = ItemKitFormSet(instance=self.object)
        return render(
            request,
            self.template_name,
            {"form": form, "formset": formset, "kit": self.object},
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = ItemKitFormSet(request.POST, instance=self.object)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Kit e itens atualizados com sucesso.")
            return redirect(self.success_url)

        return render(
            request,
            self.template_name,
            {"form": form, "formset": formset, "kit": self.object},
        )
