from fastapi import APIRouter, status, Depends, Path, Header

from app.dependencies.aluguel import (
    get_verificar_permissao_aluguel_use_case, 
    get_realizar_aluguel_use_case, 
    get_buscar_bicicleta_alugada_use_case, 
    get_realizar_devolucao_use_case
)
from app.dependencies.ciclista import (
    get_buscar_ciclista_use_case,
    get_atualizar_ciclista_use_case,
    get_cadastrar_ciclista_use_case,
    get_verificar_email_use_case,
    get_ativar_ciclista_use_case,
    get_obter_cartao_use_case,
    get_atualizar_cartao_use_case
)

from app.domain.entities.aluguel import AluguelResponse, NovoAluguel
from app.domain.entities.bicicleta import Bicicleta
from app.domain.entities.ciclista import EdicaoCiclista, RequisicaoCadastroCiclista, CiclistaResposta, CartaoDeCredito, NovoCartaoDeCredito
from app.domain.entities.devolucao import NovoDevolucao, Devolucao
from app.domain.entities.erro import Erro

from app.infra.repositories.fake_ciclista_repository import FakeCiclistaRepository

from app.use_cases.ativar_ciclista import AtivarCiclista
from app.use_cases.atualizar_cartao_de_credito import AtualizarCartaoDeCredito
from app.use_cases.atualizar_ciclista import AtualizarCiclista
from app.use_cases.buscar_bicicleta_alugada import BuscarBicicletaAlugada
from app.use_cases.buscar_ciclista_por_id import BuscarCiclistaPorId
from app.use_cases.cadastrar_ciclista import CadastrarCiclista
from app.use_cases.obter_cartao_de_credito import ObterCartaoDeCredito
from app.use_cases.verificar_permissao_aluguel import VerificarPermissaoAluguel
from app.use_cases.realizar_aluguel import RealizarAluguel
from app.use_cases.realizar_devolucao import RealizarDevolucao

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
    "/ciclista/{idCiclista}/permiteAluguel",
    summary="Verifica se o ciclista pode alugar uma bicicleta, já que só pode alugar uma por vez.",
    tags=["Aluguel"],
    response_model=bool,
    responses={
        200: {"description": "true se puder alugar e false caso contrário"},
        404: {"description": "Não encontrado", "model": Erro},
        422: {"description": "Dados Inválidos", "model": list[Erro]}
    }
)
def get_permite_aluguel(
    id_ciclista: int = Path(..., alias="idCiclista"),
    use_case: VerificarPermissaoAluguel = Depends(get_verificar_permissao_aluguel_use_case)
):
    return use_case.execute(id_ciclista)

@router.get(
    "/ciclista/{idCiclista}/bicicletaAlugada",
    response_model=Bicicleta | None,
    summary="Obtém bicicleta alugada por um ciclista (ou vazio caso contrário)",
    tags=["Aluguel"],
    responses={
        200: {"description": "Retorna bicicleta caso o ciclista tenha alugado ou vazio caso contrário."},
        404: {"description": "Ciclista não encontrado", "model": Erro},
        422: {"description": "Dados Inválidos", "model": list[Erro]}
    }
)
def get_bicicleta_alugada(
    id_ciclista: int = Path(..., alias="idCiclista", description="UUID do ciclista"),
    use_case: BuscarBicicletaAlugada = Depends(get_buscar_bicicleta_alugada_use_case)
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
    summary="Alterar dados de cartão de crédito de um ciclista",
    tags=["Aluguel"],
    responses={
        200: {"description": "Dados atualizados"},
        404: {"description": "Não encontrado", "model": Erro},
        422: {"description": "Dados Inválidos", "model": list[Erro]}
    }
)
def put_cartao_de_credito(
    id_ciclista: int = Path(..., alias="idCiclista"),
    payload: NovoCartaoDeCredito = ...,
    use_case: AtualizarCartaoDeCredito = Depends(get_atualizar_cartao_use_case)
):
    return use_case.execute(id_ciclista, payload)

@router.post(
    "/aluguel",
    response_model=AluguelResponse,
    description="Realiza uma cobrança de um valor fixo e em caso de aprovada a mesma libera a tranca com a bicicleta escolhida pelo ciclista. A mesma também notifica o ciclista da retirada da bicicleta.",
    summary="Realizar aluguel",
    tags=["Aluguel"],
    responses={
        200: {"description": "Aluguel realizado"},
        422: {"description": "Dados Inválidos", "model": list[Erro]}
    }
)
def post_aluguel(
    payload: NovoAluguel,
    use_case: RealizarAluguel = Depends(get_realizar_aluguel_use_case)
):
    return use_case.execute(payload)

@router.post(
    "/devolucao",
    response_model=Devolucao,
    description="Ao se devolver a bicicleta deve-se alterar o estado da tranca, e calcular possíveis custos adicionais a ser pago pelo ciclista e recorre a fila de cobrança para realiza-lo, notificando o ciclista da devolução e da taxa extra paga.",
    summary="Realizar devolução, sendo invocado de maneira automática pelo hardware do totem ao encostar a bicicleta na tranca.",
    tags=["Aluguel"],
    responses={
        200: {"description": "Devolucao realizada"},
        422: {"description": "Dados Inválidos", "model": list[Erro]}
    }
)
def post_devolucao(
    payload: NovoDevolucao,
    use_case: RealizarDevolucao = Depends(get_realizar_devolucao_use_case)
):
    return use_case.execute(payload)