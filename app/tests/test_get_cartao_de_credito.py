from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_cartao_credito_sucesso():
    client.get("/restaurarBanco")

    payload = {
        "ciclista": {
            "nome": "Carlos",
            "nascimento": "1980-01-01",
            "cpf": "12345678901",
            "nacionalidade": "BRASILEIRO",
            "email": "carlos@bike.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://foto.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Carlos",
            "numero": "4111111111111111",
            "validade": "2026-10-01",
            "cvv": "123"
        }
    }

    res = client.post("/ciclista", json=payload)
    assert res.status_code == 201
    id_ciclista = res.json()["id"]

    res_get = client.get(f"/cartaoDeCredito/{id_ciclista}")
    assert res_get.status_code == 200
    assert res_get.json()["nomeTitular"] == "Carlos"

def test_get_cartao_credito_erro_ciclista_nao_encontrado():
    client.get("/restaurarBanco")

    res_get = client.get("/cartaoDeCredito/999")
    assert res_get.status_code == 404

def test_get_cartao_credito_id_invalido():
    res = client.get("/cartaoDeCredito/abc")
    assert res.status_code == 422