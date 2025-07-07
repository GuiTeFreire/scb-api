from unittest.mock import Mock

from app.use_cases.listar_funcionarios import ListarFuncionarios

class TestListarFuncionarios:
    def setup_method(self):
        self.mock_repository = Mock()
        self.use_case = ListarFuncionarios(self.mock_repository)
    
    def test_execute_sucesso_lista_vazia(self):
        # Arrange
        self.mock_repository.listar_todos.return_value = []
        
        # Act
        result = self.use_case.execute()
        
        # Assert
        self.mock_repository.listar_todos.assert_called_once()
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_execute_sucesso_com_funcionarios(self):
        # Arrange
        funcionario1_mock = Mock()
        funcionario1_mock.id = 1
        funcionario1_mock.nome = "Carlos Souza"
        funcionario1_mock.email = "carlos@empresa.com"
        
        funcionario2_mock = Mock()
        funcionario2_mock.id = 2
        funcionario2_mock.nome = "Maria Santos"
        funcionario2_mock.email = "maria@empresa.com"
        
        self.mock_repository.listar_todos.return_value = [funcionario1_mock, funcionario2_mock]
        
        # Act
        result = self.use_case.execute()
        
        # Assert
        self.mock_repository.listar_todos.assert_called_once()
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0].id == 1
        assert result[0].nome == "Carlos Souza"
        assert result[1].id == 2
        assert result[1].nome == "Maria Santos"