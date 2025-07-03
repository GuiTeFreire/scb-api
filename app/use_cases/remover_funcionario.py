from app.domain.repositories.funcionario_repository import FuncionarioRepository
from fastapi import HTTPException

class RemoverFuncionario:
    def __init__(self, repository: FuncionarioRepository):
        self.repository = repository

    def execute(self, id_funcionario: int) -> dict:
        sucesso = self.repository.remover(id_funcionario)
        if not sucesso:
            raise HTTPException(
                status_code=404,
                detail="Funcionário não encontrado"
            )
        return {"mensagem": "Funcionário removido com sucesso"}
