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
    
    # Remover todos os decorators @patch e argumentos de mock dos testes, deixar apenas asserts simples.

    def test_get_realizar_aluguel_use_case(self):
        # Arrange
        mock_aluguel_repo = Mock()
        mock_ciclista_repo = Mock()
        mock_externo_repo = Mock()
        # mock_equipamento_repo = Mock()
        
        # Act
        from app.dependencies.aluguel import get_realizar_aluguel_use_case
        use_case = get_realizar_aluguel_use_case()
        
        # Assert
        assert isinstance(use_case, RealizarAluguel)
        assert hasattr(use_case, 'aluguel_repo')
        assert hasattr(use_case, 'ciclista_repo')
        assert hasattr(use_case, 'externo_repo')
        assert hasattr(use_case, 'equipamento_repo')
    
    def test_get_realizar_devolucao_use_case(self):
        # Arrange
        mock_aluguel_repo = Mock()
        mock_ciclista_repo = Mock()
        mock_externo_repo = Mock()
        # mock_equipamento_repo = Mock()
        
        # Act
        from app.dependencies.aluguel import get_realizar_devolucao_use_case
        use_case = get_realizar_devolucao_use_case()
        
        # Assert
        assert isinstance(use_case, RealizarDevolucao)
        assert hasattr(use_case, 'aluguel_repo')
        assert hasattr(use_case, 'ciclista_repo')
        assert hasattr(use_case, 'externo_repo')
        assert hasattr(use_case, 'equipamento_repo')
    
    def test_get_buscar_bicicleta_alugada_use_case(self):
        # Arrange
        mock_aluguel_repo = Mock()
        
        # Act
        from app.dependencies.aluguel import get_buscar_bicicleta_alugada_use_case
        use_case = get_buscar_bicicleta_alugada_use_case()
        
        # Assert
        assert isinstance(use_case, BuscarBicicletaAlugada)
        assert hasattr(use_case, 'aluguel_repo')
        assert hasattr(use_case, 'ciclista_repo')
        assert hasattr(use_case, 'equipamento_repo')
    
    def test_get_verificar_permissao_aluguel_use_case(self):
        # Arrange
        mock_aluguel_repo = Mock()
        mock_ciclista_repo = Mock()
        
        # Act
        from app.dependencies.aluguel import get_verificar_permissao_aluguel_use_case
        use_case = get_verificar_permissao_aluguel_use_case()
        
        # Assert
        assert isinstance(use_case, VerificarPermissaoAluguel)
        assert hasattr(use_case, 'aluguel_repo')
        assert hasattr(use_case, 'ciclista_repo') 