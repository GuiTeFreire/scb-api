import pytest
from app.use_cases.realizar_devolucao import RealizarDevolucao
from app.infra.repositories.fake_aluguel_repository import fake_aluguel_repository
from app.infra.repositories.fake_ciclista_repository import fake_ciclista_repository
from app.infra.repositories.fake_externo_repository import fake_externo_repository
from app.infra.repositories.fake_equipamento_repository import fake_equipamento_repository
from app.domain.entities.aluguel import Aluguel
from app.domain.entities.ciclista import NovoCiclista, CartaoDeCredito, Ciclista, StatusEnum
from datetime import datetime, timedelta
from fastapi import HTTPException

@pytest.fixture(autouse=True)
def reset_repos():
    fake_ciclista_repository.resetar()
    fake_aluguel_repository.resetar()

# Função auxiliar para criar ciclistas ativos nos testes
def _criar_ciclista_ativo(nome, email, cpf):
    novo_ciclista = NovoCiclista(
        nome=nome,
        nascimento=datetime(1990, 1, 1),
        cpf=cpf,
        nacionalidade="BRASILEIRO",
        email=email,
        senha="senha123",
        urlFotoDocumento="https://site.com/doc.png"
    )
    cartao = CartaoDeCredito(
        id=1,
        nomeTitular=nome,
        numero="4111111111111111",
        validade=datetime(2026, 12, 1),
        cvv="123"
    )
    ciclista = Ciclista(
        **novo_ciclista.model_dump(),
        id=0,
        cartaoDeCredito=cartao,
        status=StatusEnum.ATIVO
    )
    return fake_ciclista_repository.salvar(ciclista)

