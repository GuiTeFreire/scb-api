from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_editar_funcionario_com_sucesso():
    client.get("/restaurarBanco")
    payload = {
        "nome": "Amanda Rocha",
        "idade": 28,
        "funcao": "Analista",
        "cpf": "55555555555",
        "email": "amanda@empresa.com",
        "senha": "123456"
    }
    res = client.post("/funcionario", json=payload)
    assert res.status_code == 200
    matricula = res.json()["matricula"]

    update_payload = {
        "nome": "Amanda Silva",
        "idade": 29,
        "funcao": "Coordenadora",
        "cpf": "55555555555",
        "email": "amanda.silva@empresa.com",
        "senha": "novaSenha"
    }

    res_put = client.put(f"/funcionario/{matricula}", json=update_payload)
    assert res_put.status_code == 200
    assert res_put.json()["nome"] == "Amanda Silva"
    assert res_put.json()["email"] == "amanda.silva@empresa.com"

def test_editar_funcionario_inexistente():
    client.get("/restaurarBanco")
    payload = {
        "nome": "Qualquer",
        "idade": 40,
        "funcao": "Zelador",
        "cpf": "00000000000",
        "email": "naoexiste@teste.com",
        "senha": "invalido"
    }
    res = client.put("/funcionario/999", json=payload)
    assert res.status_code == 404
    assert res.json()["mensagem"] == "Funcionário não encontrado"
