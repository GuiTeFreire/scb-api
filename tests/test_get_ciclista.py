from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_ciclista_existente():
    # Primeiro cria um ciclista
    payload = {
        "ciclista": {
            "nome": "Carlos Teste",
            "nascimento": "1990-01-01",
            "cpf": "99999999999",
            "nacionalidade": "BRASILEIRO",
            "email": "carlos@example.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://example.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Carlos Teste",
            "numero": "4111111111111111",
            "validade": "2026-10-01",
            "cvv": "123"
        }
    }

    post_response = client.post("/ciclista", json=payload)
    assert post_response.status_code == 201
    id_ciclista = post_response.json()["id"]

    # Busca pelo ciclista recém-criado
    get_response = client.get(f"/ciclista/{id_ciclista}")
    assert get_response.status_code == 200
    assert get_response.json()["email"] == "carlos@example.com"

def test_get_ciclista_inexistente():
    response = client.get("/ciclista/99999")
    assert response.status_code == 404
