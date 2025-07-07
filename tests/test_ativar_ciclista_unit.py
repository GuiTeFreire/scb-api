import pytest
from unittest.mock import Mock
from fastapi import HTTPException

from app.use_cases.ativar_ciclista import AtivarCiclista
from app.domain.entities.ciclista import StatusEnum

class TestAtivarCiclista:
    def setup_method(self):
        self.mock_repository = Mock()
        self.use_case = AtivarCiclista(self.mock_repository)
    
    def test_execute_sucesso(self):
        # Arrange
        id_ciclista = 1
        ciclista_mock = Mock()
        ciclista_mock.status = StatusEnum.AGUARDANDO_CONFIRMACAO
        ciclista_mock.model_dump.return_value = {"id": 1, "status": StatusEnum.ATIVO}
        
        self.mock_repository.buscar_por_id.return_value = ciclista_mock
        self.mock_repository.atualizar.return_value = ciclista_mock
        
        # Act
        result = self.use_case.execute(id_ciclista)
        
        # Assert
        self.mock_repository.buscar_por_id.assert_called_once_with(id_ciclista)
        self.mock_repository.atualizar.assert_called_once_with(id_ciclista, ciclista_mock.model_dump())
        assert ciclista_mock.status == StatusEnum.ATIVO
        assert result is not None
    
    def test_execute_ciclista_inexistente(self):
        # Arrange
        id_ciclista = 999
        
        # Mock do repository para simular ciclista não encontrado
        self.mock_repository.buscar_por_id.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(id_ciclista)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Ciclista não encontrado"
        self.mock_repository.buscar_por_id.assert_called_once_with(id_ciclista)
        # Verifica que atualizar não foi chamado
        self.mock_repository.atualizar.assert_not_called()
    