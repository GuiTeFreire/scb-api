from app.infra.repositories import fake_ciclista_repository as repo

from app.use_cases.ativar_ciclista import AtivarCiclista
from app.use_cases.atualizar_cartao_de_credito import AtualizarCartaoDeCredito
from app.use_cases.atualizar_ciclista import AtualizarCiclista
from app.use_cases.buscar_ciclista_por_id import BuscarCiclistaPorId
from app.use_cases.cadastrar_ciclista import CadastrarCiclista
from app.use_cases.obter_cartao_de_credito import ObterCartaoDeCredito
from app.use_cases.verificar_email_existente import VerificarEmailExistente

def get_buscar_ciclista_use_case():
    return BuscarCiclistaPorId(repo)

def get_atualizar_ciclista_use_case():
    return AtualizarCiclista(repo)

def get_cadastrar_ciclista_use_case():
    return CadastrarCiclista(repo)

def get_verificar_email_use_case():
    return VerificarEmailExistente(repo)

def get_ativar_ciclista_use_case() -> AtivarCiclista:
    return AtivarCiclista(repo)

def get_obter_cartao_use_case():
    return ObterCartaoDeCredito(repo)

def get_atualizar_cartao_use_case():
    return AtualizarCartaoDeCredito(repo)