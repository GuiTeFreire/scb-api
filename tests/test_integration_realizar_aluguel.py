import pytest
import httpx

@pytest.mark.integration
class TestIntegrationRealizarAluguel:
    BASE_URL = "http://localhost:8000/aluguel"

    def test_realizar_aluguel_sucesso(self):
        payload = {
            "ciclista": 1,
            "trancaInicio": 2
        }
        response = httpx.post(self.BASE_URL, json=payload, timeout=10)
        assert response.status_code in (200, 201)
        data = response.json()
        assert "bicicleta" in data
        assert "trancaInicio" in data
        assert "horaInicio" in data
        assert "cobranca" in data
        assert "ciclista" in data

    def test_realizar_aluguel_tranca_inexistente(self):
        payload = {
            "ciclista": 1,
            "trancaInicio": 99999
        }
        response = httpx.post(self.BASE_URL, json=payload, timeout=10)
        assert response.status_code == 422 or response.status_code == 404
        data = response.json()
        assert "mensagem" in data or "detail" in data

    def test_realizar_aluguel_ciclista_inexistente(self):
        payload = {
            "ciclista": 99999,
            "trancaInicio": 2
        }
        response = httpx.post(self.BASE_URL, json=payload, timeout=10)
        assert response.status_code == 422 or response.status_code == 404
        data = response.json()
        assert "mensagem" in data or "detail" in data

    def test_realizar_aluguel_tranca_ocupada(self):
        # Pré-condição: tranca 2 deve estar OCUPADA (já com bicicleta)
        payload = {
            "ciclista": 1,
            "trancaInicio": 2
        }
        # Primeiro aluguel para ocupar a tranca
        httpx.post(self.BASE_URL, json=payload, timeout=10)
        # Segundo aluguel deve falhar
        response = httpx.post(self.BASE_URL, json=payload, timeout=10)
        assert response.status_code == 422 or response.status_code == 400
        data = response.json()
        assert "mensagem" in data or "detail" in data

    def test_realizar_aluguel_ciclista_com_aluguel_ativo(self):
        # Pré-condição: ciclista 1 já tem aluguel ativo
        payload = {
            "ciclista": 1,
            "trancaInicio": 3
        }
        response = httpx.post(self.BASE_URL, json=payload, timeout=10)
        assert response.status_code == 422 or response.status_code == 400
        data = response.json()
        assert "mensagem" in data or "detail" in data

    def test_realizar_aluguel_falha_cobranca(self):
        # Pré-condição: ciclista 2 tem cartão inválido
        payload = {
            "ciclista": 2,
            "trancaInicio": 4
        }
        response = httpx.post(self.BASE_URL, json=payload, timeout=10)
        assert response.status_code == 422 or response.status_code == 400
        data = response.json()
        assert "mensagem" in data or "detail" in data 