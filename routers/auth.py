from fastapi import APIRouter, HTTPException

from database import db
from schemas import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    """
    Identifica o eleitor pela matrícula (simulação — sem senha,
    já que é um exercício didático dentro da escola).
    """
    result = (
        db().table("eleitores")
        .select("id, nome, turma_id")
        .eq("matricula", payload.matricula)
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Eleitor não encontrado")

    eleitor = result.data[0]
    return LoginResponse(
        eleitor_id=eleitor["id"],
        nome=eleitor["nome"],
        turma_id=eleitor["turma_id"],
    )
