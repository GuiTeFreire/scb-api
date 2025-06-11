from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_edicao_ciclista_com_sucesso():
    payload = {
        "ciclista": {
            "nome": "Ana Original",
            "nascimento": "1992-03-10",
            "cpf": "12345678901",
            "nacionalidade": "BRASILEIRO",
            "email": "ana@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://example.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Ana Original",
            "numero": "4111111111111111",
            "validade": "2026-10-01",
            "cvv": "123"
        }
    }

    post_resp = client.post("/ciclista", json=payload)
    assert post_resp.status_code == 201
    id_ciclista = post_resp.json()["id"]

    novo_dados = {
        "nome": "Ana Editada",
        "nascimento": "1992-03-10",
        "cpf": "12345678901",
        "nacionalidade": "BRASILEIRO",
        "email": "ana-editada@teste.com",
        "urlFotoDocumento": "https://example.com/doc-novo.png"
    }

    put_resp = client.put(f"/ciclista/{id_ciclista}", json=novo_dados)
    assert put_resp.status_code == 200
    assert put_resp.json()["nome"] == "Ana Editada"
    assert put_resp.json()["email"] == "ana-editada@teste.com"
    assert "senha" not in put_resp.json()

def test_edicao_ciclista_inexistente():
    payload = {
        "nome": "Fulano",
        "nascimento": "2000-01-01",
        "cpf": "11111111111",
        "nacionalidade": "BRASILEIRO",
        "email": "fulano@teste.com"
    }

    response = client.put("/ciclista/99999", json=payload)
    assert response.status_code == 404

def test_edicao_ciclista_com_cpf_e_passaporte():
    payload_cadastro = {
        "ciclista": {
            "nome": "Fulano",
            "nascimento": "1990-01-01",
            "cpf": "88888888888",
            "nacionalidade": "BRASILEIRO",
            "email": "duplicado@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://example.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Fulano",
            "numero": "4111111111111111",
            "validade": "2026-10-01",
            "cvv": "123"
        }
    }

    response_post = client.post("/ciclista", json=payload_cadastro)
    assert response_post.status_code == 201
    id_ciclista = response_post.json()["id"]

    payload_edicao = {
        "nome": "Fulano",
        "nascimento": "1990-01-01",
        "cpf": "88888888888",
        "passaporte": {
            "numero": "XP123456",
            "validade": "2030-01-01",
            "pais": "US"
        },
        "nacionalidade": "ESTRANGEIRO",
        "email": "duplicado@teste.com",
        "urlFotoDocumento": "https://example.com/doc2.png"
    }

    response_put = client.put(f"/ciclista/{id_ciclista}", json=payload_edicao)
    assert response_put.status_code == 422
