from unittest.mock import Mock

from app.use_cases.verificar_email_existente import VerificarEmailExistente

class TestVerificarEmailExistente:
    def setup_method(self):
        self.mock_repository = Mock()
        self.use_case = VerificarEmailExistente(self.mock_repository)
    
    def test_execute_email_existente(self):
        # Arrange
        email = "joao@teste.com"
        
        # Mock do repository para simular email encontrado
        self.mock_repository.buscar_por_email.return_value = Mock()
        
        # Act
        result = self.use_case.execute(email)
        
        # Assert
        self.mock_repository.buscar_por_email.assert_called_once_with(email)
        assert result is True
    
    def test_execute_email_inexistente(self):
        # Arrange
        email = "email_inexistente@teste.com"
        
        # Mock do repository para simular email não encontrado
        self.mock_repository.buscar_por_email.return_value = None
        
        # Act
        result = self.use_case.execute(email)
        
        # Assert
        self.mock_repository.buscar_por_email.assert_called_once_with(email)
        assert result is False