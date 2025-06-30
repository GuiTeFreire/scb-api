import pytest
from unittest.mock import patch, MagicMock
from app.infra.repositories.real_equipamento_repository import RealEquipamentoRepository

@pytest.fixture
def repo():
    return RealEquipamentoRepository()

def test_obter_bicicleta_sucesso(repo):
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        mock_client.get.return_value.json.return_value = {'id': 1}
        mock_client.get.return_value.raise_for_status.return_value = None
        result = repo.obter_bicicleta(1)
        assert result == {'id': 1}

def test_obter_bicicleta_404(repo):
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        from httpx import HTTPStatusError, Response, Request
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 404
        mock_request = MagicMock(spec=Request)
        mock_client.get.side_effect = HTTPStatusError('Not found', request=mock_request, response=mock_response)
        result = repo.obter_bicicleta(1)
        assert result is None

def test_alterar_status_bicicleta_sucesso(repo):
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        mock_client.post.return_value.raise_for_status.return_value = None
        assert repo.alterar_status_bicicleta(1, 'NOVA') is True

def test_alterar_status_bicicleta_falha(repo):
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        mock_client.post.side_effect = Exception('Erro')
        assert repo.alterar_status_bicicleta(1, 'NOVA') is False

def test_obter_tranca_sucesso(repo):
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        mock_client.get.return_value.json.return_value = {'id': 1}
        mock_client.get.return_value.raise_for_status.return_value = None
        result = repo.obter_tranca(1)
        assert result == {'id': 1}

def test_obter_tranca_404(repo):
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        from httpx import HTTPStatusError, Response, Request
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 404
        mock_request = MagicMock(spec=Request)
        mock_client.get.side_effect = HTTPStatusError('Not found', request=mock_request, response=mock_response)
        result = repo.obter_tranca(1)
        assert result is None

def test_alterar_status_tranca_sucesso(repo):
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        mock_client.post.return_value.raise_for_status.return_value = None
        assert repo.alterar_status_tranca(1, 'NOVA') is True

def test_alterar_status_tranca_falha(repo):
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        mock_client.post.side_effect = Exception('Erro')
        assert repo.alterar_status_tranca(1, 'NOVA') is False

def test_obter_bicicleta_na_tranca_sucesso(repo):
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        mock_client.get.return_value.json.return_value = {'bicicleta': 1}
        mock_client.get.return_value.raise_for_status.return_value = None
        result = repo.obter_bicicleta_na_tranca(1)
        assert result == {'bicicleta': 1}

def test_obter_bicicleta_na_tranca_404(repo):
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        from httpx import HTTPStatusError, Response, Request
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 404
        mock_request = MagicMock(spec=Request)
        mock_client.get.side_effect = HTTPStatusError('Not found', request=mock_request, response=mock_response)
        result = repo.obter_bicicleta_na_tranca(1)
        assert result is None

def test_obter_bicicleta_erro_http(repo):
    from unittest.mock import patch, MagicMock
    import pytest
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        from httpx import HTTPStatusError, Response, Request
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 500
        mock_request = MagicMock(spec=Request)
        mock_client.get.side_effect = HTTPStatusError('Erro', request=mock_request, response=mock_response)
        with pytest.raises(HTTPStatusError):
            repo.obter_bicicleta(1)

def test_obter_tranca_erro_http(repo):
    from unittest.mock import patch, MagicMock
    import pytest
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        from httpx import HTTPStatusError, Response, Request
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 500
        mock_request = MagicMock(spec=Request)
        mock_client.get.side_effect = HTTPStatusError('Erro', request=mock_request, response=mock_response)
        with pytest.raises(HTTPStatusError):
            repo.obter_tranca(1)

def test_obter_bicicleta_na_tranca_erro_http(repo):
    from unittest.mock import patch, MagicMock
    import pytest
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        from httpx import HTTPStatusError, Response, Request
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 500
        mock_request = MagicMock(spec=Request)
        mock_client.get.side_effect = HTTPStatusError('Erro', request=mock_request, response=mock_response)
        with pytest.raises(HTTPStatusError):
            repo.obter_bicicleta_na_tranca(1)

def test_obter_bicicleta_erro_generico(repo):
    from unittest.mock import patch
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        mock_client.get.side_effect = Exception('Erro generico')
        result = repo.obter_bicicleta(1)
        assert result is None

def test_obter_tranca_erro_generico(repo):
    from unittest.mock import patch
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        mock_client.get.side_effect = Exception('Erro generico')
        result = repo.obter_tranca(1)
        assert result is None

def test_alterar_status_bicicleta_erro_generico(repo):
    from unittest.mock import patch
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        mock_client.post.side_effect = Exception('Erro generico')
        result = repo.alterar_status_bicicleta(1, 'NOVA')
        assert result is False

def test_alterar_status_tranca_erro_generico(repo):
    from unittest.mock import patch
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        mock_client.post.side_effect = Exception('Erro generico')
        result = repo.alterar_status_tranca(1, 'NOVA')
        assert result is False

def test_obter_bicicleta_na_tranca_erro_generico(repo):
    from unittest.mock import patch
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        mock_client.get.side_effect = Exception('Erro generico')
        result = repo.obter_bicicleta_na_tranca(1)
        assert result is None 