# web/execucao/api_views.py
from __future__ import annotations

from cadastro.models import Loja
from django.http import Http404, HttpRequest, JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def loja_lookup_por_codigo(request: HttpRequest) -> JsonResponse:
    """
    Lookup de Loja por código (Java).

    Entrada (querystring):
      - codigo: obrigatório, numérico

    Saída (200):
      - {id, codigo, nome}

    Erros:
      - 400: codigo ausente ou inválido
      - 404: loja não encontrada
    """
    codigo = (request.GET.get("codigo") or "").strip()

    if not codigo or not codigo.isdigit():
        return JsonResponse(
            {"detail": "codigo must be a numeric string"},
            status=400,
        )

    try:
        loja = Loja.objects.only("id", "codigo", "nome").get(codigo=codigo)
    except Loja.DoesNotExist as exc:
        raise Http404("Loja not found") from exc

    return JsonResponse(
        {"id": loja.id, "codigo": loja.codigo, "nome": loja.nome},
        status=200,
    )
