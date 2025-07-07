import pytest
from unittest.mock import Mock, patch

from app.use_cases.realizar_aluguel import RealizarAluguel
from app.use_cases.realizar_devolucao import RealizarDevolucao
from app.use_cases.buscar_bicicleta_alugada import BuscarBicicletaAlugada
from app.use_cases.verificar_permissao_aluguel import VerificarPermissaoAluguel

class TestDependenciesAluguel:
    def setup_method(self):
        self.mock_aluguel_repo = Mock()
        self.mock_ciclista_repo = Mock()
        self.mock_externo_repo = Mock()
        self.mock_equipamento_repo = Mock()
    
    @patch('app.dependencies.aluguel.fake_aluguel_repository')
    @patch('app.dependencies.aluguel.fake_ciclista_repository')
    @patch('app.dependencies.aluguel.fake_externo_repository')
    @patch('app.dependencies.aluguel.fake_equipamento_repository')

    def test_get_realizar_aluguel_use_case(self, mock_equipamento_repo, mock_externo_repo, mock_ciclista_repo, mock_aluguel_repo):
        # Arrange
        mock_aluguel_repo.return_value = self.mock_aluguel_repo
        mock_ciclista_repo.return_value = self.mock_ciclista_repo
        mock_externo_repo.return_value = self.mock_externo_repo
        mock_equipamento_repo.return_value = self.mock_equipamento_repo
        
        # Act
        from app.dependencies.aluguel import get_realizar_aluguel_use_case
        use_case = get_realizar_aluguel_use_case()
        
        # Assert
        assert isinstance(use_case, RealizarAluguel)
        assert hasattr(use_case, 'aluguel_repo')
        assert hasattr(use_case, 'ciclista_repo')
        assert hasattr(use_case, 'externo_repo')
        assert hasattr(use_case, 'equipamento_repo')
    
    @patch('app.dependencies.aluguel.fake_aluguel_repository')
    @patch('app.dependencies.aluguel.fake_ciclista_repository')
    @patch('app.dependencies.aluguel.fake_externo_repository')
    @patch('app.dependencies.aluguel.fake_equipamento_repository')

    def test_get_realizar_devolucao_use_case(self, mock_equipamento_repo, mock_externo_repo, mock_ciclista_repo, mock_aluguel_repo):
        # Arrange
        mock_aluguel_repo.return_value = self.mock_aluguel_repo
        mock_ciclista_repo.return_value = self.mock_ciclista_repo
        mock_externo_repo.return_value = self.mock_externo_repo
        mock_equipamento_repo.return_value = self.mock_equipamento_repo
        
        # Act
        from app.dependencies.aluguel import get_realizar_devolucao_use_case
        use_case = get_realizar_devolucao_use_case()
        
        # Assert
        assert isinstance(use_case, RealizarDevolucao)
        assert hasattr(use_case, 'aluguel_repo')
        assert hasattr(use_case, 'ciclista_repo')
        assert hasattr(use_case, 'servico_externo_repo')
        assert hasattr(use_case, 'equipamento_repo')
    
    @patch('app.dependencies.aluguel.fake_aluguel_repository')

    def test_get_buscar_bicicleta_alugada_use_case(self, mock_aluguel_repo):
        # Arrange
        mock_aluguel_repo.return_value = self.mock_aluguel_repo
        
        # Act
        from app.dependencies.aluguel import get_buscar_bicicleta_alugada_use_case
        use_case = get_buscar_bicicleta_alugada_use_case()
        
        # Assert
        assert isinstance(use_case, BuscarBicicletaAlugada)
        assert hasattr(use_case, 'aluguel_repo')
        assert hasattr(use_case, 'ciclista_repo')
        assert hasattr(use_case, 'equipamento_repo')
    
    @patch('app.dependencies.aluguel.fake_aluguel_repository')
    @patch('app.dependencies.aluguel.fake_ciclista_repository')

    def test_get_verificar_permissao_aluguel_use_case(self, mock_ciclista_repo, mock_aluguel_repo):
        # Arrange
        mock_aluguel_repo.return_value = self.mock_aluguel_repo
        mock_ciclista_repo.return_value = self.mock_ciclista_repo
        
        # Act
        from app.dependencies.aluguel import get_verificar_permissao_aluguel_use_case
        use_case = get_verificar_permissao_aluguel_use_case()
        
        # Assert
        assert isinstance(use_case, VerificarPermissaoAluguel)
        assert hasattr(use_case, 'aluguel_repo')
        assert hasattr(use_case, 'ciclista_repo') 