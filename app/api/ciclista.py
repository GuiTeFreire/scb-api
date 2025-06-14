from fastapi import APIRouter, status, Depends, Path, Header

from app.dependencies.ciclista import (
    get_buscar_ciclista_use_case,
    get_atualizar_ciclista_use_case,
    get_cadastrar_ciclista_use_case,
    get_verificar_email_use_case,
    get_ativar_ciclista_use_case,
    get_obter_cartao_use_case,
    get_atualizar_cartao_use_case
)

from app.domain.entities.ciclista import EdicaoCiclista, RequisicaoCadastroCiclista, CiclistaResposta, CartaoDeCredito, NovoCartaoDeCredito
from app.domain.entities.erro import Erro

from app.infra.repositories.fake_ciclista_repository import FakeCiclistaRepository

from app.use_cases.ativar_ciclista import AtivarCiclista
from app.use_cases.atualizar_cartao_de_credito import AtualizarCartaoDeCredito
from app.use_cases.atualizar_ciclista import AtualizarCiclista
from app.use_cases.buscar_ciclista_por_id import BuscarCiclistaPorId
from app.use_cases.cadastrar_ciclista import CadastrarCiclista
from app.use_cases.obter_cartao_de_credito import ObterCartaoDeCredito

router = APIRouter()

repo = FakeCiclistaRepository()

@router.post(
    "/ciclista",
    response_model=CiclistaResposta,
    summary="Cadastrar um ciclista",
    status_code=status.HTTP_201_CREATED,
    tags=["Aluguel"],
    responses={
        201: {"description": "Ciclista cadastrado"},
        404: {"description": "Requisição mal formada", "model": Erro},
        422: {"description": "Dados Inválidos", "model": list[Erro]}
    }
)
def post_ciclista(
    payload: RequisicaoCadastroCiclista,
    use_case: CadastrarCiclista = Depends(get_cadastrar_ciclista_use_case)
):
    return use_case.execute(payload)

@router.get(
    "/ciclista/{idCiclista}",
    response_model=CiclistaResposta,
    summary="Recupera dados de um ciclista",
    status_code=status.HTTP_200_OK,
    tags=["Aluguel"],
    responses={
        200: {"description": "Retorna ciclista solicitado"},
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
        404: {"description": "Não encontrado", "model": Erro},
        422: {"description": "Dados Inválidos", "model": list[Erro]}
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
    summary="Ativar cadastro do ciclista",
    tags=["Aluguel"],
    responses={
        200: {"description": "Ciclista ativado"},
        404: {"description": "Não encontrado", "model": Erro},
        422: {"description": "Dados Inválidos", "model": list[Erro]},
    }
)
def ativar_ciclista(
    id_ciclista: int = Path(..., alias="idCiclista"),
    x_id_requisicao: int = Header(default=None, alias="x-id-requisicao"),
    use_case: AtivarCiclista = Depends(get_ativar_ciclista_use_case)
):
    return use_case.execute(id_ciclista)

@router.get(
    "/ciclista/existeEmail/{email}",
    summary="Verifica se o e-mail já foi utilizado por algum ciclista.",
    tags=["Aluguel"],
    response_model=bool,
    responses={
        200: {"description": "True caso exista o email e false caso contrario."},
        400: {"description": "Email não enviado como parâmetro", "model": Erro},
        422: {"description": "Dados Inválidos", "model": list[Erro]}
    }
)
def get_email_existe(
    email: str,
    use_case: BuscarCiclistaPorId = Depends(get_verificar_email_use_case)
):
    return use_case.execute(email)

@router.get(
    "/cartaoDeCredito/{idCiclista}",
    response_model=CartaoDeCredito,
    summary="Obter dados do cartão de crédito do ciclista",
    tags=["Aluguel"],
    responses={
        200: {"description": "Dados do cartão"},
        404: {"description": "Não encontrado", "model": Erro},
        422: {"description": "Dados Inválidos", "model": list[Erro]}
    }
)
def get_cartao_de_credito(
    id_ciclista: int = Path(..., alias="idCiclista"),
    use_case: ObterCartaoDeCredito = Depends(get_obter_cartao_use_case)
):
    return use_case.execute(id_ciclista)

@router.put(
    "/cartaoDeCredito/{idCiclista}",
    response_model=CartaoDeCredito,
    summary="Atualizar cartão de crédito do ciclista",
    tags=["Aluguel"],
    responses={
        200: {"description": "Cartão atualizado"},
        404: {"description": "Não encontrado", "model": Erro},
        422: {"description": "Dados Inválidos", "model": Erro}
    }
)
def put_cartao_de_credito(
    id_ciclista: int = Path(..., alias="idCiclista"),
    payload: NovoCartaoDeCredito = ...,
    use_case: AtualizarCartaoDeCredito = Depends(get_atualizar_cartao_use_case)
):
    return use_case.execute(id_ciclista, payload)