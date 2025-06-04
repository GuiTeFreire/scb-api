from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def build_payload(cpf=None, passaporte=None, email="user@regra.com", numero="4111111111111111"):
    ciclista = {
        "nome": "Regra de Negócio",
        "nascimento": "1990-05-10",
        "nacionalidade": "BRASILEIRO",
        "email": email,
        "senha": "senhaSegura",
        "urlFotoDocumento": "https://example.com/doc.png"
    }
    if cpf:
        ciclista["cpf"] = cpf
    if passaporte:
        ciclista["passaporte"] = passaporte

    return {
        "ciclista": ciclista,
        "meioDePagamento": {
            "nomeTitular": "Regra de Negócio",
            "numero": numero,
            "validade": "2026-10-01",
            "cvv": "123"
        }
    }

def test_erro_cpf_e_passaporte_ao_mesmo_tempo():
    passaporte = {"numero": "XPTO999", "validade": "2031-01-01", "pais": "US"}
    payload = build_payload(cpf="12345678900", passaporte=passaporte, email="duplo@regra.com")
    response = client.post("/ciclista", json=payload)
    assert response.status_code == 422

def test_erro_sem_cpf_e_sem_passaporte():
    payload = build_payload(cpf=None, passaporte=None, email="vazio@regra.com")
    response = client.post("/ciclista", json=payload)
    assert response.status_code == 422

def test_erro_email_duplicado():
    # 1ª vez deve funcionar
    payload = build_payload(cpf="98765432100", email="duplicado@regra.com")
    response1 = client.post("/ciclista", json=payload)
    assert response1.status_code == 201

    # 2ª vez com mesmo e-mail
    response2 = client.post("/ciclista", json=payload)
    assert response2.status_code == 422

def test_erro_cartao_numero_invalido():
    payload = build_payload(cpf="12312312399", email="cartao@regra.com", numero="abcdefg")
    response = client.post("/ciclista", json=payload)
    assert response.status_code == 422
    # O erro será lançado pelo validador de tipos Pydantic para 'numero'
