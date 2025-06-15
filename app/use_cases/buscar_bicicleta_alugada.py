from fastapi import HTTPException
from app.domain.entities.bicicleta import Bicicleta
from app.domain.repositories.aluguel_repository import AluguelRepository
from app.domain.repositories.ciclista_repository import CiclistaRepository

class BuscarBicicletaAlugada:
    def __init__(
        self,
        aluguel_repo: AluguelRepository,
        ciclista_repo: CiclistaRepository
    ):
        self.aluguel_repo = aluguel_repo
        self.ciclista_repo = ciclista_repo

    def execute(self, ciclista_id: int) -> Bicicleta | None:
        ciclista = self.ciclista_repo.buscar_por_id(ciclista_id)
        if not ciclista:
            raise HTTPException(
                status_code=404,
                detail={"codigo": "404", "mensagem": "Ciclista não encontrado"}
            )

        alugueis = self.aluguel_repo.listar()
        for aluguel in alugueis:
            if aluguel.ciclista == ciclista_id and aluguel.horaFim is None:
                return Bicicleta(
                    id=aluguel.bicicleta,
                    marca="MockMarca",
                    modelo="MockModelo",
                    ano=2020,
                    numero=aluguel.bicicleta,
                    status="EM_USO"
                )
        
        return None
