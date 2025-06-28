from datetime import datetime
from fastapi import HTTPException

from app.domain.entities.aluguel import Aluguel, NovoAluguel
from app.domain.entities.ciclista import StatusEnum
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
        # 1. Sistema solicita número da tranca (já recebido em dados.trancaInicio)
        
        # 2. Ciclista informa número da tranca (já recebido)
        
        # 3. Sistema valida número da tranca [A1]
        if dados.trancaInicio <= 0:
            raise HTTPException(status_code=422, detail="Número da tranca inválido")
        
        # 4. Sistema verifica se ciclista pode pegar bicicleta [R1][R5][E1][E4]
        ciclista = self.ciclista_repo.buscar_por_id(dados.ciclista)
        if not ciclista or ciclista.status != StatusEnum.ATIVO:
            raise HTTPException(status_code=422, detail="Ciclista não está ativo")
        
        if not self.verificador.execute(dados.ciclista):
            raise HTTPException(status_code=422, detail="Ciclista já possui aluguel ativo")
        
        # 5. Verificar se tranca está ocupada (pré-condição)
        # if dados.trancaInicio.status != "OCUPADA":
        #     raise HTTPException(status_code=422, detail="Tranca não está ocupada")
        
        # 6. Sistema lê número da bicicleta presa na tranca [E2]
        id_bicicleta = 5678 # Mock
        
        # 7. Verificar se bicicleta não está em reparo [E4][R5]
        # if id_bicicleta.status != "EM_REPARO":
        #     raise HTTPException(status_code=422, detail="Bicicleta em reparo")
        
        # 8. Sistema envia cobrança [R2]
        id_cobranca = 1234
        valor_cobranca = 10.00
        print(f"[MOCK] Cobrança de R$ {valor_cobranca:.2f} realizada com sucesso")
        
        # 9. Sistema registra dados da retirada [R3]
        aluguel = Aluguel(
            ciclista=dados.ciclista,
            trancaInicio=dados.trancaInicio,
            bicicleta=id_bicicleta,
            horaInicio=datetime.now(),
            trancaFim=None,
            horaFim=None,
            cobranca=id_cobranca
        )
        
        # 10. Sistema altera status da bicicleta para "em uso"
        print(f"[MOCK] Bicicleta {id_bicicleta} teve status alterado para EM_USO")
        
        # 11. Sistema altera status da tranca para "livre"
        print(f"[MOCK] Tranca {dados.trancaInicio} teve status alterado para LIVRE")
        
        # 12. Sistema envia email [R4]
        print(f"[MOCK] E-mail enviado ao ciclista {dados.ciclista} com dados do aluguel.")
        
        return self.aluguel_repo.salvar(aluguel)