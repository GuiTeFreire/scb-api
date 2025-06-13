from app.use_cases.cadastrar_funcionario import CadastrarFuncionario
from app.use_cases.listar_funcionarios import ListarFuncionarios
from app.infra.repositories.fake_funcionario_repository import FakeFuncionarioRepository

repo = FakeFuncionarioRepository()

def get_cadastrar_funcionario_uc():
    return CadastrarFuncionario(repo)

def get_listar_funcionarios_uc():
    return ListarFuncionarios(repo)