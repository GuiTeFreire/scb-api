import os
from app.infra.repositories import fake_ciclista_repository
from app.use_cases.cadastrar_ciclista import CadastrarCiclista
from app.use_cases.buscar_ciclista_por_id import BuscarCiclistaPorId
from app.use_cases.atualizar_ciclista import AtualizarCiclista
from app.use_cases.ativar_ciclista import AtivarCiclista
from app.use_cases.obter_cartao_de_credito import ObterCartaoDeCredito
from app.use_cases.atualizar_cartao_de_credito import AtualizarCartaoDeCredito
from app.use_cases.verificar_email_existente import VerificarEmailExistente

def get_cadastrar_ciclista_use_case() -> CadastrarCiclista:
    from app.infra.repositories.http_externo_repository import HttpExternoRepository
    return CadastrarCiclista(fake_ciclista_repository, HttpExternoRepository())

def get_buscar_ciclista_use_case() -> BuscarCiclistaPorId:
    return BuscarCiclistaPorId(fake_ciclista_repository)

def get_atualizar_ciclista_use_case() -> AtualizarCiclista:
    from app.infra.repositories.http_externo_repository import HttpExternoRepository
    return AtualizarCiclista(fake_ciclista_repository, HttpExternoRepository())

def get_ativar_ciclista_use_case() -> AtivarCiclista:
    return AtivarCiclista(fake_ciclista_repository)

def get_obter_cartao_use_case() -> ObterCartaoDeCredito:
    return ObterCartaoDeCredito(fake_ciclista_repository)

def get_atualizar_cartao_use_case() -> AtualizarCartaoDeCredito:
    from app.infra.repositories.http_externo_repository import HttpExternoRepository
    return AtualizarCartaoDeCredito(fake_ciclista_repository, HttpExternoRepository())

def get_verificar_email_use_case() -> VerificarEmailExistente:
    return VerificarEmailExistente(fake_ciclista_repository)