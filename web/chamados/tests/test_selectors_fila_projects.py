from __future__ import annotations

from chamados.models import Chamado
from chamados.selectors.fila import fila_base_queryset, fila_projects

from ._base import ChamadoBaseTestCase


class TestFilaSelectorProjects(ChamadoBaseTestCase):
    def _mk_projeto(self, *, codigo: str, nome: str) -> object:
        return self.projeto.__class__.objects.create(codigo=codigo, nome=nome)

    def _mk_subprojeto(self, *, projeto, codigo: str, nome: str) -> object:
        return self.sub.__class__.objects.create(
            projeto=projeto, codigo=codigo, nome=nome
        )

    def _mk_chamado(self, *, projeto, subprojeto, protocolo: str) -> Chamado:
        # prioridade/status não importam para projects, mas o selector usa base_qs (fila),
        # então o status tem que ser um status da fila.
        return Chamado.objects.create(
            loja=self.loja,
            projeto=projeto,
            subprojeto=subprojeto,
            kit=self.kit,
            tipo=Chamado.Tipo.ENVIO,
            status=Chamado.Status.ABERTO,
            protocolo=protocolo,
        )

    def test_dado_chamados_em_dois_projetos_quando_build_projects_entao_ordena_por_count_e_marca_active(
        self,
    ) -> None:
        # Arrange: projeto A (2 chamados), projeto B (1 chamado)
        projeto_a = self._mk_projeto(codigo="P2", nome="Projeto 2")
        sub_a = self._mk_subprojeto(projeto=projeto_a, codigo="S2", nome="Sub 2")

        projeto_b = self._mk_projeto(codigo="P3", nome="Projeto 3")
        sub_b = self._mk_subprojeto(projeto=projeto_b, codigo="S3", nome="Sub 3")

        self._mk_chamado(projeto=projeto_a, subprojeto=sub_a, protocolo="PX-1")
        self._mk_chamado(projeto=projeto_a, subprojeto=sub_a, protocolo="PX-2")
        self._mk_chamado(projeto=projeto_b, subprojeto=sub_b, protocolo="PY-1")

        base_qs = fila_base_queryset()

        calls: list[int] = []

        def url_builder(pid: int) -> str:
            calls.append(pid)
            return f"/fila?projeto={pid}"

        # Act
        projects = fila_projects(
            base_qs,
            projeto_selected=projeto_b.id,
            url_builder=url_builder,
        )

        # Assert: ordenado por count desc => A primeiro (2), depois B (1)
        assert [p["id"] for p in projects] == [projeto_a.id, projeto_b.id]
        assert [p["count"] for p in projects] == [2, 1]

        # Assert: active conforme selected
        assert projects[0]["active"] is False
        assert projects[1]["active"] is True

        # Assert: url_builder chamado com os pids retornados
        assert calls == [projeto_a.id, projeto_b.id]
        assert projects[0]["url"] == f"/fila?projeto={projeto_a.id}"
        assert projects[1]["url"] == f"/fila?projeto={projeto_b.id}"
