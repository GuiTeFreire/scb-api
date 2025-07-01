from datetime import datetime
from fastapi import HTTPException

from app.domain.entities.aluguel import Aluguel, NovoAluguel
from app.domain.entities.ciclista import StatusEnum
from app.domain.repositories.aluguel_repository import AluguelRepository
from app.domain.repositories.ciclista_repository import CiclistaRepository
from app.domain.repositories.externo_repository import ExternoRepository
from app.domain.repositories.equipamento_repository import EquipamentoRepository
from app.use_cases.verificar_permissao_aluguel import VerificarPermissaoAluguel

class RealizarAluguel:
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
        self.verificador = VerificarPermissaoAluguel(ciclista_repo, aluguel_repo)

    def execute(self, dados: NovoAluguel) -> Aluguel:
        if dados.trancaInicio <= 0:
            raise HTTPException(status_code=422, detail="Número da tranca inválido")
        
        ciclista = self.ciclista_repo.buscar_por_id(dados.ciclista)
        if not ciclista or ciclista.status != StatusEnum.ATIVO:
            raise HTTPException(status_code=422, detail="Ciclista não está ativo")
        
        if not self.verificador.execute(dados.ciclista):
            raise HTTPException(status_code=422, detail="Ciclista já possui aluguel ativo")
        
        # Verificar se tranca está ocupada (integração com microsserviço de equipamento)
        tranca = self.equipamento_repo.obter_tranca(dados.trancaInicio)
        if not tranca:
            raise HTTPException(status_code=422, detail="Tranca não encontrada")
        
        if tranca["status"] != "OCUPADA":
            raise HTTPException(status_code=422, detail="Tranca não está ocupada")
        
        bicicleta_na_tranca = self.equipamento_repo.obter_bicicleta_na_tranca(dados.trancaInicio)
        if not bicicleta_na_tranca:
            raise HTTPException(status_code=422, detail="Nenhuma bicicleta encontrada na tranca")
        
        id_bicicleta = bicicleta_na_tranca["id"]
        
        bicicleta = self.equipamento_repo.obter_bicicleta(id_bicicleta)
        if not bicicleta:
            raise HTTPException(status_code=422, detail="Bicicleta não encontrada")
        
        if bicicleta["status"] in ["EM_REPARO", "APOSENTADA"]:
            raise HTTPException(status_code=422, detail="Bicicleta em reparo ou aposentada")
        
        # Sistema envia cobrança [R2] (integração com microsserviço externo)
        valor_cobranca = 10.00
        resultado_cobranca = self.externo_repo.realizar_cobranca(dados.ciclista, valor_cobranca)
        cobranca_id = None
        if resultado_cobranca["status"] != "APROVADA":
            self.externo_repo.incluir_cobranca_fila(dados.ciclista, valor_cobranca)
        else:
            cobranca_id = resultado_cobranca["id_cobranca"]

        aluguel = Aluguel(
            ciclista=dados.ciclista,
            trancaInicio=dados.trancaInicio,
            bicicleta=id_bicicleta,
            horaInicio=datetime.now(),
            trancaFim=None,
            horaFim=None,
            cobranca=cobranca_id
        )
        
        # Sistema altera status da bicicleta para "em uso" (integração com microsserviço de equipamento)
        self.equipamento_repo.alterar_status_bicicleta(id_bicicleta, "EM_USO")
        
        # Sistema altera status da tranca para "livre" (integração com microsserviço de equipamento)
        self.equipamento_repo.alterar_status_tranca(dados.trancaInicio, "LIVRE")
        
        # Sistema envia email [R4] (integração com microsserviço externo)
        self.externo_repo.enviar_email(
            email=ciclista.email,
            assunto="Aluguel realizado com sucesso",
            mensagem=f"Seu aluguel foi realizado. Bicicleta: {id_bicicleta}, Tranca: {dados.trancaInicio}"
        )
        
        return self.aluguel_repo.salvar(aluguel)