# web/config/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from iam.views import acesso_negado_403


def root_redirect(request):
    return redirect("execucao:fila")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", root_redirect),
    # Operation
    path("execucao/", include(("execucao.urls", "execucao"), namespace="execucao")),
    # Registry (cadastro)
    path("cadastro/", include(("cadastro.urls", "cadastro"), namespace="cadastro")),
    # IAM
    path("iam/", include(("iam.urls", "iam"), namespace="iam")),
    path("redes/", include(("redes.urls", "redes"), namespace="redes")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler403 = acesso_negado_403
