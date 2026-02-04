from django.urls import reverse
import pytest

from cadastro.models import Categoria, Equipamento, TipoEquipamento


@pytest.mark.django_db
def test_ajax_tipos_por_equipamento_retorna_json(client):
    cat = Categoria.objects.create(nome="Monitores")

    eq = Equipamento.objects.create(
        nome="micro",
        codigo="11740-000",
        categoria=cat,
    )

    t1 = TipoEquipamento.objects.create(categoria=cat, nome="LCD", codigo="LCD", disponivel=True)
    t2 = TipoEquipamento.objects.create(
        categoria=cat, nome="Touch", codigo="TOUCH", disponivel=True
    )

    url = reverse("registry:ajax_tipos_por_equipamento")

    resp = client.get(
        url,
        {"equipamento_id": eq.id},
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )

    assert resp.status_code == 200
    data = resp.json()

    assert {d["id"] for d in data} == {t1.id, t2.id}
    assert {d["nome"] for d in data} == {"LCD", "Touch"}
