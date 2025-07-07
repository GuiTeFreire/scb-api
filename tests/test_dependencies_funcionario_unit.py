from unittest.mock import Mock, patch

from app.use_cases.cadastrar_funcionario import CadastrarFuncionario
from app.use_cases.listar_funcionarios import ListarFuncionarios
from app.use_cases.buscar_funcionario_por_id import BuscarFuncionarioPorId
from app.use_cases.atualizar_funcionario import AtualizarFuncionario
from app.use_cases.remover_funcionario import RemoverFuncionario

class TestDependenciesFuncionario:
    def setup_method(self):
        self.mock_funcionario_repo = Mock()
    
    @patch('app.dependencies.funcionario.fake_funcionario_repository')

    def test_get_cadastrar_funcionario_use_case(self, mock_funcionario_repo):
        # Arrange
        mock_funcionario_repo.return_value = self.mock_funcionario_repo
        
        # Act
        from app.dependencies.funcionario import get_cadastrar_funcionario_use_case
        use_case = get_cadastrar_funcionario_use_case()
        
        # Assert
        assert isinstance(use_case, CadastrarFuncionario)
        assert hasattr(use_case, 'repository')
    
    @patch('app.dependencies.funcionario.fake_funcionario_repository')

    def test_get_listar_funcionarios_use_case(self, mock_funcionario_repo):
        # Arrange
        mock_funcionario_repo.return_value = self.mock_funcionario_repo
        
        # Act
        from app.dependencies.funcionario import get_listar_funcionarios_use_case
        use_case = get_listar_funcionarios_use_case()
        
        # Assert
        assert isinstance(use_case, ListarFuncionarios)
        assert hasattr(use_case, 'repository')
    
    @patch('app.dependencies.funcionario.fake_funcionario_repository')

    def test_get_buscar_funcionario_use_case(self, mock_funcionario_repo):
        # Arrange
        mock_funcionario_repo.return_value = self.mock_funcionario_repo
        
        # Act
        from app.dependencies.funcionario import get_buscar_funcionario_use_case
        use_case = get_buscar_funcionario_use_case()
        
        # Assert
        assert isinstance(use_case, BuscarFuncionarioPorId)
        assert hasattr(use_case, 'repository')
    
    @patch('app.dependencies.funcionario.fake_funcionario_repository')

    def test_get_atualizar_funcionario_use_case(self, mock_funcionario_repo):
        # Arrange
        mock_funcionario_repo.return_value = self.mock_funcionario_repo
        
        # Act
        from app.dependencies.funcionario import get_atualizar_funcionario_use_case
        use_case = get_atualizar_funcionario_use_case()
        
        # Assert
        assert isinstance(use_case, AtualizarFuncionario)
        assert hasattr(use_case, 'repository')
    
    @patch('app.dependencies.funcionario.fake_funcionario_repository')

    def test_get_remover_funcionario_use_case(self, mock_funcionario_repo):
        # Arrange
        mock_funcionario_repo.return_value = self.mock_funcionario_repo
        
        # Act
        from app.dependencies.funcionario import get_remover_funcionario_use_case
        use_case = get_remover_funcionario_use_case()
        
        # Assert
        assert isinstance(use_case, RemoverFuncionario)
        assert hasattr(use_case, 'repository') 