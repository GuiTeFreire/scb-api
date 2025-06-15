from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.aluguel import Aluguel

class AluguelRepository(ABC):
    @abstractmethod
    def salvar(self, aluguel: Aluguel) -> Aluguel: ...

    @abstractmethod
    def listar(self) -> List[Aluguel]: ...

    @abstractmethod
    def tem_aluguel_ativo(self, ciclista_id: int) -> bool: ...
