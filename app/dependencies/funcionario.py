from app.use_cases.cadastrar_funcionario import CadastrarFuncionario
from app.infra.repositories.fake_funcionario_repository import FakeFuncionarioRepository

repo = FakeFuncionarioRepository()

def get_cadastrar_funcionario_uc():
    return CadastrarFuncionario(repo)
