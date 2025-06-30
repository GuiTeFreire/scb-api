from typing import Optional, Dict, Any
from app.domain.repositories.equipamento_repository import EquipamentoRepository

class FakeEquipamentoRepository(EquipamentoRepository):
    def obter_bicicleta(self, id_bicicleta: int) -> Optional[Dict[str, Any]]:
        # Mock de obtenção de bicicleta
        return {
            "id": id_bicicleta,
            "marca": "MockMarca",
            "modelo": "MockModelo",
            "ano": "2020",
            "numero": id_bicicleta,
            "status": "DISPONÍVEL"
        }
    
    def obter_tranca(self, id_tranca: int) -> Optional[Dict[str, Any]]:
        # Mock de obtenção de tranca
        return {
            "id": id_tranca,
            "numero": id_tranca,
            "localizacao": "-22.9068,-43.1729",
            "anoDeFabricacao": "2020",
            "modelo": "MockTranca",
            "status": "OCUPADA",
            "bicicleta": 5678
        }
    
    def alterar_status_bicicleta(self, id_bicicleta: int, status: str) -> bool:
        # Mock de alteração de status da bicicleta
        print(f"[MOCK] Bicicleta {id_bicicleta} teve status alterado para {status}")
        return True
    
    def alterar_status_tranca(self, id_tranca: int, status: str) -> bool:
        # Mock de alteração de status da tranca
        print(f"[MOCK] Tranca {id_tranca} teve status alterado para {status}")
        return True
    
    def obter_bicicleta_na_tranca(self, id_tranca: int) -> Optional[Dict[str, Any]]:
        # Mock de obtenção de bicicleta na tranca
        return {
            "id": 5678,
            "marca": "MockMarca",
            "modelo": "MockModelo",
            "ano": "2020",
            "numero": 5678,
            "status": "EM_USO"
        }

fake_equipamento_repository = FakeEquipamentoRepository() 