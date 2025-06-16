from datetime import datetime
from fastapi import HTTPException
from app.domain.entities.devolucao import NovoDevolucao, Devolucao
from app.domain.repositories.aluguel_repository import AluguelRepository
from app.domain.repositories.ciclista_repository import CiclistaRepository

class RealizarDevolucao:
    def __init__(self, aluguel_repo: AluguelRepository, ciclista_repo: CiclistaRepository):
        self.aluguel_repo = aluguel_repo
        self.ciclista_repo = ciclista_repo

    def execute(self, dados: NovoDevolucao) -> Devolucao:
        ciclista = self.ciclista_repo.buscar_por_id(dados.ciclista)
        if not ciclista or ciclista.status != "ATIVO":
            raise HTTPException(
                status_code=422,
                detail=[{"codigo": "422", "mensagem": "Ciclista inválido ou inativo"}]
            )

        alugueis = self.aluguel_repo.listar()
        aluguel_ativo = next(
            (a for a in alugueis if a.ciclista == dados.ciclista and a.horaFim is None),
            None
        )

        if not aluguel_ativo:
            raise HTTPException(
                status_code=422,
                detail=[{"codigo": "422", "mensagem": "Ciclista não possui aluguel ativo"}]
            )

        aluguel_ativo.horaFim = datetime.now()
        aluguel_ativo.trancaFim = dados.trancaFim

        # Simula cálculo e fila de cobrança
        aluguel_ativo.cobranca = 9999  # mock

        # Simula alteração do status da bicicleta
        print(f"[MOCK] Bicicleta {aluguel_ativo.bicicleta} teve status alterado para DISPONÍVEL")
        
        # Simula alteração do status da tranca
        print(f"[MOCK] Tranca {dados.trancaFim} teve status alterado para OCUPADA")
        
        # Simula notificação
        # print(f"Notificando ciclista {dados.ciclista} sobre devolução.")

        return Devolucao(
            bicicleta=aluguel_ativo.bicicleta,
            horaInicio=aluguel_ativo.horaInicio,
            horaFim=aluguel_ativo.horaFim,
            cobranca=aluguel_ativo.cobranca,
            ciclista=aluguel_ativo.ciclista,
            trancaFim=aluguel_ativo.trancaFim
        )
