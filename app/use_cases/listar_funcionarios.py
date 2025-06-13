from typing import List
from app.domain.entities.funcionario import Funcionario
from app.domain.repositories.funcionario_repository import FuncionarioRepository

class ListarFuncionarios:
    def __init__(self, repository: FuncionarioRepository):
        self.repository = repository

    def execute(self) -> List[Funcionario]:
        return self.repository.listar_todos()
