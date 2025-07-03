import pytest
from app.use_cases.atualizar_funcionario import AtualizarFuncionario
from app.use_cases.cadastrar_funcionario import CadastrarFuncionario
from app.infra.repositories.fake_funcionario_repository import fake_funcionario_repository
from app.domain.entities.funcionario import NovoFuncionario
from fastapi import HTTPException

@pytest.fixture(autouse=True)
def reset_repo():
    fake_funcionario_repository.resetar()

def test_editar_funcionario_com_sucesso():
    use_case_cadastro = CadastrarFuncionario(fake_funcionario_repository)
    dados = NovoFuncionario(
        nome="Amanda Rocha",
        idade=28,
        funcao="Analista",
        cpf="55555555555",
        email="amanda@empresa.com",
        senha="123456"
    )
    funcionario = use_case_cadastro.execute(dados)
    use_case_edicao = AtualizarFuncionario(fake_funcionario_repository)
    update_payload = NovoFuncionario(
        nome="Amanda Silva",
        idade=29,
        funcao="Coordenadora",
        cpf="55555555555",
        email="amanda.silva@empresa.com",
        senha="novaSenha"
    )
    resultado = use_case_edicao.execute(funcionario.matricula, update_payload)
    assert resultado.nome == "Amanda Silva"
    assert resultado.email == "amanda.silva@empresa.com"

def test_editar_funcionario_inexistente():
    use_case_edicao = AtualizarFuncionario(fake_funcionario_repository)
    update_payload = NovoFuncionario(
        nome="Qualquer",
        idade=40,
        funcao="Zelador",
        cpf="00000000000",
        email="naoexiste@teste.com",
        senha="invalido"
    )
    with pytest.raises(HTTPException) as exc:
        use_case_edicao.execute(999, update_payload)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Funcionário não encontrado"
