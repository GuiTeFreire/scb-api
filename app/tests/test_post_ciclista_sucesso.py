from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def build_payload(cpf=None, passaporte=None, email="user@sucesso.com"):
    ciclista = {
        "nome": "Usuário Sucesso",
        "nascimento": "1985-07-20",
        "nacionalidade": "BRASILEIRO",
        "email": email,
        "senha": "senha123",
        "urlFotoDocumento": "https://example.com/foto.png"
    }
    if cpf:
        ciclista["cpf"] = cpf
    if passaporte:
        ciclista["passaporte"] = passaporte

    return {
        "ciclista": ciclista,
        "meioDePagamento": {
            "nomeTitular": "Usuário Sucesso",
            "numero": "4111111111111111",
            "validade": "2026-10-01",
            "cvv": "123"
        }
    }

def test_cadastro_ciclista_brasileiro_com_sucesso():
    payload = build_payload(cpf="12345678901", email="brasileiro@sucesso.com")
    response = client.post("/ciclista", json=payload)
    assert response.status_code == 201
    assert response.json()["email"] == "brasileiro@sucesso.com"
    assert response.json()["status"] == "AGUARDANDO_CONFIRMACAO"
    assert "senha" not in response.json()

def test_cadastro_ciclista_estrangeiro_com_sucesso():
    passaporte = {"numero": "XPT123", "validade": "2030-12-31", "pais": "US"}
    payload = build_payload(passaporte=passaporte, email="estrangeiro@sucesso.com")
    response = client.post("/ciclista", json=payload)
    assert response.status_code == 201
    assert response.json()["email"] == "estrangeiro@sucesso.com"
    assert response.json()["status"] == "AGUARDANDO_CONFIRMACAO"
    assert "senha" not in response.json()