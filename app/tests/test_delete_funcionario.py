from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_remover_funcionario_sucesso():
    client.get("/restaurarBanco")

    payload = {
        "nome": "Henrique Lopes",
        "idade": 45,
        "funcao": "Supervisor",
        "cpf": "99988877766",
        "email": "henrique@empresa.com",
        "senha": "senha456"
    }

    res_post = client.post("/funcionario", json=payload)
    assert res_post.status_code == 200
    matricula = res_post.json()["matricula"]

    res_delete = client.delete(f"/funcionario/{matricula}")
    assert res_delete.status_code == 200
    assert res_delete.json() == {"mensagem": "Funcionário removido com sucesso"}

    res_get = client.get(f"/funcionario/{matricula}")
    assert res_get.status_code == 404

def test_remover_funcionario_inexistente():
    client.get("/restaurarBanco")

    res = client.delete("/funcionario/9999")
    assert res.status_code == 404
    assert res.json().get("mensagem") == "Funcionário não encontrado"