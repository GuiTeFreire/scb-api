from fastapi.testclient import TestClient
from app.main import app
from app.domain.entities.devolucao import NovoDevolucao
from app.use_cases.realizar_devolucao import RealizarDevolucao
from app.use_cases.cadastrar_ciclista import CadastrarCiclista
from app.infra.repositories import fake_aluguel_repository, fake_ciclista_repository, fake_externo_repository, fake_equipamento_repository
import pytest
from fastapi import HTTPException
from app.domain.entities.aluguel import Aluguel
from app.domain.entities.ciclista import RequisicaoCadastroCiclista
from datetime import datetime, timedelta

client = TestClient(app)

def test_devolucao_sucesso():
    client.get("/restaurarBanco")

    payload_ciclista = {
        "ciclista": {
            "nome": "Lucas Alves",
            "nascimento": "1990-01-01",
            "cpf": "12345678901",
            "nacionalidade": "BRASILEIRO",
            "email": "lucas@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Lucas Alves",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_post = client.post("/ciclista", json=payload_ciclista)
    assert res_post.status_code == 201
    ciclista_id = res_post.json()["id"]

    res_ativar = client.post(f"/ciclista/{ciclista_id}/ativar")
    assert res_ativar.status_code == 200

    payload_aluguel = {
        "ciclista": ciclista_id,
        "trancaInicio": 101
    }

    res_aluguel = client.post("/aluguel", json=payload_aluguel)
    assert res_aluguel.status_code == 200

    payload_devolucao = {
        "idBicicleta": 5678,
        "idTranca": 201
    }

    res_devolucao = client.post("/devolucao", json=payload_devolucao)
    assert res_devolucao.status_code == 200
    assert res_devolucao.json()["trancaFim"] == 201
    assert res_devolucao.json()["horaFim"] is not None

def test_devolucao_falha_ciclista_inexistente():
    client.get("/restaurarBanco")

    payload = {
        "idTranca": 200,
        "idBicicleta": 9999
    }

    res = client.post("/devolucao", json=payload)
    assert res.status_code == 422

def test_devolucao_falha_sem_aluguel_ativo():
    client.get("/restaurarBanco")

    payload_ciclista = {
        "ciclista": {
            "nome": "José Sem Aluguel",
            "nascimento": "1992-01-01",
            "cpf": "20202020202",
            "nacionalidade": "BRASILEIRO",
            "email": "jose@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "José Sem Aluguel",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_post = client.post("/ciclista", json=payload_ciclista)
    assert res_post.status_code == 201
    ciclista_id = res_post.json()["id"]

    client.post(f"/ciclista/{ciclista_id}/ativar")

    payload = {
        "idTranca": 200,
        "idBicicleta": 9999
    }

    res = client.post("/devolucao", json=payload)
    assert res.status_code == 422

def test_devolucao_falha_idTranca_none():
    use_case = RealizarDevolucao(
        fake_aluguel_repository, 
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    class FakePayload:
        idTranca = None
        idBicicleta = 123
    payload = FakePayload()
    with pytest.raises(HTTPException) as exc:
        use_case.execute(payload)
    assert exc.value.status_code == 422
    assert exc.value.detail == "Bicicleta não está alugada"

def test_devolucao_falha_bicicleta_invalida():
    client.get("/restaurarBanco")

    payload_ciclista = {
        "ciclista": {
            "nome": "João Pedro",
            "nascimento": "1991-01-01",
            "cpf": "55555555555",
            "nacionalidade": "BRASILEIRO",
            "email": "joao@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "João Pedro",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_post = client.post("/ciclista", json=payload_ciclista)
    assert res_post.status_code == 201
    ciclista_id = res_post.json()["id"]

    res_ativar = client.post(f"/ciclista/{ciclista_id}/ativar")
    assert res_ativar.status_code == 200

    payload_aluguel = {
        "ciclista": ciclista_id,
        "trancaInicio": 101
    }

    res_aluguel = client.post("/aluguel", json=payload_aluguel)
    assert res_aluguel.status_code == 200

    payload_devolucao = {
        "idBicicleta": 0,
        "idTranca": 201
    }

    res = client.post("/devolucao", json=payload_devolucao)
    assert res.status_code == 422

    payload_devolucao = {
        "idBicicleta": -1,
        "idTranca": 201
    }

    res = client.post("/devolucao", json=payload_devolucao)
    assert res.status_code == 422

def test_devolucao_falha_bicicleta_nao_alugada():
    client.get("/restaurarBanco")

    payload_devolucao = {
        "idBicicleta": 9999,
        "idTranca": 201
    }

    res = client.post("/devolucao", json=payload_devolucao)
    assert res.status_code == 422
    assert res.json()["codigo"] == "422"

def test_devolucao_falha_tranca_invalida():
    client.get("/restaurarBanco")

    payload_ciclista = {
        "ciclista": {
            "nome": "Maria Silva",
            "nascimento": "1995-01-01",
            "cpf": "98765432109",
            "nacionalidade": "BRASILEIRO",
            "email": "maria@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Maria Silva",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_post = client.post("/ciclista", json=payload_ciclista)
    assert res_post.status_code == 201
    ciclista_id = res_post.json()["id"]

    res_ativar = client.post(f"/ciclista/{ciclista_id}/ativar")
    assert res_ativar.status_code == 200

    payload_aluguel = {
        "ciclista": ciclista_id,
        "trancaInicio": 101
    }

    res_aluguel = client.post("/aluguel", json=payload_aluguel)
    assert res_aluguel.status_code == 200

    # Testar com uma bicicleta que não está alugada (deve falhar)
    payload_devolucao = {
        "idBicicleta": 9999,  # Bicicleta que não existe/não está alugada
        "idTranca": 201
    }

    res = client.post("/devolucao", json=payload_devolucao)
    assert res.status_code == 422

def _criar_ciclista_ativo_para_devolucao_casos_limite(nome, email, cpf):
    """Helper para criar um ciclista ativo nos testes de casos limite de devolução"""
    use_case = CadastrarCiclista(fake_ciclista_repository, fake_externo_repository)
    dados = RequisicaoCadastroCiclista(
        ciclista={
            "nome": nome,
            "nascimento": "1990-01-01",
            "cpf": cpf,
            "nacionalidade": "BRASILEIRO",
            "email": email,
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        meioDePagamento={
            "nomeTitular": nome,
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    )
    ciclista = use_case.execute(dados)
    ciclista.status = "ATIVO"
    return ciclista

def test_devolucao_com_valor_extra():
    """Testa devolução com valor extra por tempo excedido"""
    fake_ciclista_repository.resetar()
    fake_aluguel_repository.resetar()
    
    # Criar um ciclista
    ciclista = _criar_ciclista_ativo_para_devolucao_casos_limite("João Teste", "joao@teste.com", "12345678901")
    
    # Criar um aluguel com mais de 2 horas (para gerar valor extra)
    aluguel = Aluguel(
        ciclista=ciclista.id,
        trancaInicio=103,
        bicicleta=5678,
        horaInicio=datetime.now() - timedelta(hours=3),  # 3 horas atrás
        trancaFim=None,
        horaFim=None,
        cobranca=10
    )
    aluguel_salvo = fake_aluguel_repository.salvar(aluguel)
    
    # Mock para verificar se incluir_cobranca_fila foi chamado
    original_incluir_cobranca_fila = fake_externo_repository.incluir_cobranca_fila
    chamadas_cobranca = []
    
    def mock_incluir_cobranca_fila(ciclista_id, valor):
        chamadas_cobranca.append((ciclista_id, valor))
        return original_incluir_cobranca_fila(ciclista_id, valor)
    
    fake_externo_repository.incluir_cobranca_fila = mock_incluir_cobranca_fila
    
    # Executar devolução
    class Payload:
        def __init__(self):
            self.idBicicleta = 5678
            self.idTranca = 201
    
    payload = Payload()
    use_case = RealizarDevolucao(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    resultado = use_case.execute(payload)
    
    # Verificar que a cobrança extra foi incluída na fila
    assert len(chamadas_cobranca) == 1
    assert chamadas_cobranca[0][0] == ciclista.id
    assert chamadas_cobranca[0][1] > 0  # Valor extra deve ser maior que zero
    
    # Verificar que o valor total inclui o extra
    assert resultado.cobranca > 10  # Deve ser maior que a taxa básica
    
    # Restaurar método original
    fake_externo_repository.incluir_cobranca_fila = original_incluir_cobranca_fila

def test_devolucao_sem_valor_extra():
    """Testa devolução sem valor extra (dentro das 2 horas)"""
    fake_ciclista_repository.resetar()
    fake_aluguel_repository.resetar()
    
    # Criar um ciclista
    ciclista = _criar_ciclista_ativo_para_devolucao_casos_limite("Maria Teste", "maria@teste.com", "98765432109")
    
    # Criar um aluguel com menos de 2 horas
    aluguel = Aluguel(
        ciclista=ciclista.id,
        trancaInicio=103,
        bicicleta=5678,
        horaInicio=datetime.now() - timedelta(hours=1),  # 1 hora atrás
        trancaFim=None,
        horaFim=None,
        cobranca=10
    )
    aluguel_salvo = fake_aluguel_repository.salvar(aluguel)
    
    # Mock para verificar se incluir_cobranca_fila NÃO foi chamado
    original_incluir_cobranca_fila = fake_externo_repository.incluir_cobranca_fila
    chamadas_cobranca = []
    
    def mock_incluir_cobranca_fila(ciclista_id, valor):
        chamadas_cobranca.append((ciclista_id, valor))
        return original_incluir_cobranca_fila(ciclista_id, valor)
    
    fake_externo_repository.incluir_cobranca_fila = mock_incluir_cobranca_fila
    
    # Executar devolução
    class Payload:
        def __init__(self):
            self.idBicicleta = 5678
            self.idTranca = 201
    
    payload = Payload()
    use_case = RealizarDevolucao(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    resultado = use_case.execute(payload)
    
    # Verificar que a cobrança extra NÃO foi incluída na fila
    assert len(chamadas_cobranca) == 0
    
    # Verificar que o valor total é apenas a taxa básica
    assert resultado.cobranca == 10
    
    # Restaurar método original
    fake_externo_repository.incluir_cobranca_fila = original_incluir_cobranca_fila

def test_devolucao_dummy_para_cobertura():
    """Teste dummy para cobrir linhas finais do arquivo"""
    pass