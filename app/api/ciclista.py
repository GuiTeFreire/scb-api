from fastapi import APIRouter, status, Path
from app.models.ciclista import RequisicaoCadastroCiclista, CiclistaResposta
from app.models.erro import Erro
from app.services.ciclista import cadastrar_ciclista, buscar_ciclista_por_id, atualizar_ciclista
from app.models.ciclista import EdicaoCiclista

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

@router.get(
    "/ciclista/{idCiclista}",
    response_model=CiclistaResposta,
    summary="Recupera dados de um ciclista",
    status_code=status.HTTP_200_OK,
    tags=["Aluguel"],
    responses={
        404: {"description": "Requisição mal formada", "model": Erro},
        422: {"description": "Dados Inválidos", "model": list[Erro]},
    }
)
def get_ciclista(idCiclista: int = Path(..., gt=0)):
    return buscar_ciclista_por_id(idCiclista)

@router.put(
    "/ciclista/{idCiclista}",
    response_model=CiclistaResposta,
    summary="Alterar dados de um ciclista",
    tags=["Aluguel"],
    responses={
        200: {"description": "Dados atualizados"},
        422: {"description": "Dados Inválidos", "model": list[Erro]},
        404: {"description": "Não encontrado", "model": Erro}
    }
)
def put_ciclista(idCiclista: int, payload: EdicaoCiclista):
    return atualizar_ciclista(idCiclista, payload)