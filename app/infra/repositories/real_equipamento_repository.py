import httpx
from typing import Optional, Dict, Any
from app.domain.repositories.equipamento_repository import EquipamentoRepository
from app.config.integration_config import IntegrationConfig

# Implementação real para microsserviço de equipamento
class RealEquipamentoRepository(EquipamentoRepository):
    def __init__(self):
        self.config = IntegrationConfig.get_equipment_service_config()
    
    def obter_bicicleta(self, id_bicicleta: int) -> Optional[Dict[str, Any]]:
        # Obtém dados da bicicleta do microsserviço de equipamento
        try:
            with httpx.Client(timeout=self.config["timeout"]) as client:
                response = client.get(
                    f"{self.config['base_url']}/bicicleta/{id_bicicleta}",
                    headers=self.config["headers"]
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
        except Exception as e:
            print(f"Erro ao obter bicicleta {id_bicicleta}: {str(e)}")
            return None
    
    def obter_tranca(self, id_tranca: int) -> Optional[Dict[str, Any]]:
        # Obtém dados da tranca do microsserviço de equipamento
        try:
            with httpx.Client(timeout=self.config["timeout"]) as client:
                response = client.get(
                    f"{self.config['base_url']}/tranca/{id_tranca}",
                    headers=self.config["headers"]
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
        except Exception as e:
            print(f"Erro ao obter tranca {id_tranca}: {str(e)}")
            return None
    
    def alterar_status_bicicleta(self, id_bicicleta: int, status: str) -> bool:
        # Altera status da bicicleta no microsserviço de equipamento
        try:
            with httpx.Client(timeout=self.config["timeout"]) as client:
                response = client.post(
                    f"{self.config['base_url']}/bicicleta/{id_bicicleta}/status/{status}",
                    headers=self.config["headers"]
                )
                response.raise_for_status()
                return True
        except Exception as e:
            print(f"Erro ao alterar status da bicicleta {id_bicicleta}: {str(e)}")
            return False
    
    def alterar_status_tranca(self, id_tranca: int, status: str) -> bool:
        # Altera status da tranca no microsserviço de equipamento
        try:
            with httpx.Client(timeout=self.config["timeout"]) as client:
                response = client.post(
                    f"{self.config['base_url']}/tranca/{id_tranca}/status/{status}",
                    headers=self.config["headers"]
                )
                response.raise_for_status()
                return True
        except Exception as e:
            print(f"Erro ao alterar status da tranca {id_tranca}: {str(e)}")
            return False
    
    def obter_bicicleta_na_tranca(self, id_tranca: int) -> Optional[Dict[str, Any]]:
        # Obtém bicicleta associada à tranca
        try:
            with httpx.Client(timeout=self.config["timeout"]) as client:
                response = client.get(
                    f"{self.config['base_url']}/tranca/{id_tranca}/bicicleta",
                    headers=self.config["headers"]
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
        except Exception as e:
            print(f"Erro ao obter bicicleta na tranca {id_tranca}: {str(e)}")
            return None 