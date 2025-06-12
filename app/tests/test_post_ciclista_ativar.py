from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ativar_ciclista_sucesso():
    payload = {
        "ciclista": {
            "nome": "Clara Ativa",
            "nascimento": "1995-01-01",
            "cpf": "77777777777",
            "nacionalidade": "BRASILEIRO",
            "email": "clara@ativar.com",
            "senha": "segura123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Clara Ativa",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res = client.post("/ciclista", json=payload)
    assert res.status_code == 201
    id_ciclista = res.json()["id"]

    ativar = client.post(f"/ciclista/{id_ciclista}/ativar")
    assert ativar.status_code == 200
    assert ativar.json()["status"] == "ATIVO"

def test_ativar_ciclista_inexistente():
    res = client.post("/ciclista/99999/ativar")
    assert res.status_code == 404
    assert res.json()["mensagem"] == "Ciclista não encontrado"
