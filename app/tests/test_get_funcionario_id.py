from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_funcionario_por_id_sucesso():
    client.get("/restaurarBanco")

    payload = {
        "nome": "Joana Silva",
        "idade": 40,
        "funcao": "Técnico",
        "cpf": "22222222222",
        "email": "joana@empresa.com",
        "senha": "senha456"
    }

    res = client.post("/funcionario", json=payload)
    assert res.status_code == 200
    matricula = res.json()["matricula"]

    res_get = client.get(f"/funcionario/{matricula}")
    assert res_get.status_code == 200
    funcionario = res_get.json()
    assert funcionario["email"] == "joana@empresa.com"
    assert funcionario["nome"] == "Joana Silva"
    assert funcionario["cpf"] == "22222222222"

def test_get_funcionario_por_id_inexistente():
    client.get("/restaurarBanco")

    res_get = client.get("/funcionario/9999")
    assert res_get.status_code == 404
    assert res_get.json().get("mensagem") == "Funcionário não encontrado"
