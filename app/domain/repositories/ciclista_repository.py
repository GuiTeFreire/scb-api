from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.ciclista import Ciclista

class CiclistaRepository(ABC):
    @abstractmethod
    def salvar(self, ciclista: Ciclista) -> Ciclista: ...
    
    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[Ciclista]: ...

    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[Ciclista]: ...

    @abstractmethod
    def atualizar(self, id: int, dados: dict) -> Optional[Ciclista]: ...
