from fastapi import HTTPException
from app.domain.repositories.ciclista_repository import CiclistaRepository
from app.domain.entities.ciclista import CartaoDeCredito

class ObterCartaoDeCredito:
    def __init__(self, repository: CiclistaRepository):
        self.repository = repository

    def execute(self, id_ciclista: int) -> CartaoDeCredito:
        ciclista = self.repository.buscar_por_id(id_ciclista)
        if not ciclista:
            raise HTTPException(
                status_code=404,
                detail={"codigo": "404", "mensagem": "Ciclista não encontrado"}
            )
        return ciclista.cartaoDeCredito
