from abc import ABC, abstractmethod
from app.domain.entities.funcionario import Funcionario, NovoFuncionario
from typing import List

class FuncionarioRepository(ABC):
    @abstractmethod
    def salvar(self, dados: NovoFuncionario) -> Funcionario: ...

class FuncionarioRepository(ABC):
    @abstractmethod
    def listar_todos(self) -> List[Funcionario]: ...