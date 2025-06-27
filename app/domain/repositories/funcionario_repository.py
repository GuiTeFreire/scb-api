from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.funcionario import Funcionario, NovoFuncionario

class FuncionarioRepository(ABC):
    @abstractmethod
    def salvar(self, dados: NovoFuncionario) -> Funcionario: ...

    @abstractmethod
    def listar_todos(self) -> List[Funcionario]: ...

    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[Funcionario]: ...

    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[Funcionario]: ...

    @abstractmethod
    def resetar(self) -> None: ...

    @abstractmethod
    def remover(self, id: int) -> bool: ...