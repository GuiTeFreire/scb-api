from fastapi import HTTPException
from app.domain.models.ciclista import Ciclista
from app.domain.repositories.ciclista_repository import CiclistaRepository

class BuscarCiclistaPorId:
    def __init__(self, repository: CiclistaRepository):
        self.repository = repository

    def execute(self, id_ciclista: int) -> Ciclista:
        ciclista = self.repository.buscar_por_id(id_ciclista)
        if not ciclista:
            raise HTTPException(status_code=404, detail="Ciclista não encontrado")
        return ciclista
