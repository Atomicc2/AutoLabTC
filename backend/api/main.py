from fastapi import FastAPI

from api.rotas.operacoes_rotas import router as operacoes_router
from api.rotas.tratadores import registrar_tratadores

app = FastAPI(title="AutoLabTC")
registrar_tratadores(app)

app.include_router(operacoes_router, tags=["operacoes"])


@app.get("/")
def home():
    return {"message": "Olá, mundo!"}
