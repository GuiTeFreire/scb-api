from datetime import datetime
from fastapi import HTTPException

from app.domain.entities.aluguel import Aluguel, NovoAluguel
from app.domain.repositories.aluguel_repository import AluguelRepository
from app.domain.repositories.ciclista_repository import CiclistaRepository
from app.use_cases.verificar_permissao_aluguel import VerificarPermissaoAluguel

class RealizarAluguel:
    def __init__(
        self,
        aluguel_repo: AluguelRepository,
        ciclista_repo: CiclistaRepository
    ):
        self.aluguel_repo = aluguel_repo
        self.ciclista_repo = ciclista_repo
        self.verificador = VerificarPermissaoAluguel(ciclista_repo, aluguel_repo)

    def execute(self, dados: NovoAluguel) -> Aluguel:
        # Regra: só pode alugar se estiver com status ATIVO e sem aluguel ativo
        ciclista = self.ciclista_repo.buscar_por_id(dados.ciclista)
        if not ciclista or ciclista.status != "ATIVO":
            raise HTTPException(
                status_code=422,
                detail=[{"codigo": "422", "mensagem": "Ciclista não está ativo"}]
            )

        if not self.verificador.execute(dados.ciclista):
            raise HTTPException(
                status_code=422,
                detail=[{"codigo": "422", "mensagem": "Ciclista já possui aluguel ativo"}]
            )

        # Regras adicionais como verificação do status da tranca ou bicicleta
        # são simuladas (em produção, esses dados viriam de outros serviços)
        id_bicicleta = 5678  # mock: bicicleta disponível
        id_cobranca = 1234   # mock: cobrança bem-sucedida

        # Simulação: notificação enviada ao ciclista
        # print(f"Notificação: aluguel iniciado para ciclista {dados.ciclista}")

        aluguel = Aluguel(
            ciclista=dados.ciclista,
            trancaInicio=dados.trancaInicio,
            bicicleta=id_bicicleta,
            horaInicio=datetime.now(),
            trancaFim=None,
            horaFim=None,
            cobranca=id_cobranca
        )

        return self.aluguel_repo.salvar(aluguel)