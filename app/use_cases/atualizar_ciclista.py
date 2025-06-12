from fastapi import HTTPException
from app.domain.models.ciclista import Ciclista
from app.domain.repositories.ciclista_repository import CiclistaRepository
from app.domain.models.ciclista import EdicaoCiclista

class AtualizarCiclista:
    def __init__(self, repository: CiclistaRepository):
        self.repository = repository

    def execute(self, id_ciclista: int, dados: EdicaoCiclista) -> Ciclista:
        if (dados.cpf and dados.passaporte) or (not dados.cpf and not dados.passaporte):
            raise HTTPException(status_code=422)

        ciclista = self.repository.atualizar(id_ciclista, dados.model_dump())
        if not ciclista:
            raise HTTPException(status_code=404)

        return ciclista
