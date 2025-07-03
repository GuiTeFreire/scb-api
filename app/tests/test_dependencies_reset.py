from app.dependencies.reset import get_restaurar_banco_uc
from app.use_cases.restaurar_banco import RestaurarBanco

def test_get_restaurar_banco_uc():
    use_case = get_restaurar_banco_uc()
    assert isinstance(use_case, RestaurarBanco) 