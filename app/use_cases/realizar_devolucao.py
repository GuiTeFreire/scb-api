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
        # 1. Sistema lê número da bicicleta
        id_bicicleta = payload.idBicicleta
        id_tranca = payload.idTranca

        # 2. Sistema valida número da bicicleta [E1]
        if id_bicicleta is None or id_bicicleta <= 0:
            raise HTTPException(status_code=422, detail="Número da bicicleta inválido")

        # 3. Verificar pré-condições
        alugueis = self.aluguel_repo.listar()
        aluguel_ativo = next(
            (a for a in alugueis if a.bicicleta == id_bicicleta and a.horaFim is None),
            None
        )
        if not aluguel_ativo:
            raise HTTPException(status_code=422, detail="Bicicleta não está alugada")

        # 4. Sistema calcula valor a pagar [R1]
        tempo_uso = datetime.now() - aluguel_ativo.horaInicio
        horas_excedidas = max(0, (tempo_uso.total_seconds() / 3600) - 2)
        valor_extra = (horas_excedidas * 2) * 5.00  # R$ 5,00 por meia hora
        valor_total = 10.00 + valor_extra  # Taxa básica + extra

        # 5. Sistema registra dados da devolução [R2]
        aluguel_ativo.horaFim = datetime.now()
        aluguel_ativo.trancaFim = id_tranca
        aluguel_ativo.cobranca = valor_total

        # 6. Sistema altera status da bicicleta para "disponível"
        print(f"[MOCK] Bicicleta {id_bicicleta} teve status alterado para DISPONÍVEL")

        # 7. Sistema altera status da tranca para "ocupada"
        print(f"[MOCK] Tranca {id_tranca} teve status alterado para OCUPADA")

        # 8. Sistema envia email [R3]
        print(f"[MOCK] E-mail enviado ao ciclista {aluguel_ativo.ciclista} com dados da devolução")

        return Devolucao(
            bicicleta=aluguel_ativo.bicicleta,
            horaInicio=aluguel_ativo.horaInicio,
            trancaFim=aluguel_ativo.trancaFim,
            horaFim=aluguel_ativo.horaFim,
            cobranca=aluguel_ativo.cobranca,
            ciclista=aluguel_ativo.ciclista
        )
