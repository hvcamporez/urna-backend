from fastapi import APIRouter

from database import db

router = APIRouter(prefix="/apuracao", tags=["Apuração"])


@router.get("/resultado/{cargo_id}")
def resultado_cargo(cargo_id: str):
    """Totaliza os votos de um cargo (boletim de urna consolidado)."""
    votos = (
        db().table("votos")
        .select("candidato_id")
        .eq("cargo_id", cargo_id)
        .execute()
        .data
    )
    candidatos = (
        db().table("candidatos")
        .select("id, nome, numero")
        .eq("cargo_id", cargo_id)
        .execute()
        .data
    )

    contagem = {}
    brancos = 0
    for v in votos:
        candidato_id = v["candidato_id"]
        if candidato_id is None:
            brancos += 1
        else:
            contagem[candidato_id] = contagem.get(candidato_id, 0) + 1

    resultado = [
        {
            "candidato": c["nome"],
            "numero": c["numero"],
            "votos": contagem.get(c["id"], 0),
        }
        for c in candidatos
    ]
    resultado.sort(key=lambda item: item["votos"], reverse=True)

    return {
        "resultado": resultado,
        "brancos": brancos,
        "total_votos": len(votos),
    }
