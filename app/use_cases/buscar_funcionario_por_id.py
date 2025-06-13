from fastapi import HTTPException
from app.domain.repositories.funcionario_repository import FuncionarioRepository

class BuscarFuncionarioPorId:
    def __init__(self, repository: FuncionarioRepository):
        self.repository = repository

    def execute(self, id_funcionario: int):
        funcionario = self.repository.buscar_por_id(id_funcionario)
        if not funcionario:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")
        return funcionario
