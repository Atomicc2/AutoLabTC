from fastapi import APIRouter

from api.servicos.operacoes_service import AutomatoService

router = APIRouter()


@router.get("/")
def listar_automatos():
    servico = AutomatoService()
    return servico.listar()
