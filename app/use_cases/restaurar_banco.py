from app.domain.repositories.funcionario_repository import FuncionarioRepository
from app.domain.repositories.ciclista_repository import CiclistaRepository
from app.domain.repositories.aluguel_repository import AluguelRepository

from app.infra.repositories.fake_funcionario_repository import fake_funcionario_repository as funcionario_repo
from app.infra.repositories.fake_ciclista_repository import fake_ciclista_repository as ciclista_repo
from app.infra.repositories.fake_aluguel_repository import fake_aluguel_repository

class RestaurarBanco:
    def __init__(
        self,
        funcionario_repo: FuncionarioRepository = funcionario_repo,
        ciclista_repo: CiclistaRepository = ciclista_repo,
        aluguel_repo: AluguelRepository = fake_aluguel_repository
    ):
        self.funcionario_repo = funcionario_repo
        self.ciclista_repo = ciclista_repo
        self.aluguel_repo = aluguel_repo

    def execute(self):
        self.funcionario_repo.resetar()
        self.ciclista_repo.resetar()
        self.aluguel_repo.resetar()
