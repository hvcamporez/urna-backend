from fastapi import APIRouter, HTTPException

from database import db
from schemas import VotoRequest

router = APIRouter(prefix="/votacao", tags=["Votação"])


@router.get("/candidatos/{cargo_id}")
def listar_candidatos(cargo_id: str):
    """Lista os candidatos de um cargo, para exibir na tela de voto."""
    result = (
        db().table("candidatos")
        .select("id, numero, nome, nome_urna, foto_url")
        .eq("cargo_id", cargo_id)
        .order("numero")
        .execute()
    )
    return result.data


@router.get("/sessao/{turma_id}")
def status_sessao(turma_id: str):
    """Consulta se a sessão de votação da turma está aberta ou fechada."""
    result = (
        db().table("sessao_votacao")
        .select("*")
        .eq("turma_id", turma_id)
        .order("data_inicio", desc=True)
        .limit(1)
        .execute()
    )
    if not result.data:
        return {"status": "inexistente"}
    return result.data[0]


@router.post("/votar")
def votar(payload: VotoRequest):
    """
    Registra o voto chamando a função 'registrar_voto' no Postgres,
    que grava o voto e o comprovante em uma única transação atômica,
    sem nunca vincular eleitor a candidato.
    """
    try:
        db().rpc(
            "registrar_voto",
            {
                "p_eleitor_id": payload.eleitor_id,
                "p_cargo_id": payload.cargo_id,
                "p_turma_id": payload.turma_id,
                "p_candidato_id": payload.candidato_id,
            },
        ).execute()
    except Exception as e:
        # Erros de negócio (sessão fechada, voto duplicado) vêm da
        # exceção lançada dentro da função SQL.
        raise HTTPException(status_code=400, detail=str(e))

    return {"mensagem": "Voto registrado com sucesso"}
