from abc import ABC, abstractmethod
from typing import Dict, Any

# Interface para integração com microsserviço externo (cobrança, email, validação)
class ExternoRepository(ABC):
    @abstractmethod
    def validar_cartao_credito(self, cartao_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def realizar_cobranca(self, ciclista_id: int, valor: float) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def incluir_cobranca_fila(self, ciclista_id: int, valor: float) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def enviar_email(self, email: str, assunto: str, mensagem: str) -> Dict[str, Any]:
        pass 