from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_restaurar_banco_endpoint():
    response = client.get("/restaurarBanco")
    assert response.status_code == 200
    assert "mensagem" in response.json()
    assert "restaurado" in response.json()["mensagem"].lower()

def test_restaurar_dados_endpoint():
    response = client.get("/restaurarDados")
    assert response.status_code == 200
    assert "mensagem" in response.json()
    assert "restaurados" in response.json()["mensagem"].lower() 