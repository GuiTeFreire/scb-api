from app.dependencies.ciclista import repo

from app.infra.repositories.fake_aluguel_repository import fake_aluguel_repository
from app.infra.repositories.fake_ciclista_repository import fake_ciclista_repository

from app.use_cases.buscar_bicicleta_alugada import BuscarBicicletaAlugada
from app.use_cases.verificar_permissao_aluguel import VerificarPermissaoAluguel
from app.use_cases.realizar_aluguel import RealizarAluguel
from app.use_cases.realizar_devolucao import RealizarDevolucao

def get_verificar_permissao_aluguel_use_case():
    return VerificarPermissaoAluguel(
        ciclista_repo=repo,
        aluguel_repo=fake_aluguel_repository
    )

def get_realizar_aluguel_use_case():
    return RealizarAluguel(fake_aluguel_repository, repo)

def get_buscar_bicicleta_alugada_use_case():
    return BuscarBicicletaAlugada(fake_aluguel_repository, repo)

def get_realizar_devolucao_use_case():
    return RealizarDevolucao(fake_aluguel_repository, repo)
