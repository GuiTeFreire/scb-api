import pytest
import httpx
from datetime import date

@pytest.mark.integration
class TestIntegrationCadastrarCiclista:
    BASE_URL = "http://localhost:8000/ciclista"

    def test_cadastro_ciclista_sucesso(self):
        payload = {
            "ciclista": {
                "nome": "Fulano Integracao",
                "nascimento": "1990-01-01",
                "cpf": "12345678901",
                "nacionalidade": "Brasileiro",
                "email": "integracao_sucesso@example.com",
                "senha": "ABC123"
            },
            "meioDePagamento": {
                "nomeTitular": "Fulano Integracao",
                "numero": "4012001037141112",
                "validade": "12/2030",
                "cvv": "123"
            }
        }
        response = httpx.post(self.BASE_URL, json=payload, timeout=10)
        assert response.status_code in (200, 201)
        data = response.json()
        assert "id" in data
        assert data["email"] == payload["ciclista"]["email"]

    def test_cadastro_ciclista_cartao_invalido(self):
        payload = {
            "ciclista": {
                "nome": "Fulano Integracao",
                "nascimento": "1990-01-01",
                "cpf": "12345678902",
                "nacionalidade": "Brasileiro",
                "email": "integracao_falha@example.com",
                "senha": "ABC123"
            },
            "meioDePagamento": {
                "nomeTitular": "Fulano Integracao",
                "numero": "0000000000000000",  # Cartão inválido
                "validade": "12/2030",
                "cvv": "123"
            }
        }
        response = httpx.post(self.BASE_URL, json=payload, timeout=10)
        # Espera-se erro de validação do cartão
        assert response.status_code == 422 or response.status_code == 400
        data = response.json()
        assert "mensagem" in data or "detail" in data 