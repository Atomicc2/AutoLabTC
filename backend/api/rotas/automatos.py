from fastapi import APIRouter

from api.servicos.automato_service import AutomatoService

router = APIRouter()


@router.get("/")
def listar_automatos():
    servico = AutomatoService()
    return servico.listar()
