from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_permite_aluguel_retorna_true_quando_nao_tem_aluguel_ativo():
    client.get("/restaurarBanco")

    payload = {
        "ciclista": {
            "nome": "Maria Silva",
            "nascimento": "1995-01-01",
            "cpf": "12345678901",
            "nacionalidade": "BRASILEIRO",
            "email": "maria@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Maria Silva",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_post = client.post("/ciclista", json=payload)
    assert res_post.status_code == 201
    id_ciclista = res_post.json()["id"]

    res_ativar = client.post(f"/ciclista/{id_ciclista}/ativar")
    assert res_ativar.status_code == 200

    res = client.get(f"/ciclista/{id_ciclista}/permiteAluguel")
    assert res.status_code == 200
    assert res.json() is True

def test_permite_aluguel_404_para_ciclista_inexistente():
    client.get("/restaurarBanco")

    res = client.get("/ciclista/9999/permiteAluguel")
    assert res.status_code == 404

def test_permite_aluguel_retorna_false_para_ciclista_inativo():
    client.get("/restaurarBanco")

    payload = {
        "ciclista": {
            "nome": "Maria Silva",
            "nascimento": "1995-01-01",
            "cpf": "12345678901",
            "nacionalidade": "BRASILEIRO",
            "email": "maria@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Maria Silva",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_post = client.post("/ciclista", json=payload)
    assert res_post.status_code == 201
    id_ciclista = res_post.json()["id"]

    res = client.get(f"/ciclista/{id_ciclista}/permiteAluguel")
    assert res.status_code == 200
    assert res.json() is False