from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_listar_funcionarios_vazio():
    """Deve retornar lista vazia inicialmente"""
    res = client.get("/funcionario")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) == 0


def test_listar_funcionarios_com_dados():
    """Após cadastrar um funcionário, ele deve aparecer na listagem"""
    payload = {
        "nome": "Carlos Souza",
        "idade": 35,
        "funcao": "Gerente",
        "cpf": "12345678900",
        "email": "carlos@empresa.com",
        "senha": "123456"
    }

    res_post = client.post("/funcionario", json=payload)
    assert res_post.status_code == 200

    res = client.get("/funcionario")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(f["email"] == "carlos@empresa.com" for f in data)
