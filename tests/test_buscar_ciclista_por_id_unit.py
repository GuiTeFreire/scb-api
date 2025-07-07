import pytest
from unittest.mock import Mock
from fastapi import HTTPException

from app.use_cases.buscar_ciclista_por_id import BuscarCiclistaPorId

class TestBuscarCiclistaPorId:  
    def setup_method(self):
        self.mock_repository = Mock()
        self.use_case = BuscarCiclistaPorId(self.mock_repository)
    
    def test_execute_sucesso(self):
        # Arrange
        id_ciclista = 1
        
        # Mock do repository para simular ciclista encontrado
        ciclista_mock = Mock()
        ciclista_mock.id = 1
        ciclista_mock.nome = "João Silva"
        ciclista_mock.email = "joao@teste.com"
        self.mock_repository.buscar_por_id.return_value = ciclista_mock
        
        # Act
        result = self.use_case.execute(id_ciclista)
        
        # Assert
        self.mock_repository.buscar_por_id.assert_called_once_with(id_ciclista)
        assert result is not None
        assert result.id == 1
        assert result.nome == "João Silva"
    
    def test_execute_ciclista_inexistente(self):
        # Arrange
        id_ciclista = 999
        
        # Mock do repository para simular ciclista não encontrado
        self.mock_repository.buscar_por_id.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(id_ciclista)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Ciclista não encontrado"
        self.mock_repository.buscar_por_id.assert_called_once_with(id_ciclista)
