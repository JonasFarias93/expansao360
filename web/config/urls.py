# web/config/urls.py


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Operation
    path("execucao/", include(("execucao.urls", "execucao"), namespace="execucao")),
    # Registry (cadastro)
    path("cadastro/", include(("cadastro.urls", "cadastro"), namespace="cadastro")),
    # IAM (se você expõe alguma tela/admin extra; senão pode remover)
    # path("iam/", include(("iam.urls", "iam"), namespace="iam")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
