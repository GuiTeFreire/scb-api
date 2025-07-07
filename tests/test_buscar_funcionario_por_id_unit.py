import pytest
from unittest.mock import Mock
from fastapi import HTTPException

from app.use_cases.buscar_funcionario_por_id import BuscarFuncionarioPorId

class TestBuscarFuncionarioPorId:
    def setup_method(self):
        self.mock_repository = Mock()
        self.use_case = BuscarFuncionarioPorId(self.mock_repository)
    
    def test_execute_sucesso(self):
        # Arrange
        id_funcionario = 1
        
        # Mock do repository para simular funcionário encontrado
        funcionario_mock = Mock()
        funcionario_mock.id = 1
        funcionario_mock.nome = "Carlos Souza"
        funcionario_mock.email = "carlos@empresa.com"
        self.mock_repository.buscar_por_id.return_value = funcionario_mock
        
        # Act
        result = self.use_case.execute(id_funcionario)
        
        # Assert
        self.mock_repository.buscar_por_id.assert_called_once_with(id_funcionario)
        assert result is not None
        assert result.id == 1
        assert result.nome == "Carlos Souza"
    
    def test_execute_funcionario_inexistente(self):
        # Arrange
        id_funcionario = 999
        
        # Mock do repository para simular funcionário não encontrado
        self.mock_repository.buscar_por_id.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(id_funcionario)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Funcionário não encontrado"
        self.mock_repository.buscar_por_id.assert_called_once_with(id_funcionario)
