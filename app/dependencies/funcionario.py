from app.use_cases.cadastrar_funcionario import CadastrarFuncionario
from app.use_cases.listar_funcionarios import ListarFuncionarios
from app.use_cases.buscar_funcionario_por_id import BuscarFuncionarioPorId
from app.infra.repositories import fake_funcionario_repository

def get_cadastrar_funcionario_uc():
    return CadastrarFuncionario(fake_funcionario_repository)

def get_listar_funcionarios_uc():
    return ListarFuncionarios(fake_funcionario_repository)

def get_buscar_funcionario_uc():
    return BuscarFuncionarioPorId(fake_funcionario_repository)
