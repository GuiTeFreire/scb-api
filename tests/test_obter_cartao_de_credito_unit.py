import pytest
from unittest.mock import Mock
from fastapi import HTTPException

from app.use_cases.obter_cartao_de_credito import ObterCartaoDeCredito

class TestObterCartaoDeCredito:
    def setup_method(self):
        self.mock_repository = Mock()
        self.use_case = ObterCartaoDeCredito(self.mock_repository)
    
    def test_execute_sucesso(self):
        # Arrange
        id_ciclista = 1
        
        # Mock do cartão de crédito
        cartao_mock = Mock()
        cartao_mock.id = 1
        cartao_mock.nomeTitular = "João Silva"
        cartao_mock.numero = "4111111111111111"
        cartao_mock.cvv = "123"
        
        # Mock do ciclista com cartão
        ciclista_mock = Mock()
        ciclista_mock.cartaoDeCredito = cartao_mock
        self.mock_repository.buscar_por_id.return_value = ciclista_mock
        
        # Act
        result = self.use_case.execute(id_ciclista)
        
        # Assert
        self.mock_repository.buscar_por_id.assert_called_once_with(id_ciclista)
        assert result is not None
        assert result.id == 1
        assert result.nomeTitular == "João Silva"
        assert result.numero == "4111111111111111"
    
    def test_execute_ciclista_inexistente(self):
        # Arrange
        id_ciclista = 999
        
        # Mock do repository para simular ciclista não encontrado
        self.mock_repository.buscar_por_id.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(id_ciclista)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail["codigo"] == "404"
        assert exc_info.value.detail["mensagem"] == "Ciclista não encontrado"
        self.mock_repository.buscar_por_id.assert_called_once_with(id_ciclista)