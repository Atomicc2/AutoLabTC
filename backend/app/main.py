import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.erros import ErroDeDominio
from backend.app.rotas.operacoes import roteador as roteador_operacoes

app = FastAPI(title="AutoLab-TC")

origens = os.getenv("FRONTEND_ORIGINS", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origem.strip() for origem in origens.split(",") if origem.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ErroDeDominio)
async def tratar_erro_de_dominio(request: Request, erro: ErroDeDominio):
    return JSONResponse(status_code=erro.status, content={"detail": erro.mensagem})


app.include_router(roteador_operacoes)


@app.get("/")
async def root():
    return {"message": "Hello World"}
