from fastapi import APIRouter, UploadFile, File, Response
from api.servicos.operacoes_servico import complemento

router = APIRouter(prefix="/operacoes", tags=["Operações"])

@router.post("/complemento")
async def realizar_complemento(arquivo: UploadFile = File(...)):
    jff = (await arquivo.read()).decode("utf-8")
    resultado = complemento(jff)

    return Response(
        content=resultado,
        media_type="application/xml"
    )