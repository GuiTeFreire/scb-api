from fastapi import APIRouter, status
from app.models.ciclista import RequisicaoCadastroCiclista, CiclistaResposta
from app.models.erro import Erro
from app.services.ciclista import cadastrar_ciclista

router = APIRouter()

@router.post(
    "/ciclista",
    response_model=CiclistaResposta,
    summary="Cadastrar um ciclista",
    status_code=status.HTTP_201_CREATED,
    tags=["Aluguel"],
    responses={
        422: {"description": "Dados Inválidos", "model": list[Erro]},
        404: {"description": "Requisição mal formada", "model": Erro}
    }
)
def post_ciclista(payload: RequisicaoCadastroCiclista):
    return cadastrar_ciclista(payload)