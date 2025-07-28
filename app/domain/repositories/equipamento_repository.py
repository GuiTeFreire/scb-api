from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

# Interface para integração com microsserviço de equipamento (bicicletas, trancas, totens)
class EquipamentoRepository(ABC):
    @abstractmethod
    def obter_bicicleta(self, id_bicicleta: int) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def obter_tranca(self, id_tranca: int) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def alterar_status_bicicleta(self, id_bicicleta: int, status: str) -> bool:
        pass
    
    @abstractmethod
    def alterar_status_tranca(self, id_tranca: int, status: str) -> bool:
        pass
    
    @abstractmethod
    def obter_bicicleta_na_tranca(self, id_tranca: int) -> Optional[Dict[str, Any]]:
        pass 

    @abstractmethod
    def destrancar_tranca(self, id_tranca: int) -> bool:
        pass 

    @abstractmethod
    def trancar_tranca(self, id_tranca: int, id_bicicleta: int) -> bool:
        pass 

    @abstractmethod
    def restaurar_dados(self) -> bool:
        pass 