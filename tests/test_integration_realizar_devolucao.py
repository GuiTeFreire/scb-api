import pytest
import httpx

@pytest.mark.integration
class TestIntegrationRealizarDevolucao:
    BASE_URL = "https://scb-api-g8jr.onrender.com/devolucao"

    def test_realizar_devolucao_sucesso(self):
        # Pré-condição: bicicleta 3 está alugada pelo ciclista 3 e tranca 2 está disponível
        payload = {
            "idBicicleta": 3,
            "idTranca": 2
        }
        response = httpx.post(self.BASE_URL, json=payload, timeout=10)
        assert response.status_code in (200, 201)
        data = response.json()
        assert "bicicleta" in data
        assert "trancaFim" in data
        assert "horaFim" in data
        assert "cobranca" in data
        assert "ciclista" in data

    def test_realizar_devolucao_tranca_inexistente(self):
        payload = {
            "idBicicleta": 3,
            "idTranca": 99999
        }
        response = httpx.post(self.BASE_URL, json=payload, timeout=10)
        assert response.status_code == 422 or response.status_code == 404
        data = response.json()
        assert "mensagem" in data or "detail" in data

    def test_realizar_devolucao_bicicleta_nao_alugada(self):
        payload = {
            "idBicicleta": 99999,  # Bicicleta inexistente ou não alugada
            "idTranca": 2
        }
        response = httpx.post(self.BASE_URL, json=payload, timeout=10)
        assert response.status_code == 422 or response.status_code == 404
        data = response.json()
        assert "mensagem" in data or "detail" in data

    def test_realizar_devolucao_tranca_ocupada(self):
        # Pré-condição: tranca 1 já está ocupada
        payload = {
            "idBicicleta": 3,
            "idTranca": 1
        }
        response = httpx.post(self.BASE_URL, json=payload, timeout=10)
        assert response.status_code == 422 or response.status_code == 400
        data = response.json()
        assert "mensagem" in data or "detail" in data 