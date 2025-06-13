from app.domain.repositories.funcionario_repository import FuncionarioRepository
from app.domain.entities.funcionario import NovoFuncionario, Funcionario
from fastapi import HTTPException

class AtualizarFuncionario:
    def __init__(self, repository: FuncionarioRepository):
        self.repository = repository

    def execute(self, id_funcionario: int, dados: NovoFuncionario) -> Funcionario:
        funcionario = self.repository.atualizar(id_funcionario, dados)
        if not funcionario:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")
        return funcionario
