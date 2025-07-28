import pytest
from app.infra.repositories.http_equipamento_repository import HttpEquipamentoRepository
from app.infra.repositories.http_externo_repository import HttpExternoRepository
import httpx

@pytest.fixture(scope="session", autouse=True)
def restaurar_todos_os_dados():
    # Chama o endpoint do microsserviço principal diretamente
    try:
        response = httpx.get("https://scb-api-g8jr.onrender.com/restaurarDados", timeout=10)
        assert response.status_code == 200, f"Falha ao restaurar dados no principal: {response.text}"
    except Exception as e:
        print(f"[ERRO] Não foi possível restaurar dados no principal: {e}")

    # Chama os métodos dos repositórios reais
    equipamento_repo = HttpEquipamentoRepository()
    externo_repo = HttpExternoRepository()
    try:
        assert equipamento_repo.restaurar_dados(), "Falha ao restaurar dados no microsserviço de equipamento"
    except Exception as e:
        print(f"[ERRO] Não foi possível restaurar dados no equipamento: {e}")
    try:
        assert externo_repo.restaurar_dados(), "Falha ao restaurar dados no microsserviço externo"
    except Exception as e:
        print(f"[ERRO] Não foi possível restaurar dados no externo: {e}")
    yield 