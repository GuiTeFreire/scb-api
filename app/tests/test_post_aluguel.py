from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_aluguel_sucesso():
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
    assert res_aluguel.json()["ciclista"] == ciclista_id
    assert res_aluguel.json()["trancaInicio"] == 101
    assert res_aluguel.json()["horaFim"] is None


def test_aluguel_falha_com_aluguel_ativo():
    client.get("/restaurarBanco")

    payload_ciclista = {
        "ciclista": {
            "nome": "João Pedro",
            "nascimento": "1991-01-01",
            "cpf": "99999999999",
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
        "trancaInicio": 102
    }

    res1 = client.post("/aluguel", json=payload_aluguel)
    print("ERRO PRIMEIRO ALUGUEL:", res1.status_code, res1.json())
    assert res1.status_code == 200

    res2 = client.post("/aluguel", json=payload_aluguel)
    assert res2.status_code == 422

def test_aluguel_falha_ciclista_inativo():
    client.get("/restaurarBanco")

    payload_ciclista = {
        "ciclista": {
            "nome": "Carlos Inativo",
            "nascimento": "1995-01-01",
            "cpf": "88888888888",
            "nacionalidade": "BRASILEIRO",
            "email": "inativo@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Carlos Inativo",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_post = client.post("/ciclista", json=payload_ciclista)
    assert res_post.status_code == 201
    ciclista_id = res_post.json()["id"]

    payload_aluguel = {
        "ciclista": ciclista_id,
        "trancaInicio": 105
    }

    res = client.post("/aluguel", json=payload_aluguel)
    assert res.status_code == 422

def test_aluguel_falha_tranca_invalida():
    client.get("/restaurarBanco")

    payload_ciclista = {
        "ciclista": {
            "nome": "Maria Tranca Invalida",
            "nascimento": "1992-01-01",
            "cpf": "77777777777",
            "nacionalidade": "BRASILEIRO",
            "email": "tranca@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Maria Tranca Invalida",
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

    # Testar com trancaInicio = 0 (inválido)
    payload_aluguel = {
        "ciclista": ciclista_id,
        "trancaInicio": 0
    }

    res = client.post("/aluguel", json=payload_aluguel)
    assert res.status_code == 422

    # Testar com trancaInicio negativo (inválido)
    payload_aluguel = {
        "ciclista": ciclista_id,
        "trancaInicio": -1
    }

    res = client.post("/aluguel", json=payload_aluguel)
    assert res.status_code == 422