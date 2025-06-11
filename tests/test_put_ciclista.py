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
