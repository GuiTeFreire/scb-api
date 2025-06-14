from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_atualizar_cartao_com_sucesso():
    client.get("/restaurarBanco")
    payload = {
        "ciclista": {
            "nome": "Cartão Update",
            "nascimento": "1990-01-01",
            "cpf": "88888888888",
            "nacionalidade": "BRASILEIRO",
            "email": "update@cartao.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Cartão Update",
            "numero": "4111111111111111",
            "validade": "2026-10-01",
            "cvv": "123"
        }
    }

    res = client.post("/ciclista", json=payload)
    id_ciclista = res.json()["id"]

    update = {
        "nomeTitular": "Nome Atualizado",
        "numero": "4222222222222",
        "validade": "2027-01-01",
        "cvv": "456"
    }

    res = client.put(f"/cartaoDeCredito/{id_ciclista}", json=update)
    assert res.status_code == 200

def test_atualizar_cartao_ciclista_inexistente():
    client.get("/restaurarBanco")

    update = {
        "nomeTitular": "Inexistente",
        "numero": "4000000000000",
        "validade": "2027-01-01",
        "cvv": "123"
    }

    res = client.put("/cartaoDeCredito/999", json=update)
    assert res.status_code == 404
