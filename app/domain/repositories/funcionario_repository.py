from abc import ABC, abstractmethod
from app.domain.entities.funcionario import Funcionario, NovoFuncionario
from typing import List, Optional

class FuncionarioRepository(ABC):
    @abstractmethod
    def salvar(self, dados: NovoFuncionario) -> Funcionario: ...

    @abstractmethod
    def listar_todos(self) -> List[Funcionario]: ...

    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[Funcionario]: ...

    @abstractmethod
    def resetar(self) -> None: ...