from app.infra.repositories.fake_funcionario_repository import FakeFuncionarioRepository
from app.domain.entities.funcionario import NovoFuncionario

def novo_funcionario(email="a@a.com", nome="Teste"): 
    return NovoFuncionario(
        senha="123", confirmacaoSenha="123", email=email,
        nome=nome, idade=30, funcao="Reparador", cpf="11111111111"
    )

def test_salvar_e_listar_funcionario():
    repo = FakeFuncionarioRepository()
    repo.resetar()
    repo.salvar(novo_funcionario())
    funcionarios = repo.listar_todos()
    assert len(funcionarios) == 1
    assert funcionarios[0].email == "a@a.com"

def test_buscar_por_id_e_email():
    repo = FakeFuncionarioRepository()
    repo.resetar()
    f = repo.salvar(novo_funcionario(email="b@b.com"))
    assert repo.buscar_por_id(f.matricula) == f
    assert repo.buscar_por_email("b@b.com") == f
    assert repo.buscar_por_id(99999) is None
    assert repo.buscar_por_email("naoexiste@x.com") is None

def test_atualizar_funcionario():
    repo = FakeFuncionarioRepository()
    repo.resetar()
    f = repo.salvar(novo_funcionario(email="c@c.com", nome="Antigo"))
    atualizado = repo.atualizar(f.matricula, novo_funcionario(email="c@c.com", nome="Novo"))
    assert atualizado.nome == "Novo"

def test_remover_funcionario():
    repo = FakeFuncionarioRepository()
    repo.resetar()
    f = repo.salvar(novo_funcionario(email="d@d.com"))
    assert repo.remover(f.matricula) is True
    assert repo.remover(99999) is False
    assert repo.listar_todos() == []

def test_resetar_funcionario():
    repo = FakeFuncionarioRepository()
    repo.salvar(novo_funcionario())
    repo.resetar()
    assert repo.listar_todos() == [] 