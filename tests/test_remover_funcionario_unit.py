import pytest
from unittest.mock import Mock
from fastapi import HTTPException

from app.use_cases.remover_funcionario import RemoverFuncionario

class TestRemoverFuncionario:
    def setup_method(self):
        self.mock_repository = Mock()
        self.use_case = RemoverFuncionario(self.mock_repository)
    
    def test_execute_sucesso(self):
        # Arrange
        id_funcionario = 123
        
        # Mock do repository para simular remoção bem-sucedida
        self.mock_repository.remover.return_value = True
        
        # Act
        result = self.use_case.execute(id_funcionario)
        
        # Assert
        self.mock_repository.remover.assert_called_once_with(id_funcionario)
        assert result == {"mensagem": "Funcionário removido com sucesso"}
    
    def test_execute_funcionario_inexistente(self):
        # Arrange
        id_funcionario = 999
        
        # Mock do repository para simular funcionário não encontrado
        self.mock_repository.remover.return_value = False
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(id_funcionario)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Funcionário não encontrado"
        self.mock_repository.remover.assert_called_once_with(id_funcionario)