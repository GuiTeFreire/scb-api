from fastapi import HTTPException
from app.domain.repositories.ciclista_repository import CiclistaRepository
from app.domain.entities.ciclista import Ciclista

class AtivarCiclista:
    def __init__(self, repository: CiclistaRepository):
        self.repository = repository

    def execute(self, id_ciclista: int) -> Ciclista:
        ciclista = self.repository.buscar_por_id(id_ciclista)
        if not ciclista:
            raise HTTPException(status_code=404, detail="Ciclista não encontrado")

        ciclista.status = "ATIVO"
        return self.repository.atualizar(id_ciclista, ciclista.model_dump())
