import pytest
from app.use_cases.remover_funcionario import RemoverFuncionario
from app.infra.repositories.fake_funcionario_repository import fake_funcionario_repository
from app.domain.entities.funcionario import NovoFuncionario
from fastapi import HTTPException

@pytest.fixture(autouse=True)
def reset_repo():
    fake_funcionario_repository.resetar()

def test_remover_funcionario_sucesso():
    dados = NovoFuncionario(
        nome="Henrique Lopes",
        idade=45,
        funcao="Supervisor",
        cpf="99988877766",
        email="henrique@empresa.com",
        senha="senha456"
    )
    funcionario = fake_funcionario_repository.salvar(dados)
    use_case = RemoverFuncionario(fake_funcionario_repository)

    resultado = use_case.execute(funcionario.matricula)

    assert resultado == {"mensagem": "Funcionário removido com sucesso"}
    assert fake_funcionario_repository.buscar_por_id(funcionario.matricula) is None

def test_remover_funcionario_inexistente():
    use_case = RemoverFuncionario(fake_funcionario_repository)
    matricula_inexistente = 9999

    with pytest.raises(HTTPException) as exc:
        use_case.execute(matricula_inexistente)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Funcionário não encontrado"