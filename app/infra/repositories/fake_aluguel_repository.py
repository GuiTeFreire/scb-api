from typing import List

from app.domain.entities.aluguel import Aluguel
from app.domain.repositories.aluguel_repository import AluguelRepository

class FakeAluguelRepository(AluguelRepository):
    def __init__(self):
        self._db: List[Aluguel] = []
        self._contador_id = 1

    def salvar(self, aluguel: Aluguel) -> Aluguel:
        aluguel.id = self._contador_id
        self._contador_id += 1
        self._db.append(aluguel)
        return aluguel

    def listar(self) -> List[Aluguel]:
        return self._db

    def tem_aluguel_ativo(self, ciclista_id: int) -> bool:
        for aluguel in self._db:
            if aluguel.ciclista == ciclista_id and aluguel.horaFim is None:
                return True
        return False

    def resetar(self):
        self._db.clear()
        self._contador_id = 1

fake_aluguel_repository = FakeAluguelRepository()