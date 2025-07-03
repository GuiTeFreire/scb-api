from app.dependencies.aluguel import (
    get_realizar_aluguel_use_case,
    get_realizar_devolucao_use_case,
    get_buscar_bicicleta_alugada_use_case,
    get_verificar_permissao_aluguel_use_case
)
from app.use_cases.realizar_aluguel import RealizarAluguel
from app.use_cases.realizar_devolucao import RealizarDevolucao
from app.use_cases.buscar_bicicleta_alugada import BuscarBicicletaAlugada
from app.use_cases.verificar_permissao_aluguel import VerificarPermissaoAluguel

def test_get_realizar_aluguel_use_case():
    use_case = get_realizar_aluguel_use_case()
    assert isinstance(use_case, RealizarAluguel)

def test_get_realizar_devolucao_use_case():
    use_case = get_realizar_devolucao_use_case()
    assert isinstance(use_case, RealizarDevolucao)

def test_get_buscar_bicicleta_alugada_use_case():
    use_case = get_buscar_bicicleta_alugada_use_case()
    assert isinstance(use_case, BuscarBicicletaAlugada)

def test_get_verificar_permissao_aluguel_use_case():
    use_case = get_verificar_permissao_aluguel_use_case()
    assert isinstance(use_case, VerificarPermissaoAluguel) 