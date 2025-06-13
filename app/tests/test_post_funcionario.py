from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_post_funcionario_sucesso():
    payload = {
        "nome": "Carlos Souza",
        "idade": 35,
        "funcao": "Gerente",
        "cpf": "12345678900",
        "email": "carlos@empresa.com",
        "documento": "RG123456",
        "senha": "123456"
    }

    res = client.post("/funcionario", json=payload)
    assert res.status_code == 200
    body = res.json()
    assert body["nome"] == "Carlos Souza"
    assert "matricula" in body
