from app.domain.repositories.funcionario_repository import FuncionarioRepository
from app.domain.repositories.ciclista_repository import CiclistaRepository
from app.infra.repositories import fake_funcionario_repository, fake_ciclista_repository

class RestaurarBanco:
    def __init__(self, funcionario_repo: FuncionarioRepository, ciclista_repo: CiclistaRepository):
        self.funcionario_repo = funcionario_repo
        self.ciclista_repo = ciclista_repo

    def execute(self):
        self.funcionario_repo.resetar()
        self.ciclista_repo.resetar()