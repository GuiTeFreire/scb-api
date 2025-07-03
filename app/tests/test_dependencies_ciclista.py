import pytest
from app.dependencies.ciclista import (
    get_cadastrar_ciclista_use_case,
    get_buscar_ciclista_use_case,
    get_atualizar_ciclista_use_case,
    get_ativar_ciclista_use_case,
    get_obter_cartao_use_case,
    get_atualizar_cartao_use_case,
    get_verificar_email_use_case
)
from app.use_cases.cadastrar_ciclista import CadastrarCiclista
from app.use_cases.buscar_ciclista_por_id import BuscarCiclistaPorId
from app.use_cases.atualizar_ciclista import AtualizarCiclista
from app.use_cases.ativar_ciclista import AtivarCiclista
from app.use_cases.obter_cartao_de_credito import ObterCartaoDeCredito
from app.use_cases.atualizar_cartao_de_credito import AtualizarCartaoDeCredito
from app.use_cases.verificar_email_existente import VerificarEmailExistente

def test_get_cadastrar_ciclista_use_case():
    use_case = get_cadastrar_ciclista_use_case()
    assert isinstance(use_case, CadastrarCiclista)

def test_get_buscar_ciclista_use_case():
    use_case = get_buscar_ciclista_use_case()
    assert isinstance(use_case, BuscarCiclistaPorId)

def test_get_atualizar_ciclista_use_case():
    use_case = get_atualizar_ciclista_use_case()
    assert isinstance(use_case, AtualizarCiclista)

def test_get_ativar_ciclista_use_case():
    use_case = get_ativar_ciclista_use_case()
    assert isinstance(use_case, AtivarCiclista)

def test_get_obter_cartao_use_case():
    use_case = get_obter_cartao_use_case()
    assert isinstance(use_case, ObterCartaoDeCredito)

def test_get_atualizar_cartao_use_case():
    use_case = get_atualizar_cartao_use_case()
    assert isinstance(use_case, AtualizarCartaoDeCredito)

def test_get_verificar_email_use_case():
    use_case = get_verificar_email_use_case()
    assert isinstance(use_case, VerificarEmailExistente) 