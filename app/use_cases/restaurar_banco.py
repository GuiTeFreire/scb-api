from app.domain.repositories.funcionario_repository import FuncionarioRepository
from app.domain.repositories.ciclista_repository import CiclistaRepository
from app.domain.repositories.aluguel_repository import AluguelRepository

from app.infra.repositories import fake_funcionario_repository, fake_ciclista_repository, fake_aluguel_repository

class RestaurarBanco:
    def __init__(
        self,
        funcionario_repo: FuncionarioRepository = fake_funcionario_repository,
        ciclista_repo: CiclistaRepository = fake_ciclista_repository,
        aluguel_repo: AluguelRepository = fake_aluguel_repository
    ):
        self.funcionario_repo = funcionario_repo
        self.ciclista_repo = ciclista_repo
        self.aluguel_repo = aluguel_repo
    
    def execute(self):
        self.funcionario_repo.resetar()
        self.ciclista_repo.resetar()
        self.aluguel_repo.resetar()

    def restaurar_dados_iniciais(self):
        self.execute()
        # Funcionários
        from app.domain.entities.funcionario import NovoFuncionario
        funcionario = NovoFuncionario(
            senha="123",
            confirmacaoSenha="123",
            email="employee@example.com",
            nome="Beltrano",
            idade=25,
            funcao="Reparador",
            cpf="99999999999"
        )
        self.funcionario_repo.salvar(funcionario)

        # Ciclistas
        from app.domain.entities.ciclista import Ciclista, CartaoDeCredito, StatusEnum
        from datetime import date
        cartao = lambda id: CartaoDeCredito(
            id=id,
            nomeTitular="Fulano Beltrano",
            numero="4012001037141112",
            validade="12/2022",
            cvv="132"
        )
        nome_ciclistas="Fulano Beltrano"

        ciclistas = [
            Ciclista(
                id=1,
                status=StatusEnum.ATIVO,
                nome=nome_ciclistas,
                nascimento=date(2021,5,2),
                cpf="78804034009",
                nacionalidade="Brasileiro",
                email="user@example.com",
                senha="ABC123",
                cartaoDeCredito=cartao(1)
            ),
            Ciclista(
                id=2,
                status=StatusEnum.AGUARDANDO_CONFIRMACAO,
                nome=nome_ciclistas,
                nascimento=date(2021,5,2),
                cpf="43943488039",
                nacionalidade="Brasileiro",
                email="user2@example.com",
                senha="ABC123",
                cartaoDeCredito=cartao(2)
            ),
            Ciclista(
                id=3,
                status=StatusEnum.ATIVO,
                nome=nome_ciclistas,
                nascimento=date(2021,5,2),
                cpf="10243164084",
                nacionalidade="Brasileiro",
                email="user3@example.com",
                senha="ABC123",
                cartaoDeCredito=cartao(3)
            ),
            Ciclista(
                id=4,
                status=StatusEnum.ATIVO,
                nome=nome_ciclistas,
                nascimento=date(2021,5,2),
                cpf="30880150017",
                nacionalidade="Brasileiro",
                email="user4@example.com",
                senha="ABC123",
                cartaoDeCredito=cartao(4)
            ),
        ]
        for c in ciclistas:
            self.ciclista_repo.salvar(c)

        # Alugueis
        from app.domain.entities.aluguel import Aluguel
        from datetime import datetime, timedelta
        now = datetime.now()
        alugueis = [
            Aluguel(
                id=1,
                ciclista=3,
                bicicleta=3,
                trancaInicio=2,
                horaInicio=now,
                trancaFim=None,
                horaFim=None,
                cobranca=1
            ),
            Aluguel(
                id=2,
                ciclista=4,
                bicicleta=5,
                trancaInicio=4,
                horaInicio=now - timedelta(hours=2),
                trancaFim=None,
                horaFim=None,
                cobranca=2
            ),
            Aluguel(
                id=3,
                ciclista=3,
                bicicleta=1,
                trancaInicio=1,
                horaInicio=now - timedelta(hours=2),
                trancaFim=2,
                horaFim=now,
                cobranca=3
            ),
        ]
        for a in alugueis:
            self.aluguel_repo.salvar(a)
