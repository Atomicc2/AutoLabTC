from fastapi import FastAPI

from api.rotas.operacoes_rotas import router as operacoes_router

app = FastAPI(title="AutoLabTC")

app.include_router(operacoes_router, tags=["operacoes"])

@app.get("/")
def home():
    return {"message": "Olá, mundo!"}