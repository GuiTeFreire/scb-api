from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_restaurar_banco():
    payload_func = {
        "nome": "Funcionario Teste",
        "idade": 30,
        "funcao": "Gerente",
        "cpf": "11111111111",
        "email": "func@test.com",
        "senha": "123456"
    }
    payload_cic = {
        "ciclista": {
            "nome": "Ciclista Teste",
            "nascimento": "1990-01-01",
            "cpf": "99999999999",
            "nacionalidade": "BRASILEIRO",
            "email": "ciclista@test.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Ciclista Teste",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_func = client.post("/funcionario", json=payload_func)
    assert res_func.status_code == 200

    res_cic = client.post("/ciclista", json=payload_cic)
    assert res_cic.status_code == 201

    assert client.get("/funcionario").status_code == 200
    assert client.get(f"/ciclista/{res_cic.json()['id']}").status_code == 200

    res_reset = client.get("/restaurarBanco")
    assert res_reset.status_code == 200
    assert res_reset.json() == {"mensagem": "Banco restaurado com sucesso"}

    res_func_list = client.get("/funcionario")
    assert res_func_list.status_code == 200
    assert res_func_list.json() == []

    res_cic_404 = client.get(f"/ciclista/{res_cic.json()['id']}")
    assert res_cic_404.status_code == 404
