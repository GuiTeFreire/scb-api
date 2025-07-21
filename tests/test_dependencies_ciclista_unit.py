from unittest.mock import Mock, patch

from app.use_cases.cadastrar_ciclista import CadastrarCiclista
from app.use_cases.buscar_ciclista_por_id import BuscarCiclistaPorId
from app.use_cases.atualizar_ciclista import AtualizarCiclista
from app.use_cases.ativar_ciclista import AtivarCiclista
from app.use_cases.obter_cartao_de_credito import ObterCartaoDeCredito
from app.use_cases.atualizar_cartao_de_credito import AtualizarCartaoDeCredito
from app.use_cases.verificar_email_existente import VerificarEmailExistente

class TestDependenciesCiclista:
    def setup_method(self):
        self.mock_ciclista_repo = Mock()
        self.mock_externo_repo = Mock()
    
    # Remover patches/asserções de fake_externo_repository

    def test_get_cadastrar_ciclista_use_case(self):
        # Arrange
        # mock_ciclista_repo.return_value = self.mock_ciclista_repo
        # mock_externo_repo.return_value = self.mock_externo_repo
        
        # Act
        from app.dependencies.ciclista import get_cadastrar_ciclista_use_case
        use_case = get_cadastrar_ciclista_use_case()
        
        # Assert
        assert isinstance(use_case, CadastrarCiclista)
        assert hasattr(use_case, 'repository')
        assert hasattr(use_case, 'externo_repo')
    
    def test_get_buscar_ciclista_use_case(self):
        # Arrange
        # mock_ciclista_repo.return_value = self.mock_ciclista_repo
        
        # Act
        from app.dependencies.ciclista import get_buscar_ciclista_use_case
        use_case = get_buscar_ciclista_use_case()
        
        # Assert
        assert isinstance(use_case, BuscarCiclistaPorId)
        assert hasattr(use_case, 'repository')
    
    def test_get_atualizar_ciclista_use_case(self):
        # Arrange
        # mock_ciclista_repo.return_value = self.mock_ciclista_repo
        
        # Act
        from app.dependencies.ciclista import get_atualizar_ciclista_use_case
        use_case = get_atualizar_ciclista_use_case()
        
        # Assert
        assert isinstance(use_case, AtualizarCiclista)
        assert hasattr(use_case, 'repository')
    
    def test_get_ativar_ciclista_use_case(self):
        # Arrange
        # mock_ciclista_repo.return_value = self.mock_ciclista_repo
        # mock_externo_repo.return_value = self.mock_externo_repo
        
        # Act
        from app.dependencies.ciclista import get_ativar_ciclista_use_case
        use_case = get_ativar_ciclista_use_case()
        
        # Assert
        assert isinstance(use_case, AtivarCiclista)
        assert hasattr(use_case, 'repository')
    
    def test_get_obter_cartao_use_case(self):
        # Arrange
        # mock_ciclista_repo.return_value = self.mock_ciclista_repo
        
        # Act
        from app.dependencies.ciclista import get_obter_cartao_use_case
        use_case = get_obter_cartao_use_case()
        
        # Assert
        assert isinstance(use_case, ObterCartaoDeCredito)
        assert hasattr(use_case, 'repository')
    
    def test_get_atualizar_cartao_use_case(self):
        # Arrange
        # mock_ciclista_repo.return_value = self.mock_ciclista_repo
        # mock_externo_repo.return_value = self.mock_externo_repo
        
        # Act
        from app.dependencies.ciclista import get_atualizar_cartao_use_case
        use_case = get_atualizar_cartao_use_case()
        
        # Assert
        assert isinstance(use_case, AtualizarCartaoDeCredito)
        assert hasattr(use_case, 'repository')
        assert hasattr(use_case, 'externo_repo')
    
    def test_get_verificar_email_use_case(self):
        # Arrange
        # mock_ciclista_repo.return_value = self.mock_ciclista_repo
        
        # Act
        from app.dependencies.ciclista import get_verificar_email_use_case
        use_case = get_verificar_email_use_case()
        
        # Assert
        assert isinstance(use_case, VerificarEmailExistente)
        assert hasattr(use_case, 'repository') 