from typing import Dict, Any
import os

class IntegrationConfig:
    # URLs dos microsserviços (alterar conforme o necessário)
    EXTERNAL_BASE_URL = os.getenv("EXTERNAL_BASE_URL", "http://localhost:8001")
    EQUIPMENT_URL = os.getenv("EQUIPMENT_URL", "http://localhost:8002")
    
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", "1"))
    
    DEFAULT_HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    @classmethod
    def get_external_service_config(cls) -> Dict[str, Any]:
        return {
            "base_url": cls.EXTERNAL_URL,
            "timeout": cls.REQUEST_TIMEOUT,
            "max_retries": cls.MAX_RETRIES,
            "retry_delay": cls.RETRY_DELAY,
            "headers": cls.DEFAULT_HEADERS
        }
    
    @classmethod
    def get_equipment_service_config(cls) -> Dict[str, Any]:
        return {
            "base_url": cls.EQUIPMENT_URL,
            "timeout": cls.REQUEST_TIMEOUT,
            "max_retries": cls.MAX_RETRIES,
            "retry_delay": cls.RETRY_DELAY,
            "headers": cls.DEFAULT_HEADERS
        } 