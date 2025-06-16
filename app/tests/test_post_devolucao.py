from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_devolucao_sucesso():
    client.get("/restaurarBanco")

    # Cadastrar ciclista
    payload_ciclista = {
        "ciclista": {
            "nome": "Maria Devolve",
            "nascimento": "1990-01-01",
            "cpf": "10101010101",
            "nacionalidade": "BRASILEIRO",
            "email": "maria@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Maria Devolve",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_post = client.post("/ciclista", json=payload_ciclista)
    assert res_post.status_code == 201
    ciclista_id = res_post.json()["id"]

    client.post(f"/ciclista/{ciclista_id}/ativar")

    # Criar aluguel
    payload_aluguel = {
        "ciclista": ciclista_id,
        "trancaInicio": 103
    }
    res_aluguel = client.post("/aluguel", json=payload_aluguel)
    assert res_aluguel.status_code == 200

    # Realizar devolução
    payload_devolucao = {
        "ciclista": ciclista_id,
        "trancaFim": 201
    }
    res_devolucao = client.post("/devolucao", json=payload_devolucao)
    assert res_devolucao.status_code == 200
    body = res_devolucao.json()
    assert body["ciclista"] == ciclista_id
    assert body["trancaFim"] == 201
    assert body["horaFim"] is not None


def test_devolucao_falha_ciclista_inexistente():
    client.get("/restaurarBanco")

    payload = {
        "ciclista": 9999,
        "trancaFim": 200
    }

    res = client.post("/devolucao", json=payload)
    assert res.status_code == 422
    assert res.json()["mensagem"][0]["mensagem"] == "Ciclista inválido ou inativo"


def test_devolucao_falha_sem_aluguel_ativo():
    client.get("/restaurarBanco")

    # Cadastrar ciclista
    payload_ciclista = {
        "ciclista": {
            "nome": "José Sem Aluguel",
            "nascimento": "1992-01-01",
            "cpf": "20202020202",
            "nacionalidade": "BRASILEIRO",
            "email": "jose@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "José Sem Aluguel",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_post = client.post("/ciclista", json=payload_ciclista)
    assert res_post.status_code == 201
    ciclista_id = res_post.json()["id"]

    client.post(f"/ciclista/{ciclista_id}/ativar")

    payload = {
        "ciclista": ciclista_id,
        "trancaFim": 200
    }

    res = client.post("/devolucao", json=payload)
    assert res.status_code == 422
    assert res.json()["mensagem"][0]["mensagem"] == "Ciclista não possui aluguel ativo"
