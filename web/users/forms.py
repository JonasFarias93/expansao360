# web/users/forms.py
from __future__ import annotations

from django import forms
from django.contrib.auth import get_user_model
from users.models import UserProfile

User = get_user_model()


class UserCreateForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")
    first_name = forms.CharField(max_length=80, label="Nome", required=False)
    last_name = forms.CharField(max_length=80, label="Sobrenome", required=False)
    email = forms.EmailField(label="Email", required=False)
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")
    perfil = forms.ChoiceField(choices=UserProfile.Perfil.choices, label="Perfil")
    equipe = forms.CharField(max_length=80, label="Equipe", required=False)

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username já existe.")
        return username


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["perfil", "status", "equipe", "supervisor", "observacoes"]
        widgets = {
            "observacoes": forms.Textarea(attrs={"rows": 3}),
        }