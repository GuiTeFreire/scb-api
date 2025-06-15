from app.infra.repositories import fake_funcionario_repository

from app.use_cases.atualizar_funcionario import AtualizarFuncionario
from app.use_cases.buscar_funcionario_por_id import BuscarFuncionarioPorId
from app.use_cases.cadastrar_funcionario import CadastrarFuncionario
from app.use_cases.listar_funcionarios import ListarFuncionarios
from app.use_cases.remover_funcionario import RemoverFuncionario

def get_cadastrar_funcionario_use_case():
    return CadastrarFuncionario(fake_funcionario_repository)

def get_listar_funcionarios_use_case():
    return ListarFuncionarios(fake_funcionario_repository)

def get_buscar_funcionario_use_case():
    return BuscarFuncionarioPorId(fake_funcionario_repository)

def get_atualizar_funcionario_use_case():
    return AtualizarFuncionario(fake_funcionario_repository)

def get_remover_funcionario_use_case():
    return RemoverFuncionario(fake_funcionario_repository)
