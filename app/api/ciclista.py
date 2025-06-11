from fastapi import APIRouter, status, Path, HTTPException
from app.models.ciclista import RequisicaoCadastroCiclista, CiclistaResposta
from app.models.erro import Erro
from app.services.ciclista import cadastrar_ciclista, buscar_ciclista_por_id, atualizar_ciclista, email_existe
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
def get_ciclista(id_ciclista: int = Path(..., gt=0, alias="idCiclista")):
    return buscar_ciclista_por_id(id_ciclista)

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
def put_ciclista(payload: EdicaoCiclista, id_ciclista: int = Path(..., alias="idCiclista")):
    return atualizar_ciclista(id_ciclista, payload)

@router.get(
    "/ciclista/existeEmail/{email}",
    summary="Verifica se o e-mail já foi utilizado por algum ciclista.",
    tags=["Aluguel"],
    response_model=bool,
    responses={
        200: {"description": "True caso exista o email e false caso contrario."},
        422: {"description": "Dados Inválidos", "model": list[Erro]},
        400: {"description": "Email não enviado como parâmetro", "model": Erro}
    }
)
def get_email_existe(email: str = Path(..., title="Email do ciclista")):
  return email_existe(email)