def test_devolucao_sucesso():
    # Setup: Cria ciclista e aluguel ativo
    ciclista = _criar_ciclista_ativo("Lucas Alves", "lucas@teste.com", "12345678901")
    aluguel = Aluguel(
        ciclista=ciclista.id,
        trancaInicio=101,
        bicicleta=5678,
        horaInicio=datetime.now() - timedelta(hours=1),
        trancaFim=None,
        horaFim=None,
        cobranca=10
    )
    fake_aluguel_repository.salvar(aluguel)

    # Execução: Realiza a devolução
    use_case = RealizarDevolucao(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    class Payload:
        idBicicleta = 5678
        idTranca = 201

    resultado = use_case.execute(Payload())
    
    # Verificação: Confirma que a devolução foi realizada com sucesso
    assert resultado.trancaFim == 201
    assert resultado.horaFim is not None

def test_devolucao_falha_sem_aluguel_ativo():
    # Setup: Cria ciclista sem aluguel ativo
    ciclista = _criar_ciclista_ativo("José Sem Aluguel", "jose@teste.com", "20202020202")
    payload = type('Payload', (), {"idTranca": 200, "idBicicleta": 9999})()
    
    # Execução: Tenta devolver sem aluguel ativo
    use_case = RealizarDevolucao(
        fake_aluguel_repository, 
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    with pytest.raises(HTTPException) as exc:
        use_case.execute(payload)
    
    # Verificação: Confirma erro 422
    assert exc.value.status_code == 422

def test_devolucao_falha_bicicleta_nao_alugada():
    # Setup: Prepara payload com bicicleta não alugada
    payload = type('Payload', (), {"idTranca": 201, "idBicicleta": 9999})()
    
    # Execução: Tenta devolver bicicleta não alugada
    use_case = RealizarDevolucao(
        fake_aluguel_repository, 
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    with pytest.raises(HTTPException) as exc:
        use_case.execute(payload)
    
    # Verificação: Confirma erro esperado
    assert exc.value.status_code == 422
    assert exc.value.detail == "Bicicleta não está alugada"

def test_devolucao_falha_bicicleta_invalida():
    # Setup: Cria ciclista e aluguel ativo
    ciclista = _criar_ciclista_ativo("João Pedro", "joao@teste.com", "55555555555")
    aluguel = Aluguel(
        ciclista=ciclista.id,
        trancaInicio=101,
        bicicleta=5678,
        horaInicio=datetime.now() - timedelta(hours=1),
        trancaFim=None,
        horaFim=None,
        cobranca=10
    )
    fake_aluguel_repository.salvar(aluguel)

    # Execução: Tenta devolver com ID de bicicleta 0
    class Payload:
        idBicicleta = 0
        idTranca = 201
    use_case = RealizarDevolucao(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    with pytest.raises(HTTPException) as exc:
        use_case.execute(Payload())
    assert exc.value.status_code == 422

    # Execução: Tenta devolver com ID de bicicleta negativo
    class PayloadNeg:
        idBicicleta = -1
        idTranca = 201
    with pytest.raises(HTTPException) as exc:
        use_case.execute(PayloadNeg())
    assert exc.value.status_code == 422

def test_devolucao_falha_tranca_invalida():
    # Setup: Cria ciclista e aluguel ativo
    ciclista = _criar_ciclista_ativo("Maria Silva", "maria@teste.com", "98765432109")
    aluguel = Aluguel(
        ciclista=ciclista.id,
        trancaInicio=101,
        bicicleta=5678,
        horaInicio=datetime.now() - timedelta(hours=1),
        trancaFim=None,
        horaFim=None,
        cobranca=10
    )
    fake_aluguel_repository.salvar(aluguel)
    
    # Execução: Tenta devolver com tranca None
    class Payload:
        idBicicleta = 9999
        idTranca = None
    use_case = RealizarDevolucao(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    with pytest.raises(HTTPException) as exc:
        use_case.execute(Payload())
    
    # Verificação: Confirma erro 422
    assert exc.value.status_code == 422

def test_devolucao_com_valor_extra():
    # Setup: Cria ciclista e aluguel com tempo excedido
    ciclista = _criar_ciclista_ativo("João Teste", "joao@teste.com", "12345678901")
    aluguel = Aluguel(
        ciclista=ciclista.id,
        trancaInicio=103,
        bicicleta=5678,
        horaInicio=datetime.now() - timedelta(hours=3),
        trancaFim=None,
        horaFim=None,
        cobranca=10
    )
    fake_aluguel_repository.salvar(aluguel)
    
    # Setup: Mock para capturar chamadas de cobrança
    chamadas_cobranca = []
    original_incluir_cobranca_fila = fake_externo_repository.incluir_cobranca_fila
    def mock_incluir_cobranca_fila(ciclista_id, valor):
        chamadas_cobranca.append((ciclista_id, valor))
        return original_incluir_cobranca_fila(ciclista_id, valor)
    fake_externo_repository.incluir_cobranca_fila = mock_incluir_cobranca_fila
    
    # Execução: Realiza devolução com tempo excedido
    class Payload:
        idBicicleta = 5678
        idTranca = 201
    use_case = RealizarDevolucao(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    resultado = use_case.execute(Payload())
    
    # Verificação: Confirma que cobrança extra foi gerada
    assert len(chamadas_cobranca) == 1
    assert chamadas_cobranca[0][0] == ciclista.id
    assert chamadas_cobranca[0][1] > 0
    assert resultado.cobranca > 10
    
    # Cleanup: Restaura método original
    fake_externo_repository.incluir_cobranca_fila = original_incluir_cobranca_fila

def test_devolucao_sem_valor_extra():
    # Setup: Cria ciclista e aluguel sem tempo excedido
    ciclista = _criar_ciclista_ativo("Maria Teste", "maria@teste.com", "98765432109")
    aluguel = Aluguel(
        ciclista=ciclista.id,
        trancaInicio=103,
        bicicleta=5678,
        horaInicio=datetime.now() - timedelta(hours=1),
        trancaFim=None,
        horaFim=None,
        cobranca=10
    )
    fake_aluguel_repository.salvar(aluguel)
    
    # Setup: Mock para capturar chamadas de cobrança
    chamadas_cobranca = []
    original_incluir_cobranca_fila = fake_externo_repository.incluir_cobranca_fila
    def mock_incluir_cobranca_fila(ciclista_id, valor):
        chamadas_cobranca.append((ciclista_id, valor))
        return original_incluir_cobranca_fila(ciclista_id, valor)
    fake_externo_repository.incluir_cobranca_fila = mock_incluir_cobranca_fila
    
    # Execução: Realiza devolução sem tempo excedido
    class Payload:
        idBicicleta = 5678
        idTranca = 201
    use_case = RealizarDevolucao(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    resultado = use_case.execute(Payload())
    
    # Verificação: Confirma que não houve cobrança extra
    assert len(chamadas_cobranca) == 0
    assert resultado.cobranca == 10
    
    # Cleanup: Restaura método original
    fake_externo_repository.incluir_cobranca_fila = original_incluir_cobranca_fila
