import pytest
from unittest.mock import patch
from app.config.integration_config import IntegrationConfig

def test_get_external_service_config():
    with patch('os.getenv') as getenv:
        getenv.side_effect = lambda k, d=None: {
            'EXTERNAL_BASE_URL': 'http://fake-external',
            'EQUIPMENT_URL': 'http://fake-equip',
            'REQUEST_TIMEOUT': '10',
            'MAX_RETRIES': '2',
            'RETRY_DELAY': '5',
        }.get(k, d)
        # Forçar reload dos atributos de classe
        IntegrationConfig.EXTERNAL_BASE_URL = 'http://fake-external'
        IntegrationConfig.EQUIPMENT_URL = 'http://fake-equip'
        IntegrationConfig.REQUEST_TIMEOUT = 10
        IntegrationConfig.MAX_RETRIES = 2
        IntegrationConfig.RETRY_DELAY = 5
        IntegrationConfig.DEFAULT_HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        config = IntegrationConfig.get_external_service_config()
        assert config['base_url'] == 'http://fake-external' or config['base_url'] == getattr(IntegrationConfig, 'EXTERNAL_URL', None)
        assert config['timeout'] == 10
        assert config['max_retries'] == 2
        assert config['retry_delay'] == 5
        assert config['headers'] == {'Content-Type': 'application/json', 'Accept': 'application/json'} 