from unittest.mock import Mock, patch

from app.use_cases.restaurar_banco import RestaurarBanco

class TestDependenciesReset:
    def setup_method(self):
        self.mock_funcionario_repo = Mock()
        self.mock_ciclista_repo = Mock()
        self.mock_aluguel_repo = Mock()
    
    @patch('app.dependencies.reset.fake_funcionario_repository')
    @patch('app.dependencies.reset.fake_ciclista_repository')
    @patch('app.dependencies.reset.fake_aluguel_repository')

    def test_get_restaurar_banco_uc(self, mock_aluguel_repo, mock_ciclista_repo, mock_funcionario_repo):
        # Arrange
        mock_funcionario_repo.return_value = self.mock_funcionario_repo
        mock_ciclista_repo.return_value = self.mock_ciclista_repo
        mock_aluguel_repo.return_value = self.mock_aluguel_repo
        
        # Act
        from app.dependencies.reset import get_restaurar_banco_uc
        use_case = get_restaurar_banco_uc()
        
        # Assert
        assert isinstance(use_case, RestaurarBanco)
        assert hasattr(use_case, 'funcionario_repo')
        assert hasattr(use_case, 'ciclista_repo')
        assert hasattr(use_case, 'aluguel_repo') 