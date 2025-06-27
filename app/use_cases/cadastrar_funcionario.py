from fastapi import HTTPException
from app.domain.repositories.funcionario_repository import FuncionarioRepository
from app.domain.entities.funcionario import NovoFuncionario, Funcionario

class CadastrarFuncionario:
    def __init__(self, repository: FuncionarioRepository):
        self.repository = repository

    def execute(self, dados: NovoFuncionario) -> Funcionario:
        if self.repository.buscar_por_email(dados.email):
            raise HTTPException(
                status_code=422,
                detail="E-mail já cadastrado"
            )
        
        return self.repository.salvar(dados)
