# web/chamados/views/__init__.py
from __future__ import annotations

from .abertura import ChamadoCreateView, subprojetos_por_projeto
from .evidencias import ChamadoAdicionarEvidenciaView, EvidenciaRemoverView
from .execucao import ChamadoExecucaoView, ChamadoSalvarExecucaoView
from .fila import ChamadoFilaView
from .historico import HistoricoView
from .itens import (
    ChamadoAtualizarItensView,
    ItemMarcarConfiguradoView,
    ItemSetStatusConfiguracaoView,
)
from .setup import ChamadoSalvarDadosFiscaisView, ChamadoSetupView
from .workflow import (
    ChamadoConfirmarColetaView,
    ChamadoFinalizarView,
    ChamadoInformarContabilView,
    ChamadoInformarNFSaidaView,
)

__all__ = [
    "ChamadoFilaView",
    "HistoricoView",
    "ChamadoCreateView",
    "ChamadoSetupView",
    "ChamadoExecucaoView",
    "ChamadoAtualizarItensView",
    "ItemSetStatusConfiguracaoView",
    "ChamadoInformarContabilView",
    "ChamadoInformarNFSaidaView",
    "ChamadoConfirmarColetaView",
    "ChamadoFinalizarView",
    "ChamadoSalvarDadosFiscaisView",
    "ChamadoSalvarExecucaoView",
    "ItemMarcarConfiguradoView",
    "ChamadoAdicionarEvidenciaView",
    "EvidenciaRemoverView",
    "subprojetos_por_projeto",
]
