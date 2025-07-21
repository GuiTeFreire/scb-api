from datetime import datetime
from fastapi import HTTPException
from app.domain.entities.devolucao import Devolucao
from app.domain.entities.ciclista import StatusEnum
from app.domain.repositories.aluguel_repository import AluguelRepository
from app.domain.repositories.ciclista_repository import CiclistaRepository
from app.domain.repositories.externo_repository import ExternoRepository
from app.domain.repositories.equipamento_repository import EquipamentoRepository

class RealizarDevolucao:
    def __init__(
        self, 
        aluguel_repo: AluguelRepository, 
        ciclista_repo: CiclistaRepository,
        externo_repo: ExternoRepository,
        equipamento_repo: EquipamentoRepository
    ):
        self.aluguel_repo = aluguel_repo
        self.ciclista_repo = ciclista_repo
        self.externo_repo = externo_repo
        self.equipamento_repo = equipamento_repo

    def execute(self, payload) -> Devolucao:
        id_bicicleta = payload.idBicicleta
        id_tranca = payload.idTranca

        if id_bicicleta is None or id_bicicleta <= 0:
            raise HTTPException(status_code=422, detail="Número da bicicleta inválido")

        alugueis = self.aluguel_repo.listar()
        aluguel_ativo = next(
            (a for a in alugueis if a.bicicleta == id_bicicleta and a.horaFim is None),
            None
        )
        if not aluguel_ativo:
            raise HTTPException(status_code=422, detail="Bicicleta não está alugada")

        tempo_uso = datetime.now() - aluguel_ativo.horaInicio
        horas_excedidas = max(0, (tempo_uso.total_seconds() / 3600) - 2)
        valor_extra = (horas_excedidas * 2) * 5.00
        valor_total = 10.00 + valor_extra

        aluguel_ativo.horaFim = datetime.now()
        aluguel_ativo.trancaFim = id_tranca

        # Sistema tranca a tranca (associa bicicleta e deixa OCUPADA)
        if not self.equipamento_repo.trancar_tranca(id_tranca, id_bicicleta):
            raise HTTPException(status_code=422, detail="Falha ao trancar a tranca no microsserviço de equipamento.")

        # Sistema envia email [R3] (integração com microsserviço externo)
        ciclista = self.ciclista_repo.buscar_por_id(aluguel_ativo.ciclista)
        if ciclista:
            self.externo_repo.enviar_email(
                email=ciclista.email,
                assunto="Devolução realizada com sucesso",
                mensagem=f"Sua devolução foi realizada. Bicicleta: {id_bicicleta}, Tranca: {id_tranca}, Valor: R$ {valor_total:.2f}"
            )

        # Sistema cobra valor extra, se houver
        cobranca_extra_id = None
        if valor_extra > 0:
            resultado_cobranca_extra = self.externo_repo.realizar_cobranca(aluguel_ativo.ciclista, valor_extra)
            print("[DEBUG] Resultado da cobrança extra:", resultado_cobranca_extra)
            cobranca_extra_id = resultado_cobranca_extra.get("id_cobranca") or resultado_cobranca_extra.get("id")

        cobranca_id_final = cobranca_extra_id if cobranca_extra_id is not None else int(round(aluguel_ativo.cobranca))
        print(f"[DEBUG] Valor total cobrado: {valor_total}, Valor extra: {valor_extra}")
        return Devolucao(
            bicicleta=aluguel_ativo.bicicleta,
            horaInicio=aluguel_ativo.horaInicio,
            trancaFim=aluguel_ativo.trancaFim,
            horaFim=aluguel_ativo.horaFim,
            cobranca=cobranca_id_final,
            ciclista=aluguel_ativo.ciclista
        )
