import os
from app.use_cases.realizar_aluguel import RealizarAluguel
from app.use_cases.realizar_devolucao import RealizarDevolucao
from app.use_cases.buscar_bicicleta_alugada import BuscarBicicletaAlugada
from app.use_cases.verificar_permissao_aluguel import VerificarPermissaoAluguel
from app.infra.repositories import fake_aluguel_repository, fake_ciclista_repository

def get_realizar_aluguel_use_case() -> RealizarAluguel:
    from app.infra.repositories.http_externo_repository import HttpExternoRepository
    from app.infra.repositories.http_equipamento_repository import HttpEquipamentoRepository
    return RealizarAluguel(
        fake_aluguel_repository,
        fake_ciclista_repository,
        HttpExternoRepository(),
        HttpEquipamentoRepository()
    )

def get_realizar_devolucao_use_case() -> RealizarDevolucao:
    from app.infra.repositories.http_externo_repository import HttpExternoRepository
    from app.infra.repositories.http_equipamento_repository import HttpEquipamentoRepository
    return RealizarDevolucao(
        fake_aluguel_repository,
        fake_ciclista_repository,
        HttpExternoRepository(),
        HttpEquipamentoRepository()
    )

def get_buscar_bicicleta_alugada_use_case() -> BuscarBicicletaAlugada:
    from app.infra.repositories.http_equipamento_repository import HttpEquipamentoRepository
    return BuscarBicicletaAlugada(
        fake_aluguel_repository,
        fake_ciclista_repository,
        HttpEquipamentoRepository()
    )

def get_verificar_permissao_aluguel_use_case() -> VerificarPermissaoAluguel:
    return VerificarPermissaoAluguel(
        fake_ciclista_repository,
        fake_aluguel_repository
    )
