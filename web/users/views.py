# web/users/views.py
from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView

from iam.mixins import CapabilityRequiredMixin
from iam.models import Capability, UserCapability
from users.forms import UserCreateForm, UserProfileForm
from users.models import UserProfile

User = get_user_model()

CAP_USERS_ADMIN = "users.admin"


class UsersHomeView(CapabilityRequiredMixin, TemplateView):
    template_name = "users/home.html"
    required_capability = CAP_USERS_ADMIN


class UserListView(CapabilityRequiredMixin, TemplateView):
    template_name = "users/user_list.html"
    required_capability = CAP_USERS_ADMIN

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        users = (
            User.objects.all()
            .select_related("profile")
            .order_by("username")
        )
        ctx["users"] = users
        return ctx


class UserCreateView(CapabilityRequiredMixin, View):
    required_capability = CAP_USERS_ADMIN
    template_name = "users/user_create.html"

    def get(self, request):
        return render(request, self.template_name, {"form": UserCreateForm()})

    @transaction.atomic
    def post(self, request):
        form = UserCreateForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
            first_name=form.cleaned_data.get("first_name", ""),
            last_name=form.cleaned_data.get("last_name", ""),
            email=form.cleaned_data.get("email", ""),
        )
        UserProfile.objects.create(
            user=user,
            perfil=form.cleaned_data["perfil"],
            equipe=form.cleaned_data.get("equipe", ""),
        )

        perfil_nome = form.cleaned_data["perfil"].lower()
        grupo_map = {
            "tecnico": "tecnico",
            "coordenador": "tecnico",
            "logistica": "tecnico",
            "auditor": "administrador",
            "administrador": "administrador",
        }
        grupo_nome = grupo_map.get(perfil_nome, "tecnico")
        try:
            grupo = Group.objects.get(name=grupo_nome)
            user.groups.add(grupo)
        except Group.DoesNotExist:
            pass

        messages.success(request, f"Usuário {user.username} criado com sucesso.")
        return redirect("users:user_detail", user_id=user.pk)


class UserDetailView(CapabilityRequiredMixin, TemplateView):
    required_capability = CAP_USERS_ADMIN
    template_name = "users/user_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = get_object_or_404(User.objects.select_related("profile"), pk=kwargs["user_id"])
        capabilities = UserCapability.objects.filter(user=user).select_related("capability")
        capability_ids = set(capabilities.values_list("capability_id", flat=True))
        all_capabilities = Capability.objects.all()
        ctx["u"] = user
        ctx["capabilities"] = capabilities
        ctx["all_capabilities"] = all_capabilities
        ctx["capability_ids"] = capability_ids
        return ctx


class UserEditView(CapabilityRequiredMixin, View):
    required_capability = CAP_USERS_ADMIN
    template_name = "users/user_edit.html"

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        form = UserProfileForm(instance=profile)
        return render(request, self.template_name, {"form": form, "u": user})

    @transaction.atomic
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        form = UserProfileForm(request.POST, instance=profile)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form, "u": user})
        form.save()
        messages.success(request, "Perfil atualizado.")
        return redirect("users:user_detail", user_id=user.pk)


class UserCapabilitiesView(CapabilityRequiredMixin, View):
    required_capability = CAP_USERS_ADMIN

    @transaction.atomic
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        selected = set(request.POST.getlist("capabilities"))
        all_caps = Capability.objects.all()

        for cap in all_caps:
            if str(cap.pk) in selected:
                UserCapability.objects.get_or_create(user=user, capability=cap)
            else:
                UserCapability.objects.filter(user=user, capability=cap).delete()

        messages.success(request, "Capabilities atualizadas.")
        return redirect("users:user_detail", user_id=user.pk)