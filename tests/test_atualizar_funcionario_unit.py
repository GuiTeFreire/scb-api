import pytest
from unittest.mock import Mock
from fastapi import HTTPException

from app.use_cases.atualizar_funcionario import AtualizarFuncionario
from app.domain.entities.funcionario import NovoFuncionario

class TestAtualizarFuncionario:
    def setup_method(self):
        """Setup para cada teste - cria mocks limpos"""
        self.mock_repository = Mock()
        self.use_case = AtualizarFuncionario(self.mock_repository)
    
    def test_execute_sucesso(self):
        """Testa atualização bem-sucedida de funcionário"""
        # Arrange
        id_funcionario = 1
        dados = NovoFuncionario(
            nome="Carlos Souza",
            idade=35,
            funcao="Gerente",
            cpf="12345678900",
            email="carlos@empresa.com",
            senha="123456"
        )
        
        # Mock do repository para simular atualização bem-sucedida
        funcionario_mock = Mock()
        funcionario_mock.nome = "Carlos Souza"
        funcionario_mock.email = "carlos@empresa.com"
        self.mock_repository.atualizar.return_value = funcionario_mock
        
        # Act
        result = self.use_case.execute(id_funcionario, dados)
        
        # Assert
        self.mock_repository.atualizar.assert_called_once_with(id_funcionario, dados)
        assert result is not None
        assert result.nome == "Carlos Souza"
    
    def test_execute_funcionario_inexistente(self):
        """Testa erro quando funcionário não existe"""
        # Arrange
        id_funcionario = 999
        dados = NovoFuncionario(
            nome="João Silva",
            idade=30,
            funcao="Atendente",
            cpf="11111111111",
            email="joao@empresa.com",
            senha="123456"
        )
        
        # Mock do repository para simular funcionário não encontrado
        self.mock_repository.atualizar.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(id_funcionario, dados)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Funcionário não encontrado"
        self.mock_repository.atualizar.assert_called_once_with(id_funcionario, dados)
    
    def test_execute_verifica_chamada_repository(self):
        """Testa se a chamada ao repository é feita corretamente"""
        # Arrange
        id_funcionario = 456
        dados = NovoFuncionario(
            nome="Maria Santos",
            idade=28,
            funcao="Analista",
            cpf="22222222222",
            email="maria@empresa.com",
            senha="senha123"
        )
        
        # Mock do repository para simular atualização bem-sucedida
        funcionario_mock = Mock()
        self.mock_repository.atualizar.return_value = funcionario_mock
        
        # Act
        self.use_case.execute(id_funcionario, dados)
        
        # Assert - verifica parâmetros da chamada
        assert self.mock_repository.atualizar.call_count == 1
        call_args = self.mock_repository.atualizar.call_args
        assert call_args[0][0] == id_funcionario
        assert call_args[0][1] == dados
    
    def test_execute_retorna_funcionario_atualizado(self):
        """Testa se o funcionário atualizado é retornado corretamente"""
        # Arrange
        id_funcionario = 789
        dados = NovoFuncionario(
            nome="Pedro Costa",
            idade=32,
            funcao="Desenvolvedor",
            cpf="33333333333",
            email="pedro@empresa.com",
            senha="senha456"
        )
        
        # Mock do repository para simular atualização bem-sucedida
        funcionario_mock = Mock()
        funcionario_mock.nome = "Pedro Costa"
        funcionario_mock.idade = 32
        funcionario_mock.funcao = "Desenvolvedor"
        funcionario_mock.email = "pedro@empresa.com"
        self.mock_repository.atualizar.return_value = funcionario_mock
        
        # Act
        result = self.use_case.execute(id_funcionario, dados)
        
        # Assert
        assert result is not None
        assert result.nome == "Pedro Costa"
        assert result.idade == 32
        assert result.funcao == "Desenvolvedor"
        assert result.email == "pedro@empresa.com" 