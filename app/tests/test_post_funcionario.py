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

def test_post_funcionario_falha_email_duplicado():
    client.get("/restaurarBanco")
    
    payload = {
        "nome": "João Silva",
        "idade": 30,
        "funcao": "Atendente",
        "cpf": "11111111111",
        "email": "joao@empresa.com",
        "documento": "RG111111",
        "senha": "123456"
    }

    res1 = client.post("/funcionario", json=payload)
    assert res1.status_code == 200

    res2 = client.post("/funcionario", json=payload)
    assert res2.status_code == 422
    assert res2.json()["mensagem"] == "E-mail já cadastrado"
