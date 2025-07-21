from fastapi import APIRouter, status

from app.dependencies.reset import get_restaurar_banco_uc

router = APIRouter()

@router.get(
    "/restaurarBanco",
    summary="Restaurar dados iniciais do banco de dados do microsserviço",
    status_code=status.HTTP_200_OK,
    tags=["Aluguel"],
    responses={
        200: {"description": "Banco restaurado"},
    }
)
def restaurar_banco():
    use_case = get_restaurar_banco_uc()
    use_case.execute()
    return {"mensagem": "Banco restaurado com sucesso"}

@router.get(
    "/restaurarDados",
    summary="Restaura todos os dados da aplicação para o estado inicial (para testes)",
    status_code=status.HTTP_200_OK,
    tags=["Aluguel"],
    responses={
        200: {"description": "Dados restaurados"},
    }
)
def restaurar_dados():
    use_case = get_restaurar_banco_uc()
    use_case.restaurar_dados_iniciais()
    return {"mensagem": "Dados restaurados com sucesso"}