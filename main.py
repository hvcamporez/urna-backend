from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import apuracao, auth, mesario, votacao

app = FastAPI(title="API - Simulação de Urna Eletrônica")

# Em produção, troque "*" pelo domínio publicado do seu app no Lovable
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(votacao.router)
app.include_router(mesario.router)
app.include_router(apuracao.router)


@app.get("/")
def root():
    return {"status": "API da urna eletrônica simulada no ar"}
