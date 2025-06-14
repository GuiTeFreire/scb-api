from typing import List, Optional

from app.domain.entities.ciclista import Ciclista
from app.domain.repositories.ciclista_repository import CiclistaRepository

class FakeCiclistaRepository(CiclistaRepository):
    def __init__(self):
        self._db: List[Ciclista] = []
        self._current_id = 1

    def salvar(self, ciclista: Ciclista) -> Ciclista:
        ciclista.id = self._current_id
        self._current_id += 1
        self._db.append(ciclista)
        return ciclista

    def buscar_por_id(self, id: int) -> Optional[Ciclista]:
        for c in self._db:
            if c.id == id:
                return c
        return None

    def buscar_por_email(self, email: str) -> Optional[Ciclista]:
        for c in self._db:
            if c.email == email:
                return c
        return None

    def atualizar(self, id: int, dados: dict) -> Optional[Ciclista]:
        for c in self._db:
            if c.id == id:
                for key, value in dados.items():
                    setattr(c, key, value)
                return c
        return None
    
    def resetar(self):
        self._db.clear()
        self._current_id = 1

    def proximo_id(self) -> int:
        return self._current_id