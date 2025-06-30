from typing import Dict, Any
from datetime import datetime
from app.domain.repositories.externo_repository import ExternoRepository

class FakeExternoRepository(ExternoRepository):
    def validar_cartao_credito(self, cartao_data: Dict[str, Any]) -> Dict[str, Any]:
        # Mock de validação de cartão de crédito
        numero = cartao_data.get("numero", "")
        if not numero.isdigit() or len(numero) < 13:
            return {
                "valido": False,
                "mensagem": "Número do cartão inválido"
            }
        
        return {
            "valido": True,
            "mensagem": "Cartão válido"
        }
    
    def realizar_cobranca(self, ciclista_id: int, valor: float) -> Dict[str, Any]:
        # Mock de cobrança
        return {
            "id_cobranca": 1234,
            "status": "APROVADA",
            "valor": valor,
            "ciclista_id": ciclista_id,
            "data_cobranca": datetime.now().isoformat()
        }
    
    def incluir_cobranca_fila(self, ciclista_id: int, valor: float) -> Dict[str, Any]:
        # Mock de inclusão na fila de cobrança
        return {
            "id_cobranca": 5678,
            "status": "PENDENTE",
            "valor": valor,
            "ciclista_id": ciclista_id,
            "data_inclusao": datetime.now().isoformat()
        }
    
    def enviar_email(self, email: str, assunto: str, mensagem: str) -> Dict[str, Any]:
        # Mock de envio de email
        print(f"[MOCK] Email enviado para {email}")
        print(f"[MOCK] Assunto: {assunto}")
        print(f"[MOCK] Mensagem: {mensagem}")
        
        return {
            "id_email": 9999,
            "status": "ENVIADO",
            "destinatario": email,
            "data_envio": datetime.now().isoformat()
        }

fake_externo_repository = FakeExternoRepository() 