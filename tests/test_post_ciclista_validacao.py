from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def build_payload(cpf=None, passaporte=None, email="teste@example.com", numero_cartao="4111111111111111"):
    ciclista = {
        "nome": "Fulano",
        "nascimento": "1990-01-01",
        "nacionalidade": "BRASILEIRO",
        "email": email,
        "senha": "senha123",
        "urlFotoDocumento": "https://example.com/doc.png"
    }
    if cpf:
        ciclista["cpf"] = cpf
    if passaporte:
        ciclista["passaporte"] = passaporte

    return {
        "ciclista": ciclista,
        "meioDePagamento": {
            "nomeTitular": "Fulano",
            "numero": numero_cartao,
            "validade": "2026-12-31",
            "cvv": "123"
        }
    }

def test_email_invalido():
    payload = build_payload(cpf="12345678901", email="invalid-email")
    response = client.post("/ciclista", json=payload)
    assert response.status_code == 422

def test_cpf_e_passaporte_informados():
    payload = build_payload(
        cpf="12345678901",
        passaporte={"numero": "123", "validade": "2030-01-01", "pais": "PT"}
    )
    response = client.post("/ciclista", json=payload)
    assert response.status_code == 422

def test_ausencia_de_cpf_e_passaporte():
    payload = build_payload()
    response = client.post("/ciclista", json=payload)
    assert response.status_code == 422

def test_email_duplicado():
    payload = build_payload(cpf="12345678901", email="joao@duplicado.com")
    # Primeiro cadastro
    client.post("/ciclista", json=payload)
    # Segundo com mesmo email
    response = client.post("/ciclista", json=payload)
    assert response.status_code == 422

def test_numero_cartao_invalido():
    payload = build_payload(cpf="12345678901", numero_cartao="abcd1234")
    response = client.post("/ciclista", json=payload)
    assert response.status_code == 422
