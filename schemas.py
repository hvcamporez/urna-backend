from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    matricula: str


class LoginResponse(BaseModel):
    eleitor_id: str
    nome: str
    turma_id: str


class VotoRequest(BaseModel):
    eleitor_id: str
    cargo_id: str
    turma_id: str
    candidato_id: Optional[str] = None  # None = voto em branco


class SessaoRequest(BaseModel):
    turma_id: str
