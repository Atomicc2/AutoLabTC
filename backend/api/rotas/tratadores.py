"""Converte exceções de domínio em respostas HTTP da API."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.nucleo.excecoes import (
    ErroGeracaoPdf,
    ErroJFFInvalido,
    OperacaoInvalidaError,
)


def _resposta(status_code: int, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"detail": str(exc)})


async def tratar_jff_invalido(request: Request, exc: ErroJFFInvalido) -> JSONResponse:
    return _resposta(422, exc)


async def tratar_operacao_invalida(
    request: Request, exc: OperacaoInvalidaError
) -> JSONResponse:
    return _resposta(422, exc)


async def tratar_erro_geracao_pdf(
    request: Request, exc: ErroGeracaoPdf
) -> JSONResponse:
    return _resposta(503, exc)


def registrar_tratadores(app: FastAPI) -> None:
    """Registra os tratadores globais de exceção no aplicativo."""
    app.add_exception_handler(ErroJFFInvalido, tratar_jff_invalido)
    app.add_exception_handler(OperacaoInvalidaError, tratar_operacao_invalida)
    app.add_exception_handler(ErroGeracaoPdf, tratar_erro_geracao_pdf)
