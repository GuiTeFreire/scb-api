from fastapi import HTTPException
from app.domain.repositories.ciclista_repository import CiclistaRepository
from app.domain.repositories.aluguel_repository import AluguelRepository

class VerificarPermissaoAluguel:
    def __init__(
        self,
        ciclista_repo: CiclistaRepository,
        aluguel_repo: AluguelRepository
    ):
        self.ciclista_repo = ciclista_repo
        self.aluguel_repo = aluguel_repo

    def execute(self, id_ciclista: int) -> bool:
        ciclista = self.ciclista_repo.buscar_por_id(id_ciclista)
        if not ciclista:
            raise HTTPException(
                status_code=404,
                detail={"codigo": "404", "mensagem": "Ciclista não encontrado"}
            )
        return not self.aluguel_repo.tem_aluguel_ativo(id_ciclista)
