import pytest
from unittest.mock import patch, MagicMock
from app.infra.repositories.real_externo_repository import RealExternoRepository

@pytest.fixture
def repo():
    return RealExternoRepository()

def test_validar_cartao_credito_sucesso(repo):
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        mock_client.post.return_value.json.return_value = {'valido': True}
        mock_client.post.return_value.raise_for_status.return_value = None
        result = repo.validar_cartao_credito({'numero': '123'})
        assert result == {'valido': True}

def test_validar_cartao_credito_falha(repo):
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        from httpx import HTTPStatusError, Response, Request
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 400
        mock_request = MagicMock(spec=Request)
        mock_client.post.side_effect = HTTPStatusError('Erro', request=mock_request, response=mock_response)
        result = repo.validar_cartao_credito({'numero': '123'})
        assert result['valido'] is False

def test_realizar_cobranca_sucesso(repo):
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        mock_client.post.return_value.json.return_value = {'status': 'OK'}
        mock_client.post.return_value.raise_for_status.return_value = None
        result = repo.realizar_cobranca(1, 10.0)
        assert result == {'status': 'OK'}

def test_incluir_cobranca_fila_sucesso(repo):
    from unittest.mock import patch
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        mock_client.post.return_value.json.return_value = {'status': 'OK'}
        mock_client.post.return_value.raise_for_status.return_value = None
        result = repo.incluir_cobranca_fila(1, 10.0)
        assert result == {'status': 'OK'}

def test_incluir_cobranca_fila_falha(repo):
    from unittest.mock import patch, MagicMock
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        from httpx import HTTPStatusError, Response, Request
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 400
        mock_request = MagicMock(spec=Request)
        mock_client.post.side_effect = HTTPStatusError('Erro', request=mock_request, response=mock_response)
        result = repo.incluir_cobranca_fila(1, 10.0)
        assert result['status'] == 'FALHA'

def test_enviar_email_sucesso(repo):
    from unittest.mock import patch
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        mock_client.post.return_value.json.return_value = {'status': 'OK'}
        mock_client.post.return_value.raise_for_status.return_value = None
        result = repo.enviar_email('a@b.com', 'assunto', 'msg')
        assert result == {'status': 'OK'}

def test_enviar_email_falha(repo):
    from unittest.mock import patch, MagicMock
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        from httpx import HTTPStatusError, Response, Request
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 400
        mock_request = MagicMock(spec=Request)
        mock_client.post.side_effect = HTTPStatusError('Erro', request=mock_request, response=mock_response)
        result = repo.enviar_email('a@b.com', 'assunto', 'msg')
        assert result['status'] == 'FALHA'

def test_realizar_cobranca_erro_http(repo):
    from unittest.mock import patch, MagicMock
    import pytest
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        from httpx import HTTPStatusError, Response, Request
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 500
        mock_request = MagicMock(spec=Request)
        mock_client.post.side_effect = HTTPStatusError('Erro', request=mock_request, response=mock_response)
        result = repo.realizar_cobranca(1, 10.0)
        assert result['status'] == 'FALHA'
        assert 'Erro HTTP' in result['erro']

def test_incluir_cobranca_fila_erro_http(repo):
    from unittest.mock import patch, MagicMock
    import pytest
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        from httpx import HTTPStatusError, Response, Request
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 500
        mock_request = MagicMock(spec=Request)
        mock_client.post.side_effect = HTTPStatusError('Erro', request=mock_request, response=mock_response)
        result = repo.incluir_cobranca_fila(1, 10.0)
        assert result['status'] == 'FALHA'
        assert 'Erro HTTP' in result['erro']

def test_enviar_email_erro_http(repo):
    from unittest.mock import patch, MagicMock
    import pytest
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        from httpx import HTTPStatusError, Response, Request
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 500
        mock_request = MagicMock(spec=Request)
        mock_client.post.side_effect = HTTPStatusError('Erro', request=mock_request, response=mock_response)
        result = repo.enviar_email('a@b.com', 'assunto', 'msg')
        assert result['status'] == 'FALHA'
        assert 'Erro HTTP' in result['erro']

def test_validar_cartao_credito_erro_generico(repo):
    from unittest.mock import patch
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        mock_client.post.side_effect = Exception('Erro generico')
        result = repo.validar_cartao_credito({'numero': '123'})
        assert result['valido'] is False
        assert 'Erro de conexão' in result['mensagem']

def test_realizar_cobranca_erro_generico(repo):
    from unittest.mock import patch
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        mock_client.post.side_effect = Exception('Erro generico')
        result = repo.realizar_cobranca(1, 10.0)
        assert result['status'] == 'FALHA'
        assert 'Erro de conexão' in result['erro']

def test_incluir_cobranca_fila_erro_generico(repo):
    from unittest.mock import patch
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        mock_client.post.side_effect = Exception('Erro generico')
        result = repo.incluir_cobranca_fila(1, 10.0)
        assert result['status'] == 'FALHA'
        assert 'Erro de conexão' in result['erro']

def test_enviar_email_erro_generico(repo):
    from unittest.mock import patch
    with patch('httpx.Client') as MockClient:
        mock_client = MockClient.return_value.__enter__.return_value
        mock_client.post.side_effect = Exception('Erro generico')
        result = repo.enviar_email('a@b.com', 'assunto', 'msg')
        assert result['status'] == 'FALHA'
        assert 'Erro de conexão' in result['erro'] 