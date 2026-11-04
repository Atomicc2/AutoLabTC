from typing import Annotated, Literal

from fastapi import APIRouter, File, HTTPException, Query, Response, UploadFile

from api.nucleo.excecoes import ErroGeracaoPdf
from api.servicos.operacoes_servico import complemento, complemento_pdf

router = APIRouter(prefix="/operacoes", tags=["Operações"])


@router.post("/complemento")
async def realizar_complemento(
    arquivo: Annotated[UploadFile, File()],
    formato: Annotated[Literal["jff", "pdf"], Query()] = "jff",
):
    jff = (await arquivo.read()).decode("utf-8")

    if formato == "pdf":
        try:
            pdf = complemento_pdf(jff)
        except ErroGeracaoPdf as erro:
            raise HTTPException(status_code=503, detail=str(erro)) from erro

        return Response(
            content=pdf,
            media_type="application/pdf",
            headers={"Content-Disposition": 'attachment; filename="complemento.pdf"'},
        )

    return Response(content=complemento(jff), media_type="application/xml")
