from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from execucao.models import NF_SAIDA_ONLY_DIGITS_ERROR, Chamado


# =========================
# Tipos estruturados (UI / API / testes)
# =========================
@dataclass(frozen=True)
class Pendencia:
    code: str  # ex: "COLETA_NAO_CONFIRMADA"
    message: str  # ex: "Confirme a coleta antes de finalizar."
    field: str | None = None  # ex: "nf_saida_numero"


@dataclass(frozen=True)
class PendenciaItem:
    item_id: int
    equipamento: str
    code: str  # ex: "ITEM_FALTA_SERIAL"
    message: str
    field: str | None = None


@dataclass(frozen=True)
class ValidacaoFinalizacao:
    fiscais: list[Pendencia]
    coleta: list[Pendencia]
    itens: list[PendenciaItem]

    @property
    def ok(self) -> bool:
        return not (self.fiscais or self.coleta or self.itens)


# =========================
# Regras MVP (PR6)
# =========================
def validar_finalizacao(chamado: Chamado) -> ValidacaoFinalizacao:
    """
    Valida se um chamado está apto a ser FINALIZADO.

    Retorna estrutura com pendências por categoria:
    - fiscais: contábil / NF (quando aplicável)
    - coleta: confirmação obrigatória (MVP)
    - itens: por item, apontando o que falta (MVP)

    Este service não muda estado. Apenas valida.
    """

    fiscais: list[Pendencia] = []
    coleta: list[Pendencia] = []
    itens: list[PendenciaItem] = []

    # -------------
    # Coleta (MVP: obrigatório)
    # -------------
    if getattr(chamado, "coleta_confirmada_em", None) is None:
        coleta.append(
            Pendencia(
                code="COLETA_NAO_CONFIRMADA",
                message="Confirme a coleta antes de finalizar.",
                field="coleta_confirmada",
            )
        )

    # -------------
    # Fiscais (quando aplicável)
    # MVP sugerido:
    # - Se fluxo exige NF: NF não vazia e somente dígitos
    # - Contábil obrigatório quando exigir NF (entrada do fluxo fiscal)
    # Obs: se isso mudar depois, fica centralizado aqui.
    # -------------
    exige_nf = _exige_nf_saida(chamado)

    if exige_nf:
        cont = (getattr(chamado, "contabilidade_numero", "") or "").strip()
        nf = (getattr(chamado, "nf_saida_numero", "") or "").strip()

        if not cont:
            fiscais.append(
                Pendencia(
                    code="FISCAL_FALTA_CONTABIL",
                    message="Informe o chamado contábil antes de finalizar.",
                    field="contabilidade_numero",
                )
            )

        if not nf:
            fiscais.append(
                Pendencia(
                    code="FISCAL_FALTA_NF_SAIDA",
                    message="Informe a NF de saída antes de finalizar.",
                    field="nf_saida_numero",
                )
            )
        else:
            # mantém alinhado com a regra já usada no form:
            nf_digits = "".join(nf.split())
            if not nf_digits.isdigit():
                fiscais.append(
                    Pendencia(
                        code="FISCAL_NF_SAIDA_INVALIDA",
                        message=NF_SAIDA_ONLY_DIGITS_ERROR,
                        field="nf_saida_numero",
                    )
                )

    # -------------
    # Itens
    # MVP:
    # - configuráveis: se deve_configurar=True, exige configurado_em (quando existir)
    # - rastreáveis: se tiver campos (ativo/serial), valida o que existir
    #   (sem “inventar” regra; valida apenas se o item expõe o campo)
    # -------------
    for item in _iter_itens(chamado):
        pendencias_item = _validar_item_mvp(item)
        itens.extend(pendencias_item)

    return ValidacaoFinalizacao(
        fiscais=fiscais,
        coleta=coleta,
        itens=itens,
    )


# =========================
# Helpers (internos)
# =========================
def _exige_nf_saida(chamado: Chamado) -> bool:
    # MVP: ENVIO exige NF.
    # Se no seu domínio existir chamado.exige_nf_saida() ou algo assim,
    # troque aqui (centralizado).
    if getattr(chamado, "tipo", None) == Chamado.Tipo.ENVIO:
        return True
    # fallback: se existir método de domínio
    fn = getattr(chamado, "exige_nf_saida", None)
    if callable(fn):
        return bool(fn())
    return False


def _iter_itens(chamado: Chamado) -> Iterable[object]:
    # garante itens gerados
    gen = getattr(chamado, "gerar_itens_de_instalacao", None)
    if callable(gen):
        gen()

    rel = getattr(chamado, "itens", None)
    if rel is None:
        return []

    qs = getattr(rel, "select_related", None)
    if callable(qs):
        return rel.select_related("equipamento").all().order_by("id")

    # fallback (se já vier lista)
    return list(rel)


def _label_equipamento(item: object) -> str:
    eq = getattr(item, "equipamento", None)
    if eq is None:
        return "—"
    # preferir campos comuns
    nome = getattr(eq, "nome", None)
    if nome:
        return str(nome)
    codigo = getattr(eq, "codigo", None)
    if codigo:
        return str(codigo)
    return str(eq)


def _validar_item_mvp(item: object) -> list[PendenciaItem]:
    pend: list[PendenciaItem] = []

    item_id = int(getattr(item, "id", 0) or 0)
    equipamento = _label_equipamento(item)

    # configuráveis
    deve_configurar = bool(getattr(item, "deve_configurar", False))
    if deve_configurar:
        # preferir configurado_em se existir (contrato do PR6)
        if hasattr(item, "configurado_em"):
            if getattr(item, "configurado_em", None) is None:
                pend.append(
                    PendenciaItem(
                        item_id=item_id,
                        equipamento=equipamento,
                        code="ITEM_NAO_CONFIGURADO",
                        message="Item exige configuração, mas não está configurado.",
                        field="configurado_em",
                    )
                )
        else:
            # fallback: se existir status_configuracao, valida configurado
            status = getattr(item, "status_configuracao", None)
            if status is None:
                # sem regra disponível => não inventa (MVP)
                pass

    # rastreáveis (valida apenas se o campo existir no item)
    if hasattr(item, "ativo"):
        ativo = (getattr(item, "ativo", "") or "").strip()
        if not ativo:
            pend.append(
                PendenciaItem(
                    item_id=item_id,
                    equipamento=equipamento,
                    code="ITEM_FALTA_ATIVO",
                    message="Item rastreável exige ATIVO preenchido.",
                    field="ativo",
                )
            )

    if hasattr(item, "serial"):
        serial = (getattr(item, "serial", "") or "").strip()
        if not serial:
            pend.append(
                PendenciaItem(
                    item_id=item_id,
                    equipamento=equipamento,
                    code="ITEM_FALTA_SERIAL",
                    message="Item rastreável exige SERIAL preenchido.",
                    field="serial",
                )
            )

    return pend
