import pytest
from app.use_cases.cadastrar_funcionario import CadastrarFuncionario
from app.infra.repositories.fake_funcionario_repository import fake_funcionario_repository
from app.domain.entities.funcionario import NovoFuncionario
from fastapi import HTTPException

@pytest.fixture(autouse=True)
def reset_repo():
    fake_funcionario_repository.resetar()

def test_post_funcionario_sucesso():
    use_case = CadastrarFuncionario(fake_funcionario_repository)
    dados = NovoFuncionario(
        nome="Carlos Souza",
        idade=35,
        funcao="Gerente",
        cpf="12345678900",
        email="carlos@empresa.com",
        senha="123456"
    )
    funcionario = use_case.execute(dados)
    assert funcionario.nome == "Carlos Souza"
    assert hasattr(funcionario, "matricula")

def test_post_funcionario_falha_email_duplicado():
    use_case = CadastrarFuncionario(fake_funcionario_repository)
    dados = NovoFuncionario(
        nome="João Silva",
        idade=30,
        funcao="Atendente",
        cpf="11111111111",
        email="joao@empresa.com",
        senha="123456"
    )
    use_case.execute(dados)
    with pytest.raises(HTTPException) as exc:
        use_case.execute(dados)
    assert exc.value.status_code == 422
    assert exc.value.detail == "E-mail já cadastrado"
