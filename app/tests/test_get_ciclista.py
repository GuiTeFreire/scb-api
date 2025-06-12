from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_ciclista_sucesso():
    payload = {
        "ciclista": {
            "nome": "Maria Teste",
            "nascimento": "1995-06-01",
            "cpf": "12345678900",
            "nacionalidade": "BRASILEIRO",
            "email": "maria@get.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://foto.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Maria Teste",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res = client.post("/ciclista", json=payload)
    assert res.status_code == 201
    ciclista = res.json()

    get_res = client.get(f"/ciclista/{ciclista['id']}")
    assert get_res.status_code == 200

    resposta = get_res.json()
    assert resposta["id"] == ciclista["id"]
    assert resposta["email"] == "maria@get.com"
    assert "senha" not in resposta  # Garante que senha não vaza

def test_get_ciclista_nao_encontrado():
    res = client.get("/ciclista/99999")
    assert res.status_code == 404
