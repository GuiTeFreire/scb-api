from app.dependencies.ciclista import repo

from app.infra.repositories.fake_aluguel_repository import fake_aluguel_repository

from app.use_cases.verificar_permissao_aluguel import VerificarPermissaoAluguel
from app.use_cases.realizar_aluguel import RealizarAluguel

def get_verificar_permissao_aluguel_uc():
    return VerificarPermissaoAluguel(
        ciclista_repo=repo,
        aluguel_repo=fake_aluguel_repository
    )

def get_realizar_aluguel_use_case():
    return RealizarAluguel(fake_aluguel_repository, repo)