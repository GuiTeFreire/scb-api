import pytest
from unittest.mock import Mock
from fastapi import HTTPException

from app.use_cases.cadastrar_funcionario import CadastrarFuncionario
from app.domain.entities.funcionario import NovoFuncionario

class TestCadastrarFuncionario:
    def setup_method(self):
        self.mock_repository = Mock()
        self.use_case = CadastrarFuncionario(self.mock_repository)
        
        # Mock do salvamento
        self.mock_repository.salvar.return_value = Mock()
    
    def test_execute_sucesso(self):
        # Arrange
        dados = NovoFuncionario(
            nome="Carlos Souza",
            idade=35,
            funcao="Gerente",
            cpf="12345678900",
            email="carlos@empresa.com",
            senha="123456"
        )
        
        # Mock do repository para simular email não existente
        self.mock_repository.buscar_por_email.return_value = None
        
        # Act
        result = self.use_case.execute(dados)
        
        # Assert
        self.mock_repository.buscar_por_email.assert_called_once_with("carlos@empresa.com")
        self.mock_repository.salvar.assert_called_once_with(dados)
        assert result is not None
    
    def test_execute_erro_email_duplicado(self):
        # Arrange
        dados = NovoFuncionario(
            nome="João Silva",
            idade=30,
            funcao="Atendente",
            cpf="11111111111",
            email="joao@empresa.com",
            senha="123456"
        )
        
        # Mock do repository para simular email existente
        self.mock_repository.buscar_por_email.return_value = Mock()
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(dados)
        
        assert exc_info.value.status_code == 422
        assert exc_info.value.detail == "E-mail já cadastrado"
        self.mock_repository.buscar_por_email.assert_called_once_with("joao@empresa.com")
        # Verifica que salvar não foi chamado
        self.mock_repository.salvar.assert_not_called()