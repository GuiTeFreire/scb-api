from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_listar_funcionarios_vazio():
    client.get("/restaurarBanco")

    res = client.get("/funcionario")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) == 0

def test_listar_funcionarios_apos_cadastro():
    client.get("/restaurarBanco")

    payload = {
        "nome": "Ana Pereira",
        "idade": 28,
        "funcao": "Atendente",
        "cpf": "33333333333",
        "email": "ana@empresa.com",
        "senha": "senha456"
    }

    res_post = client.post("/funcionario", json=payload)
    assert res_post.status_code == 200

    res = client.get("/funcionario")
    assert res.status_code == 200
    funcionarios = res.json()
    assert isinstance(funcionarios, list)
    assert any(f["email"] == "ana@empresa.com" for f in funcionarios)
