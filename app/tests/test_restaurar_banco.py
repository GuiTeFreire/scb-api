import pytest
from app.use_cases.restaurar_banco import RestaurarBanco
from app.infra.repositories.fake_funcionario_repository import fake_funcionario_repository
from app.infra.repositories.fake_ciclista_repository import fake_ciclista_repository
from app.infra.repositories.fake_aluguel_repository import fake_aluguel_repository
from datetime import datetime
from app.domain.entities.funcionario import NovoFuncionario
from app.domain.entities.ciclista import Ciclista, CartaoDeCredito, StatusEnum
from app.domain.entities.aluguel import Aluguel

@pytest.fixture(autouse=True)
def reset_repos():
    fake_funcionario_repository.resetar()
    fake_ciclista_repository.resetar()
    fake_aluguel_repository.resetar()

def test_restaurar_banco():
    # Setup: Adiciona dados aos repositórios
    # Cria funcionário
    funcionario = NovoFuncionario(
        nome="Carlos Souza",
        idade=35,
        funcao="Gerente",
        cpf="12345678900",
        email="carlos@empresa.com",
        senha="123456"
    )
    fake_funcionario_repository.salvar(funcionario)
    
    # Cria ciclista
    cartao = CartaoDeCredito(
        id=1,
        nomeTitular="Ciclista Teste",
        numero="4111111111111111",
        validade=datetime(2026, 12, 1),
        cvv="123"
    )
    ciclista = Ciclista(
        id=1,
        nome="Ciclista Teste",
        nascimento=datetime(1990, 1, 1),
        cpf="12345678901",
        nacionalidade="BRASILEIRO",
        email="ciclista@teste.com",
        senha="senha123",
        urlFotoDocumento="https://teste.com/doc.png",
        status=StatusEnum.ATIVO,
        cartaoDeCredito=cartao
    )
    fake_ciclista_repository.salvar(ciclista)
    
    # Cria aluguel
    aluguel = Aluguel(
        ciclista=1,
        trancaInicio=101,
        bicicleta=5678,
        horaInicio=datetime.now(),
        trancaFim=None,
        horaFim=None,
        cobranca=10
    )
    fake_aluguel_repository.salvar(aluguel)
    
    # Verificação: Confirma que os dados foram adicionados
    assert len(fake_funcionario_repository.listar_todos()) > 0
    assert len(fake_ciclista_repository._db) > 0
    assert len(fake_aluguel_repository._db) > 0
    
    # Execução: Chama o use case RestaurarBanco
    use_case = RestaurarBanco(
        funcionario_repo=fake_funcionario_repository,
        ciclista_repo=fake_ciclista_repository,
        aluguel_repo=fake_aluguel_repository
    )
    use_case.execute()
    
    # Verificação: Confirma que todos os repositórios foram limpos
    assert len(fake_funcionario_repository.listar_todos()) == 0
    assert len(fake_ciclista_repository._db) == 0
    assert len(fake_aluguel_repository._db) == 0
