import pytest
from app.use_cases.listar_funcionarios import ListarFuncionarios
from app.infra.repositories.fake_funcionario_repository import fake_funcionario_repository
from app.domain.entities.funcionario import NovoFuncionario

@pytest.fixture(autouse=True)
def reset_repo():
    fake_funcionario_repository.resetar()

def test_listar_funcionarios_vazio():
    use_case = ListarFuncionarios(fake_funcionario_repository)
    resultado = use_case.execute()
    assert isinstance(resultado, list)
    assert len(resultado) == 0

def test_listar_funcionarios_apos_cadastro():
    novo_funcionario = NovoFuncionario(
        nome="Ana Pereira",
        idade=28,
        funcao="Atendente",
        cpf="33333333333",
        email="ana@empresa.com",
        senha="senha456"
    )
    fake_funcionario_repository.salvar(novo_funcionario)
    use_case = ListarFuncionarios(fake_funcionario_repository)
    resultado = use_case.execute()
    assert isinstance(resultado, list)
    assert any(f.email == "ana@empresa.com" for f in resultado)
