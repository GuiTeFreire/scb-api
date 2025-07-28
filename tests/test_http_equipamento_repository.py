import pytest
from unittest.mock import patch, Mock
from app.infra.repositories.http_equipamento_repository import HttpEquipamentoRepository

class TestHttpEquipamentoRepository:
    
    def setup_method(self):
        self.repo = HttpEquipamentoRepository()
    
    @patch('httpx.get')
    def test_obter_bicicleta_sucesso(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1, "status": "DISPONIVEL"}
        mock_get.return_value = mock_response
        
        result = self.repo.obter_bicicleta(1)
        
        assert result == {"id": 1, "status": "DISPONIVEL"}
        mock_get.assert_called_once_with(f"{self.repo.base_url}/bicicletas/1")
    
    @patch('httpx.get')
    def test_obter_bicicleta_nao_encontrada(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = self.repo.obter_bicicleta(999)
        
        assert result is None
    
    @patch('httpx.get')
    def test_obter_tranca_sucesso(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1, "status": "DISPONIVEL"}
        mock_get.return_value = mock_response
        
        result = self.repo.obter_tranca(1)
        
        assert result == {"id": 1, "status": "DISPONIVEL"}
        mock_get.assert_called_once_with(f"{self.repo.base_url}/trancas/1")
    
    @patch('httpx.get')
    def test_obter_tranca_nao_encontrada(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = self.repo.obter_tranca(999)
        
        assert result is None
    
    @patch('httpx.post')
    def test_alterar_status_bicicleta_sucesso(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        result = self.repo.alterar_status_bicicleta(1, "OCUPADA")
        
        assert result is True
        mock_post.assert_called_once_with(f"{self.repo.base_url}/bicicletas/1/status/OCUPADA")
    
    @patch('httpx.post')
    def test_alterar_status_bicicleta_falha(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        
        result = self.repo.alterar_status_bicicleta(1, "OCUPADA")
        
        assert result is False
    
    @patch('httpx.post')
    def test_alterar_status_tranca_sucesso(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        result = self.repo.alterar_status_tranca(1, "OCUPADA")
        
        assert result is True
        mock_post.assert_called_once_with(f"{self.repo.base_url}/trancas/1/status/OCUPADA")
    
    @patch('httpx.post')
    def test_alterar_status_tranca_falha(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        
        result = self.repo.alterar_status_tranca(1, "OCUPADA")
        
        assert result is False
    
    @patch('httpx.get')
    def test_obter_bicicleta_na_tranca_sucesso(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1, "status": "OCUPADA"}
        mock_get.return_value = mock_response
        
        result = self.repo.obter_bicicleta_na_tranca(1)
        
        assert result == {"id": 1, "status": "OCUPADA"}
        mock_get.assert_called_once_with(f"{self.repo.base_url}/trancas/1/bicicleta")
    
    @patch('httpx.get')
    def test_obter_bicicleta_na_tranca_nao_encontrada(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = self.repo.obter_bicicleta_na_tranca(1)
        
        assert result is None
    
    @patch('httpx.post')
    def test_trancar_tranca_sucesso(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        result = self.repo.trancar_tranca(1, 2)
        
        assert result is True
        mock_post.assert_called_once_with(f"{self.repo.base_url}/tranca/1/trancar", json={"bicicleta": 2})
    
    @patch('httpx.post')
    def test_trancar_tranca_falha(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 422
        mock_post.return_value = mock_response
        
        result = self.repo.trancar_tranca(1, 2)
        
        assert result is False
    
    @patch('httpx.post')
    def test_destrancar_tranca_sucesso(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        result = self.repo.destrancar_tranca(1)
        
        assert result is True
        mock_post.assert_called_once_with(f"{self.repo.base_url}/tranca/1/destrancar")
    
    @patch('httpx.post')
    def test_destrancar_tranca_falha(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        
        result = self.repo.destrancar_tranca(1)
        
        assert result is False
    
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