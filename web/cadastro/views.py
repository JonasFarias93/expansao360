# web/cadastro/views.py

from django.contrib import messages
from django.db.models import IntegerField, Q
from django.db.models.functions import Cast
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.http import require_GET
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
from iam.mixins import CapabilityRequiredMixin

from .forms import (
    CategoriaForm,
    EquipamentoForm,
    ItemKitFormSet,
    KitForm,
    LojaForm,
    ProjetoForm,
    SubprojetoForm,
    TipoEquipamentoFormSet,
)
from .models import Categoria, Equipamento, Kit, Loja, Projeto, Subprojeto, TipoEquipamento


class CadastroHomeView(TemplateView):
    template_name = "cadastro/home.html"


# ============================
# AJAX: TIPOS POR EQUIPAMENTO
# ============================


@require_GET
def tipos_por_equipamento(request):
    equipamento_id = (request.GET.get("equipamento_id") or "").strip()

    # compat antigo: ?equipamento=123
    if not equipamento_id:
        equipamento_id = (request.GET.get("equipamento") or "").strip()

    # compat formset: ?itens-0-equipamento=123
    if not equipamento_id:
        for k, v in request.GET.items():
            if k.endswith("-equipamento"):
                equipamento_id = (v or "").strip()
                break

    if not equipamento_id.isdigit():
        return JsonResponse([], safe=False)

    equipamento = get_object_or_404(
        Equipamento.objects.select_related("categoria"),
        pk=int(equipamento_id),
    )

    tipos = (
        TipoEquipamento.objects.filter(categoria=equipamento.categoria, disponivel=True)
        .order_by("nome")
        .values("id", "nome")
    )

    return JsonResponse(list(tipos), safe=False)


# -----------------------
# LOJAS
# -----------------------
class LojaListView(CapabilityRequiredMixin, ListView):
    model = Loja
    template_name = "cadastro/lojas_list.html"
    context_object_name = "lojas"
    required_capability = "cadastro.visualizar"

    def get_paginate_by(self, queryset):
        per_page = self.request.GET.get("per_page", "25")
        if per_page == "all":
            return 5000
        try:
            n = int(per_page)
        except ValueError:
            return 25
        return max(10, min(n, 200))  # mínimo 10, máximo 200

    def get_queryset(self):
        qs = super().get_queryset()

        # mantém seu comportamento atual de ordenação (já existe no seu código)
        qs = qs.annotate(codigo_int=Cast("codigo", IntegerField())).order_by(
            "codigo_int",
            "nome",
        )

        q = (self.request.GET.get("q") or "").strip()
        if not q:
            return qs

        # Regras:
        # - se numérico: tentar bater em Java (codigo) OU histórico (hist)
        # - se texto: procurar por nome (icontains) e opcional cidade/uf
        if q.isdigit():
            return qs.filter(Q(codigo__iexact=q) | Q(hist__iexact=q))

        # texto
        return qs.filter(Q(nome__icontains=q) | Q(cidade__icontains=q) | Q(uf__icontains=q))


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
# CATEGORIAS (CRUD + tipos inline)
# -----------------------
class CategoriaListView(CapabilityRequiredMixin, ListView):
    model = Categoria
    template_name = "cadastro/categorias_list.html"
    context_object_name = "categorias"
    ordering = ["nome"]
    required_capability = "cadastro.visualizar"


class CategoriaCreateView(CapabilityRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "cadastro/categorias_form.html"
    required_capability = "cadastro.editar"

    def get_success_url(self):
        return reverse_lazy("registry:categoria_update", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Categoria criada. Agora cadastre os tipos.")
        return super().form_valid(form)


class CategoriaUpdateView(CapabilityRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "cadastro/categorias_update.html"
    success_url = reverse_lazy("registry:categoria_list")
    required_capability = "cadastro.editar"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = TipoEquipamentoFormSet(instance=self.object)
        return render(
            request,
            self.template_name,
            {"form": form, "formset": formset, "categoria": self.object},
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = TipoEquipamentoFormSet(request.POST, instance=self.object)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Categoria e tipos atualizados com sucesso.")
            return redirect(self.success_url)

        return render(
            request,
            self.template_name,
            {"form": form, "formset": formset, "categoria": self.object},
        )


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


class KitItensApiView(CapabilityRequiredMixin, View):
    """
    Endpoint read-only para lazy-load dos itens do kit.
    Permissões: mesmas regras da visualização da listagem (KitListView).
    """

    required_capability = "cadastro.visualizar"

    def get(self, request, pk: int, *args, **kwargs):
        kit = get_object_or_404(Kit, pk=pk)

        itens_qs = kit.itens.select_related("equipamento", "tipo").order_by(
            "equipamento__nome",
            "tipo__nome",
        )

        itens = [
            {
                "nome": i.nome_exibicao,  # "Equipamento Tipo"
                "quantidade": i.quantidade,
                "tipo": i.tipo.nome,
                "requer_configuracao": i.requer_configuracao,
            }
            for i in itens_qs
        ]

        payload = {
            "kit": {"id": kit.id, "nome": kit.nome},  # nome opcional (ok manter)
            "itens": itens,
        }
        return JsonResponse(payload)
