from datetime import datetime, timezone

from fastapi import APIRouter

from database import db
from schemas import SessaoRequest

router = APIRouter(prefix="/mesario", tags=["Mesário"])


@router.post("/sessao/abrir")
def abrir_sessao(payload: SessaoRequest):
    """Abre a sessão de votação de uma turma."""
    result = (
        db().table("sessao_votacao")
        .insert(
            {
                "turma_id": payload.turma_id,
                "status": "aberta",
                "data_inicio": datetime.now(timezone.utc).isoformat(),
            }
        )
        .execute()
    )
    return result.data[0]


@router.post("/sessao/fechar")
def fechar_sessao(payload: SessaoRequest):
    """Fecha a sessão de votação aberta de uma turma."""
    result = (
        db().table("sessao_votacao")
        .update(
            {
                "status": "fechada",
                "data_fim": datetime.now(timezone.utc).isoformat(),
            }
        )
        .eq("turma_id", payload.turma_id)
        .eq("status", "aberta")
        .execute()
    )
    return result.data
