import os
import httpx
from app.domain.repositories.externo_repository import ExternoRepository

class HttpExternoRepository(ExternoRepository):
    def __init__(self):
        self.base_url = os.getenv("EXTERNO_URL", "http://localhost:8002")

    def validar_cartao_credito(self, cartao_data):
        response = httpx.post(f"{self.base_url}/validaCartaoDeCredito", json=cartao_data)
        if response.status_code == 200:
            return {"valido": True}
        elif response.status_code == 422 and response.text:
            return response.json()
        else:
            print("[ERRO] Resposta inesperada do serviço externo:", response.status_code, response.text)
            return {"valido": False, "mensagem": "Resposta inesperada do serviço externo"}

    def realizar_cobranca(self, ciclista_id, valor):
        payload = {"ciclista": ciclista_id, "valor": valor}
        response = httpx.post(f"{self.base_url}/cobranca", json=payload)
        return response.json()

    def incluir_cobranca_fila(self, ciclista_id, valor):
        payload = {"ciclista": ciclista_id, "valor": valor}
        response = httpx.post(f"{self.base_url}/filaCobranca", json=payload)
        return response.json()

    def enviar_email(self, email, assunto, mensagem):
        payload = {"email": email, "assunto": assunto, "mensagem": mensagem}
        response = httpx.post(f"{self.base_url}/enviarEmail", json=payload)
        return response.json()

    def restaurar_dados(self):
        response = httpx.get(f"{self.base_url}/restaurarDados")
        return response.status_code == 200 