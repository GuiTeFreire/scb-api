import os
import httpx
from app.domain.repositories.equipamento_repository import EquipamentoRepository

class HttpEquipamentoRepository(EquipamentoRepository):
    def __init__(self):
        self.base_url = os.getenv("EQUIPAMENTO_URL", "http://localhost:8001")

    def obter_bicicleta(self, id_bicicleta):
        response = httpx.get(f"{self.base_url}/api/bicicletas/{id_bicicleta}")
        if response.status_code == 200:
            return response.json()
        return None

    def obter_tranca(self, id_tranca):
        response = httpx.get(f"{self.base_url}/api/trancas/{id_tranca}")
        if response.status_code == 200:
            return response.json()
        return None

    def alterar_status_bicicleta(self, id_bicicleta, status):
        response = httpx.post(f"{self.base_url}/api/bicicletas/{id_bicicleta}/status/{status}")
        return response.status_code == 200

    def alterar_status_tranca(self, id_tranca, status):
        response = httpx.post(f"{self.base_url}/api/trancas/{id_tranca}/status/{status}")
        return response.status_code == 200

    def obter_bicicleta_na_tranca(self, id_tranca):
        response = httpx.get(f"{self.base_url}/api/trancas/{id_tranca}/bicicleta")
        if response.status_code == 200:
            return response.json()
        return None

    def trancar_tranca(self, id_tranca, id_bicicleta):
        url = f"{self.base_url}/api/tranca/{id_tranca}/trancar"
        response = httpx.post(url, json={"idBicicleta": id_bicicleta})
        return response.status_code == 200

    def destrancar_tranca(self, id_tranca):
        response = httpx.post(f"{self.base_url}/api/tranca/{id_tranca}/destrancar")
        return response.status_code == 200 