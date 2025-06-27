from app.infra.repositories import fake_ciclista_repository, fake_funcionario_repository, fake_aluguel_repository

from app.use_cases.restaurar_banco import RestaurarBanco

def get_restaurar_banco_uc():
    return RestaurarBanco(
        funcionario_repo=fake_funcionario_repository,
        ciclista_repo=fake_ciclista_repository,
        aluguel_repo=fake_aluguel_repository
    )