from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_email_existe_true():
    # Cadastra um ciclista com e-mail conhecido
    payload = {
        "ciclista": {
            "nome": "Teste Email",
            "nascimento": "1995-01-01",
            "cpf": "11111111111",
            "nacionalidade": "BRASILEIRO",
            "email": "email@existe.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://example.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Teste Email",
            "numero": "4111111111111111",
            "validade": "2026-12-31",
            "cvv": "123"
        }
    }

    response = client.post("/ciclista", json=payload)
    assert response.status_code == 201

    # Verifica existência
    check = client.get("/ciclista/existeEmail/email@existe.com")
    assert check.status_code == 200
    assert check.json() is True

def test_email_existe_false():
    response = client.get("/ciclista/existeEmail/email_inexistente@teste.com")
    assert response.status_code == 200
    assert response.json() is False
