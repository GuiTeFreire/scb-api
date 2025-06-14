from fastapi import HTTPException
from app.domain.entities.ciclista import NovoCartaoDeCredito
from app.domain.repositories.ciclista_repository import CiclistaRepository

class AtualizarCartaoDeCredito:
    def __init__(self, repository: CiclistaRepository):
        self.repository = repository

    def execute(self, id_ciclista: int, novo_cartao: NovoCartaoDeCredito):
        ciclista = self.repository.buscar_por_id(id_ciclista)
        if not ciclista:
            raise HTTPException(
                status_code=404,
                detail={"codigo": "404", "mensagem": "Ciclista não encontrado"}
            )

        ciclista.cartaoDeCredito = novo_cartao.model_copy(update={"id": id_ciclista})
        self.repository.atualizar(id_ciclista, {"cartaoDeCredito": ciclista.cartaoDeCredito})
        return ciclista.cartaoDeCredito
