from datetime import datetime
from fastapi import HTTPException
from app.domain.entities.devolucao import NovoDevolucao, Devolucao
from app.domain.entities.ciclista import StatusEnum
from app.domain.repositories.aluguel_repository import AluguelRepository
from app.domain.repositories.ciclista_repository import CiclistaRepository

class RealizarDevolucao:
    def __init__(self, aluguel_repo: AluguelRepository, ciclista_repo: CiclistaRepository):
        self.aluguel_repo = aluguel_repo
        self.ciclista_repo = ciclista_repo

    def execute(self, payload) -> Devolucao:
        id_tranca = payload.idTranca
        id_bicicleta = payload.idBicicleta

        if id_tranca is None or id_bicicleta is None:
            raise HTTPException(
                status_code=422,
                detail="Dados Inválidos"
            )

        alugueis = self.aluguel_repo.listar()
        aluguel_ativo = next(
            (a for a in alugueis if a.bicicleta == id_bicicleta and a.horaFim is None),
            None
        )

        if not aluguel_ativo:
            raise HTTPException(
                status_code=422,
                detail="Bicicleta não está alugada ou já foi devolvida"
            )

        aluguel_ativo.horaFim = datetime.now()
        aluguel_ativo.trancaFim = id_tranca
        aluguel_ativo.cobranca = 100  # mock

        # Simula alteração do status da bicicleta
        print(f"[MOCK] Bicicleta {aluguel_ativo.bicicleta} teve status alterado para DISPONÍVEL")
        # Simula alteração do status da tranca
        print(f"[MOCK] Tranca {id_tranca} teve status alterado para OCUPADA")

        return Devolucao(
            bicicleta=aluguel_ativo.bicicleta,
            horaInicio=aluguel_ativo.horaInicio,
            trancaFim=aluguel_ativo.trancaFim,
            horaFim=aluguel_ativo.horaFim,
            cobranca=aluguel_ativo.cobranca,
            ciclista=aluguel_ativo.ciclista
        )
