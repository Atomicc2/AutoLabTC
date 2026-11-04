from typing import Annotated

from fastapi import APIRouter, File, Response, UploadFile

from api.servicos.operacoes_servico import complemento

router = APIRouter(prefix="/operacoes", tags=["Operações"])


@router.post("/complemento")
async def realizar_complemento(
    arquivo: Annotated[UploadFile, File()],
) -> Response:
    """Gera um .zip com o .jff do complemento e o relatório PDF das etapas."""
    jff = (await arquivo.read()).decode("utf-8")
    resposta = complemento(jff)

    return Response(
        content=resposta.compactar("complemento"),
        media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="complemento.zip"'},
    )
