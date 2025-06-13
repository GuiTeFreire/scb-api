from fastapi import APIRouter, status, Depends, Path
from app.dependencies.funcionario import get_cadastrar_funcionario_uc
from app.use_cases.cadastrar_funcionario import CadastrarFuncionario
from app.domain.entities.funcionario import NovoFuncionario, Funcionario
from app.domain.entities.erro import Erro
from app.dependencies.funcionario import get_listar_funcionarios_uc
from app.use_cases.listar_funcionarios import ListarFuncionarios
from typing import List
from app.dependencies.funcionario import get_buscar_funcionario_uc
from app.use_cases.buscar_funcionario_por_id import BuscarFuncionarioPorId
from app.dependencies.funcionario import get_atualizar_funcionario_uc

router = APIRouter()

@router.get(
    "/funcionario",
    response_model=List[Funcionario],
    summary="recupera funcionários cadastrados",
    status_code=status.HTTP_200_OK,
    tags=["Aluguel"],
    responses={
        200: {"description": "200 OK"},
    }
)
def listar_funcionarios(
    use_case: ListarFuncionarios = Depends(get_listar_funcionarios_uc)
):
    return use_case.execute()

@router.post(
    "/funcionario",
    response_model=Funcionario,
    summary="Cadastrar funcionário",
    status_code=status.HTTP_200_OK,
    tags=["Aluguel"],
    responses={
        200: {"description": "Dados cadastrados"},
        422: {"description": "Dados Inválidos", "model": list[Erro]},
    }
)
def post_funcionario(
    payload: NovoFuncionario,
    uc: CadastrarFuncionario = Depends(get_cadastrar_funcionario_uc)
):
    return uc.execute(payload)

@router.get(
    "/funcionario/{idFuncionario}",
    response_model=Funcionario,
    summary="Recupera funcionário",
    tags=["Aluguel"],
    responses={
        200: {"description": "Dados recuperados"},
        422: {"description": "Dados Inválidos", "model": list[Erro]},
        404: {"description": "Não encontrado", "model": Erro}
    }
)
def get_funcionario_por_id(
    id_funcionario: int = Path(..., gt=0, alias="idFuncionario"),
    uc: BuscarFuncionarioPorId = Depends(get_buscar_funcionario_uc)
):
    return uc.execute(id_funcionario)

@router.put(
    "/funcionario/{idFuncionario}",
    summary="Editar funcionário",
    tags=["Aluguel"],
    response_model=Funcionario,
    responses={
        200: {"description": "Dados atualizados"},
        422: {"description": "Dados Inválidos", "model": list[Erro]},
        404: {"description": "Não encontrado", "model": Erro},
    }
)
def put_funcionario(
    id_funcionario: int = Path(..., gt=0, alias="idFuncionario"),
    payload: NovoFuncionario = ...
):
    use_case = get_atualizar_funcionario_uc()
    return use_case.execute(id_funcionario, payload)