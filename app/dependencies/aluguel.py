from app.infra.repositories import fake_ciclista_repository, fake_aluguel_repository

from app.use_cases.buscar_bicicleta_alugada import BuscarBicicletaAlugada
from app.use_cases.verificar_permissao_aluguel import VerificarPermissaoAluguel
from app.use_cases.realizar_aluguel import RealizarAluguel
from app.use_cases.realizar_devolucao import RealizarDevolucao

def get_verificar_permissao_aluguel_use_case():
    return VerificarPermissaoAluguel(
        ciclista_repo=fake_ciclista_repository,
        aluguel_repo=fake_aluguel_repository
    )

def get_realizar_aluguel_use_case():
    return RealizarAluguel(fake_aluguel_repository, fake_ciclista_repository)

def get_buscar_bicicleta_alugada_use_case():
    return BuscarBicicletaAlugada(fake_aluguel_repository, fake_ciclista_repository)

def get_realizar_devolucao_use_case():
    return RealizarDevolucao(fake_aluguel_repository, fake_ciclista_repository)
