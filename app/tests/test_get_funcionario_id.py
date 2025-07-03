import pytest
from app.use_cases.buscar_funcionario_por_id import BuscarFuncionarioPorId
from app.infra.repositories.fake_funcionario_repository import fake_funcionario_repository
from app.domain.entities.funcionario import NovoFuncionario
from fastapi import HTTPException

@pytest.fixture(autouse=True)
def reset_repo():
    fake_funcionario_repository.resetar()

def test_get_funcionario_por_id_sucesso():
    novo_funcionario = NovoFuncionario(
        nome="Joana Silva",
        idade=40,
        funcao="Técnico",
        cpf="22222222222",
        email="joana@empresa.com",
        senha="senha456"
    )
    funcionario = fake_funcionario_repository.salvar(novo_funcionario)
    use_case = BuscarFuncionarioPorId(fake_funcionario_repository)

    resultado = use_case.execute(funcionario.matricula)

    assert resultado.email == "joana@empresa.com"
    assert resultado.nome == "Joana Silva"
    assert resultado.cpf == "22222222222"

def test_get_funcionario_por_id_inexistente():
    use_case = BuscarFuncionarioPorId(fake_funcionario_repository)
    matricula_inexistente = 9999

    with pytest.raises(HTTPException) as exc:
        use_case.execute(matricula_inexistente)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Funcionário não encontrado"
