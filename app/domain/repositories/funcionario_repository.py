from abc import ABC, abstractmethod
from app.domain.entities.funcionario import Funcionario, NovoFuncionario

class FuncionarioRepository(ABC):
    @abstractmethod
    def salvar(self, dados: NovoFuncionario) -> Funcionario: ...
