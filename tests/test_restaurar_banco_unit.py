from unittest.mock import Mock

from app.use_cases.restaurar_banco import RestaurarBanco

class TestRestaurarBanco:
    def setup_method(self):
        self.mock_funcionario_repo = Mock()
        self.mock_ciclista_repo = Mock()
        self.mock_aluguel_repo = Mock()
        
        self.use_case = RestaurarBanco(
            funcionario_repo=self.mock_funcionario_repo,
            ciclista_repo=self.mock_ciclista_repo,
            aluguel_repo=self.mock_aluguel_repo
        )
    
    def test_execute_sucesso(self):
        # Arrange
        # Mock dos repositórios para simular dados existentes
        self.mock_funcionario_repo.listar_todos.return_value = [Mock(), Mock()]  # 2 funcionários
        self.mock_ciclista_repo._db = {"1": Mock(), "2": Mock()}  # 2 ciclistas
        self.mock_aluguel_repo._db = {"1": Mock()}  # 1 aluguel
        
        # Act
        self.use_case.execute()
        
        # Assert
        # Verifica se os métodos de reset foram chamados
        self.mock_funcionario_repo.resetar.assert_called_once()
        self.mock_ciclista_repo.resetar.assert_called_once()
        self.mock_aluguel_repo.resetar.assert_called_once()
