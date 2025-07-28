import pytest
from unittest.mock import patch, Mock
from app.infra.repositories.http_externo_repository import HttpExternoRepository

class TestHttpExternoRepository:
    
    def setup_method(self):
        self.repo = HttpExternoRepository()
    
    @patch('httpx.post')
    def test_validar_cartao_credito_sucesso(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        cartao_data = {"numero": "4012001037141112", "validade": "12/2025", "cvv": "123"}
        result = self.repo.validar_cartao_credito(cartao_data)
        
        assert result == {"valido": True}
        mock_post.assert_called_once_with(f"{self.repo.base_url}/validaCartaoDeCredito", json=cartao_data)
    
    @patch('httpx.post')
    def test_validar_cartao_credito_invalido_422(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 422
        mock_response.text = '{"detail": "Cartão inválido"}'
        mock_response.json.return_value = {"detail": "Cartão inválido"}
        mock_post.return_value = mock_response
        
        cartao_data = {"numero": "0000000000000000", "validade": "12/2025", "cvv": "123"}
        result = self.repo.validar_cartao_credito(cartao_data)
        
        assert result == {"detail": "Cartão inválido"}
    
    @patch('httpx.post')
    def test_validar_cartao_credito_resposta_inesperada(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Erro interno"
        mock_post.return_value = mock_response
        
        cartao_data = {"numero": "4012001037141112", "validade": "12/2025", "cvv": "123"}
        result = self.repo.validar_cartao_credito(cartao_data)
        
        assert result == {"valido": False, "mensagem": "Resposta inesperada do serviço externo"}
    
    @patch('httpx.post')
    def test_realizar_cobranca_sucesso(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id_cobranca": 123, "status": "APROVADA"}
        mock_post.return_value = mock_response
        
        result = self.repo.realizar_cobranca(1, 10.50)
        
        assert result == {"id_cobranca": 123, "status": "APROVADA"}
        mock_post.assert_called_once_with(f"{self.repo.base_url}/cobranca", json={"ciclista": 1, "valor": 10.50})
    
    @patch('httpx.post')
    def test_incluir_cobranca_fila_sucesso(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id_cobranca": 456, "status": "PENDENTE"}
        mock_post.return_value = mock_response
        
        result = self.repo.incluir_cobranca_fila(1, 15.75)
        
        assert result == {"id_cobranca": 456, "status": "PENDENTE"}
        mock_post.assert_called_once_with(f"{self.repo.base_url}/filaCobranca", json={"ciclista": 1, "valor": 15.75})
    
    @patch('httpx.post')
    def test_enviar_email_sucesso(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id_email": 789, "status": "ENVIADO"}
        mock_post.return_value = mock_response
        
        result = self.repo.enviar_email("test@example.com", "Teste", "Mensagem de teste")
        
        assert result == {"id_email": 789, "status": "ENVIADO"}
        mock_post.assert_called_once_with(
            f"{self.repo.base_url}/enviarEmail", 
            json={"email": "test@example.com", "assunto": "Teste", "mensagem": "Mensagem de teste"}
        )
    
    @patch('httpx.get')
    def test_restaurar_dados_sucesso(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = self.repo.restaurar_dados()
        
        assert result is True
        mock_get.assert_called_once_with(f"{self.repo.base_url}/restaurarDados")
    
    @patch('httpx.get')
    def test_restaurar_dados_falha(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        result = self.repo.restaurar_dados()
        
        assert result is False 