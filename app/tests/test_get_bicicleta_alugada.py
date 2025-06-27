from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_bicicleta_alugada_retorna_bicicleta_quando_ha_aluguel():
    client.get("/restaurarBanco")

    payload_ciclista = {
        "ciclista": {
            "nome": "Marcos Bicicleta",
            "nascimento": "1993-01-01",
            "cpf": "32132132100",
            "nacionalidade": "BRASILEIRO",
            "email": "marcos@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Marcos Bicicleta",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_post = client.post("/ciclista", json=payload_ciclista)
    assert res_post.status_code == 201
    ciclista_id = res_post.json()["id"]

    res_ativar = client.post(f"/ciclista/{ciclista_id}/ativar")
    assert res_ativar.status_code == 200

    # Criar aluguel
    payload_aluguel = {
        "ciclista": ciclista_id,
        "trancaInicio": 101
    }

    res_aluguel = client.post("/aluguel", json=payload_aluguel)
    assert res_aluguel.status_code == 200

    # Buscar bicicleta alugada
    res = client.get(f"/ciclista/{ciclista_id}/bicicletaAlugada")
    assert res.status_code == 200
    assert res.json()["id"] == 5678  # mock retornado pelo sistema


def test_bicicleta_alugada_retorna_null_quando_nao_ha_aluguel():
    client.get("/restaurarBanco")

    payload_ciclista = {
        "ciclista": {
            "nome": "Lúcia Livre",
            "nascimento": "1990-05-20",
            "cpf": "55555555555",
            "nacionalidade": "BRASILEIRO",
            "email": "lucia@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Lúcia Livre",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_post = client.post("/ciclista", json=payload_ciclista)
    assert res_post.status_code == 201
    ciclista_id = res_post.json()["id"]

    res_ativar = client.post(f"/ciclista/{ciclista_id}/ativar")
    assert res_ativar.status_code == 200

    res = client.get(f"/ciclista/{ciclista_id}/bicicletaAlugada")
    assert res.status_code == 200
    assert res.json() is None


def test_bicicleta_alugada_ciclista_inexistente():
    client.get("/restaurarBanco")

    res = client.get("/ciclista/9999/bicicletaAlugada")
    assert res.status_code == 404
    assert res.json()["codigo"] == "404"
