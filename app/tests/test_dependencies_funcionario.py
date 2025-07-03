from app.dependencies.funcionario import (
    get_cadastrar_funcionario_use_case,
    get_listar_funcionarios_use_case,
    get_buscar_funcionario_use_case,
    get_atualizar_funcionario_use_case,
    get_remover_funcionario_use_case
)
from app.use_cases.cadastrar_funcionario import CadastrarFuncionario
from app.use_cases.listar_funcionarios import ListarFuncionarios
from app.use_cases.buscar_funcionario_por_id import BuscarFuncionarioPorId
from app.use_cases.atualizar_funcionario import AtualizarFuncionario
from app.use_cases.remover_funcionario import RemoverFuncionario

def test_get_cadastrar_funcionario_use_case():
    use_case = get_cadastrar_funcionario_use_case()
    assert isinstance(use_case, CadastrarFuncionario)

def test_get_listar_funcionarios_use_case():
    use_case = get_listar_funcionarios_use_case()
    assert isinstance(use_case, ListarFuncionarios)

def test_get_buscar_funcionario_use_case():
    use_case = get_buscar_funcionario_use_case()
    assert isinstance(use_case, BuscarFuncionarioPorId)

def test_get_atualizar_funcionario_use_case():
    use_case = get_atualizar_funcionario_use_case()
    assert isinstance(use_case, AtualizarFuncionario)

def test_get_remover_funcionario_use_case():
    use_case = get_remover_funcionario_use_case()
    assert isinstance(use_case, RemoverFuncionario) 