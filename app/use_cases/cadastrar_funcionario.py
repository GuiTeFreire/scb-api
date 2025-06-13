from app.domain.repositories.funcionario_repository import FuncionarioRepository
from app.domain.entities.funcionario import NovoFuncionario, Funcionario

class CadastrarFuncionario:
    def __init__(self, repository: FuncionarioRepository):
        self.repository = repository

    def execute(self, dados: NovoFuncionario) -> Funcionario:
        return self.repository.salvar(dados)
