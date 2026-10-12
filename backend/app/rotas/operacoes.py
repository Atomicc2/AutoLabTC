from fastapi import APIRouter, File, UploadFile
from fastapi.responses import Response

from backend.app.erros import ArquivoInvalidoError, OperacaoNaoEncontradaError
from backend.app.servicos.operacoes import OPERACOES
from backend.app.utilitarios.utilitario_jff import UtilitarioJff

TAMANHO_MAXIMO = 1_000_000

roteador = APIRouter(prefix="/operacoes", tags=["operacoes"])


@roteador.get("")
async def listar_operacoes():
    return list(OPERACOES.keys())


@roteador.post("/{nome}")
async def executar_operacao(nome: str, arquivo: UploadFile = File(...)):
    if nome not in OPERACOES:
        raise OperacaoNaoEncontradaError(f"A operação '{nome}' não existe.")

    if not arquivo.filename or not arquivo.filename.lower().endswith(".jff"):
        raise ArquivoInvalidoError("O arquivo enviado deve ter a extensão .jff.")

    conteudo = await arquivo.read()

    if len(conteudo) > TAMANHO_MAXIMO:
        raise ArquivoInvalidoError("O arquivo .jff excede o limite de 1 MB.")

    automato = UtilitarioJff.ler(conteudo)
    resultado = OPERACOES[nome](automato)
    bytes_saida = UtilitarioJff.escrever(resultado)

    nome_base = arquivo.filename.rsplit(".", 1)[0]
    nome_download = f"{nome_base}_{nome}.jff"

    return Response(
        content=bytes_saida,
        media_type="application/xml",
        headers={"Content-Disposition": f'attachment; filename="{nome_download}"'},
    )
