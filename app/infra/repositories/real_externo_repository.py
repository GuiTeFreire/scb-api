import httpx
from typing import Dict, Any
from datetime import datetime
from app.domain.repositories.externo_repository import ExternoRepository
from app.config.integration_config import IntegrationConfig

# Implementação real para serviços externos
class RealExternoRepository(ExternoRepository):
    def __init__(self):
        self.config = IntegrationConfig.get_external_service_config()
    
    def validar_cartao_credito(self, cartao_data: Dict[str, Any]) -> Dict[str, Any]:
        # Valida cartão de crédito no microsserviço externo
        try:
            with httpx.Client(timeout=self.config["timeout"]) as client:
                response = client.post(
                    f"{self.config['base_url']}/validaCartaoDeCredito",
                    json=cartao_data,
                    headers=self.config["headers"]
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "valido": False,
                "mensagem": f"Erro na validação: {e.response.status_code}"
            }
        except Exception as e:
            return {
                "valido": False,
                "mensagem": f"Erro de conexão: {str(e)}"
            }
    
    def realizar_cobranca(self, ciclista_id: int, valor: float) -> Dict[str, Any]:
        # Realiza cobrança no microsserviço externo
        try:
            with httpx.Client(timeout=self.config["timeout"]) as client:
                response = client.post(
                    f"{self.config['base_url']}/cobranca",
                    json={
                        "ciclista": ciclista_id,
                        "valor": valor
                    },
                    headers=self.config["headers"]
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "id_cobranca": None,
                "status": "FALHA",
                "valor": valor,
                "ciclista_id": ciclista_id,
                "data_cobranca": datetime.now().isoformat(),
                "erro": f"Erro HTTP: {e.response.status_code}"
            }
        except Exception as e:
            return {
                "id_cobranca": None,
                "status": "FALHA",
                "valor": valor,
                "ciclista_id": ciclista_id,
                "data_cobranca": datetime.now().isoformat(),
                "erro": f"Erro de conexão: {str(e)}"
            }
    
    def incluir_cobranca_fila(self, ciclista_id: int, valor: float) -> Dict[str, Any]:
        # Inclui cobrança na fila do microsserviço externo
        try:
            with httpx.Client(timeout=self.config["timeout"]) as client:
                response = client.post(
                    f"{self.config['base_url']}/filaCobranca",
                    json={
                        "ciclista": ciclista_id,
                        "valor": valor
                    },
                    headers=self.config["headers"]
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "id_cobranca": None,
                "status": "FALHA",
                "valor": valor,
                "ciclista_id": ciclista_id,
                "data_inclusao": datetime.now().isoformat(),
                "erro": f"Erro HTTP: {e.response.status_code}"
            }
        except Exception as e:
            return {
                "id_cobranca": None,
                "status": "FALHA",
                "valor": valor,
                "ciclista_id": ciclista_id,
                "data_inclusao": datetime.now().isoformat(),
                "erro": f"Erro de conexão: {str(e)}"
            }
    
    def enviar_email(self, email: str, assunto: str, mensagem: str) -> Dict[str, Any]:
        # Envia email através do microsserviço externo
        try:
            with httpx.Client(timeout=self.config["timeout"]) as client:
                response = client.post(
                    f"{self.config['base_url']}/enviarEmail",
                    json={
                        "email": email,
                        "assunto": assunto,
                        "mensagem": mensagem
                    },
                    headers=self.config["headers"]
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "id_email": None,
                "status": "FALHA",
                "destinatario": email,
                "data_envio": datetime.now().isoformat(),
                "erro": f"Erro HTTP: {e.response.status_code}"
            }
        except Exception as e:
            return {
                "id_email": None,
                "status": "FALHA",
                "destinatario": email,
                "data_envio": datetime.now().isoformat(),
                "erro": f"Erro de conexão: {str(e)}"
            } 