from __future__ import annotations

from execucao.models import Chamado

# Ordem de progressão (nunca regride)
_STATUS_ORDER = (
    "ABERTO",
    "EM_EXECUCAO",
    "AGUARDANDO_NF",
    "AGUARDANDO_COLETA",
    "FINALIZADO",
)


def _rank(status_value: str) -> int:
    try:
        return _STATUS_ORDER.index(status_value)
    except ValueError:
        # Status desconhecido: não arrisca mexer
        return -1


def _promote(current: str, target: str) -> str:
    rc = _rank(current)
    rt = _rank(target)
    if rc == -1 or rt == -1:
        return current
    return target if rt > rc else current


def recalcular_status(chamado: Chamado) -> Chamado.Status:
    """
    Recalcula status no gatilho 'Salvar' (fora Finalizar).
    - Idempotente
    - Nunca regride
    - Não mexe em EM_ABERTURA (contrato)
    """
    atual = str(chamado.status)

    if atual == "EM_ABERTURA":
        return chamado.status

    novo = atual

    # primeiro save após abertura => EM_EXECUCAO
    if atual == "ABERTO":
        novo = _promote(novo, "EM_EXECUCAO")


    #  NF Saída preenchida => AGUARDANDO_COLETA (maior precedência)
    if bool((chamado.nf_saida_numero or "").strip()):
        novo = _promote(novo, "AGUARDANDO_COLETA")

    #  Itens bipados + contábil preenchido => AGUARDANDO_NF
    contabil_ok = bool((chamado.contabilidade_numero or "").strip())
    if contabil_ok and chamado.pode_liberar_nf():
        novo = _promote(novo, "AGUARDANDO_NF")

    return Chamado.Status(novo)
