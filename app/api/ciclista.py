from fastapi import APIRouter, status, Depends, Path, Header
from app.domain.entities.erro import Erro
from app.domain.entities.ciclista import RequisicaoCadastroCiclista, CiclistaResposta, NovoCiclista
from app.infra.repositories.fake_ciclista_repository import FakeCiclistaRepository
from app.use_cases.cadastrar_ciclista import CadastrarCiclista
from app.domain.entities.ciclista import Ciclista
from app.use_cases.buscar_ciclista_por_id import BuscarCiclistaPorId
from app.use_cases.atualizar_ciclista import AtualizarCiclista
from app.domain.entities.ciclista import EdicaoCiclista
from app.use_cases.verificar_email_existente import VerificarEmailExistente
from app.use_cases.ativar_ciclista import AtivarCiclista
from app.dependencies.ciclista import (
    get_buscar_ciclista_use_case,
    get_atualizar_ciclista_use_case,
    get_cadastrar_ciclista_use_case,
    get_verificar_email_use_case,
    get_ativar_ciclista_uc
)

router = APIRouter()

repo = FakeCiclistaRepository()

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
def post_ciclista(
    payload: RequisicaoCadastroCiclista,
    use_case: CadastrarCiclista = Depends(get_cadastrar_ciclista_use_case)
):
    ciclista = NovoCiclista(**payload.ciclista.model_dump())
    novo = Ciclista(**ciclista.model_dump(), id=0)
    return use_case.execute(novo)

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
def get_ciclista(
    id_ciclista: int = Path(..., alias="idCiclista"),
    use_case: BuscarCiclistaPorId = Depends(get_buscar_ciclista_use_case)
):
    return use_case.execute(id_ciclista)

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
@router.put("/ciclista/{idCiclista}")
def put_ciclista(
    payload: EdicaoCiclista,
    id_ciclista: int = Path(..., alias="idCiclista"),
    use_case: AtualizarCiclista = Depends(get_atualizar_ciclista_use_case)
):
    cic = use_case.execute(id_ciclista, payload)
    return CiclistaResposta(**cic.model_dump())

@router.post(
    "/ciclista/{idCiclista}/ativar",
    response_model=CiclistaResposta,
    summary="Ativar conta de ciclista",
    tags=["Aluguel"],
    responses={
        200: {"description": "Ciclista ativado"},
        404: {"description": "Não encontrado", "model": Erro},
        422: {"description": "Dados Inválidos", "model": list[Erro]},
    }
)
def ativar_ciclista(
    idCiclista: int,
    x_id_requisicao: int = Header(default=None, alias="x-id-requisicao"),
    uc: AtivarCiclista = Depends(get_ativar_ciclista_uc)
):
    return uc.execute(idCiclista)

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
def get_email_existe(
    email: str,
    use_case: BuscarCiclistaPorId = Depends(get_verificar_email_use_case)
):
    return use_case.execute(email)