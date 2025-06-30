from fastapi import HTTPException

from app.domain.entities.bicicleta import Bicicleta, StatusBicicletaEnum
from app.domain.repositories.aluguel_repository import AluguelRepository
from app.domain.repositories.ciclista_repository import CiclistaRepository
from app.domain.repositories.equipamento_repository import EquipamentoRepository

class BuscarBicicletaAlugada:
    def __init__(
        self,
        aluguel_repo: AluguelRepository,
        ciclista_repo: CiclistaRepository,
        equipamento_repo: EquipamentoRepository
    ):
        self.aluguel_repo = aluguel_repo
        self.ciclista_repo = ciclista_repo
        self.equipamento_repo = equipamento_repo

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
                # Obter dados reais da bicicleta do microsserviço de equipamento
                bicicleta_data = self.equipamento_repo.obter_bicicleta(aluguel.bicicleta)
                if bicicleta_data:
                    return Bicicleta(
                        id=bicicleta_data["id"],
                        marca=bicicleta_data["marca"],
                        modelo=bicicleta_data["modelo"],
                        ano=bicicleta_data["ano"],
                        numero=bicicleta_data["numero"],
                        status=StatusBicicletaEnum.EM_USO
                    )
        
        return None
