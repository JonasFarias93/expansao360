# web/config/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import include, path
from django.contrib.auth import views as auth_views


def root_redirect(request):
    return redirect("execucao:fila")


urlpatterns = [
    
    path("login/", auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("admin/", admin.site.urls),
    path("", root_redirect),
    # Operation
    path("execucao/", include("chamados.urls")),
    path("execucao/", include(("chamados.urls", "execucao"), namespace="execucao")),
    # Registry (cadastro)
    path("cadastro/", include(("cadastro.urls", "cadastro"), namespace="cadastro")),
    # IAM
    path("iam/", include(("iam.urls", "iam"), namespace="iam")),
    path("redes/", include(("redes.urls", "redes"), namespace="redes")),
    # Historico
    path("historico/", include(("historico.urls", "historico"), namespace="historico")),
    #Users
    path("users/", include(("users.urls", "users"), namespace="users")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




def handler403(request, exception=None):
    return render(request, "403.html", status=403)

handler403 = handler403