from fastapi import APIRouter, status, Depends
from app.dependencies.funcionario import get_cadastrar_funcionario_uc
from app.use_cases.cadastrar_funcionario import CadastrarFuncionario
from app.domain.entities.funcionario import NovoFuncionario, Funcionario
from app.domain.entities.erro import Erro

router = APIRouter()

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
