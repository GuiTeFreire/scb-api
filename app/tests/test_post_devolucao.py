from fastapi.testclient import TestClient
from app.main import app
from app.domain.entities.devolucao import NovoDevolucao
from app.use_cases.realizar_devolucao import RealizarDevolucao
from app.infra.repositories import fake_aluguel_repository, fake_ciclista_repository
import pytest
from fastapi import HTTPException

client = TestClient(app)

def test_devolucao_sucesso():
    client.get("/restaurarBanco")

    payload_ciclista = {
        "ciclista": {
            "nome": "Maria Devolve",
            "nascimento": "1990-01-01",
            "cpf": "10101010101",
            "nacionalidade": "BRASILEIRO",
            "email": "maria@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Maria Devolve",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_post = client.post("/ciclista", json=payload_ciclista)
    assert res_post.status_code == 201
    ciclista_id = res_post.json()["id"]

    client.post(f"/ciclista/{ciclista_id}/ativar")

    payload_aluguel = {
        "ciclista": ciclista_id,
        "trancaInicio": 103
    }
    res_aluguel = client.post("/aluguel", json=payload_aluguel)
    assert res_aluguel.status_code == 200

    payload_devolucao = {
        "idTranca": 201,
        "idBicicleta": res_aluguel.json()["bicicleta"]
    }
    res_devolucao = client.post("/devolucao", json=payload_devolucao)
    assert res_devolucao.status_code == 200
    body = res_devolucao.json()
    assert body["trancaFim"] == 201
    assert body["bicicleta"] == res_aluguel.json()["bicicleta"]
    assert body["horaFim"] is not None


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
    use_case = RealizarDevolucao(fake_aluguel_repository, fake_ciclista_repository)
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
            "nome": "João Bicicleta Invalida",
            "nascimento": "1993-01-01",
            "cpf": "66666666666",
            "nacionalidade": "BRASILEIRO",
            "email": "bicicleta@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "João Bicicleta Invalida",
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

    payload_devolucao = {
        "idTranca": 201,
        "idBicicleta": 0
    }

    res = client.post("/devolucao", json=payload_devolucao)
    assert res.status_code == 422

    payload_devolucao = {
        "idTranca": 201,
        "idBicicleta": -1
    }

    res = client.post("/devolucao", json=payload_devolucao)
    assert res.status_code == 422