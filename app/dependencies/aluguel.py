from app.use_cases.realizar_aluguel import RealizarAluguel
from app.use_cases.realizar_devolucao import RealizarDevolucao
from app.use_cases.buscar_bicicleta_alugada import BuscarBicicletaAlugada
from app.use_cases.verificar_permissao_aluguel import VerificarPermissaoAluguel
from app.infra.repositories import fake_aluguel_repository, fake_ciclista_repository, fake_externo_repository, fake_equipamento_repository

def get_realizar_aluguel_use_case() -> RealizarAluguel:
    return RealizarAluguel(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )

def get_realizar_devolucao_use_case() -> RealizarDevolucao:
    return RealizarDevolucao(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )

def get_buscar_bicicleta_alugada_use_case() -> BuscarBicicletaAlugada:
    return BuscarBicicletaAlugada(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_equipamento_repository
    )

def get_verificar_permissao_aluguel_use_case() -> VerificarPermissaoAluguel:
    return VerificarPermissaoAluguel(
        fake_ciclista_repository,
        fake_aluguel_repository
    )
