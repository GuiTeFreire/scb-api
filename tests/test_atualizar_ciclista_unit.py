import pytest
from unittest.mock import Mock
from fastapi import HTTPException
from datetime import date

from app.use_cases.atualizar_ciclista import AtualizarCiclista
from app.domain.entities.ciclista import EdicaoCiclista

class TestAtualizarCiclista:
    def setup_method(self):
        self.mock_repository = Mock()
        self.mock_externo_repo = Mock()
        self.use_case = AtualizarCiclista(self.mock_repository, self.mock_externo_repo)
        
        # Mock do envio de email
        self.mock_externo_repo.enviar_email.return_value = None
    
    def test_execute_sucesso_com_cpf(self):
        # Arrange
        id_ciclista = 1
        dados = EdicaoCiclista(
            nome="João Silva",
            nascimento=date(1990, 1, 1),
            cpf="12345678901",
            nacionalidade="BRASILEIRO",
            email="joao@teste.com",
            senha="senha123",
            urlFotoDocumento="https://exemplo.com/foto.jpg"
        )
        
        # Mock do repository para simular atualização bem-sucedida
        ciclista_mock = Mock()
        ciclista_mock.email = "joao@teste.com"
        self.mock_repository.atualizar.return_value = ciclista_mock
        
        # Act
        result = self.use_case.execute(id_ciclista, dados)
        
        # Assert
        self.mock_repository.atualizar.assert_called_once_with(id_ciclista, dados.model_dump())
        self.mock_externo_repo.enviar_email.assert_called_once()
        assert result is not None
    
    def test_execute_sucesso_com_passaporte(self):
        # Arrange
        id_ciclista = 2
        dados = EdicaoCiclista(
            nome="John Smith",
            nascimento=date(1990, 1, 1),
            passaporte={"numero": "ABC123", "validade": date(2030, 12, 31), "pais": "US"},
            nacionalidade="AMERICANO",
            email="john@teste.com",
            senha="senha123",
            urlFotoDocumento="https://exemplo.com/foto.jpg"
        )
        
        # Mock do repository para simular atualização bem-sucedida
        ciclista_mock = Mock()
        ciclista_mock.email = "john@teste.com"
        self.mock_repository.atualizar.return_value = ciclista_mock
        
        # Act
        result = self.use_case.execute(id_ciclista, dados)
        
        # Assert
        self.mock_repository.atualizar.assert_called_once_with(id_ciclista, dados.model_dump())
        self.mock_externo_repo.enviar_email.assert_called_once()
        assert result is not None
    
    def test_execute_erro_cpf_e_passaporte_simultaneos(self):
        # Arrange
        id_ciclista = 3
        dados = EdicaoCiclista(
            nome="João Silva",
            nascimento=date(1990, 1, 1),
            cpf="12345678901",
            passaporte={"numero": "ABC123", "validade": date(2030, 12, 31), "pais": "US"},
            nacionalidade="BRASILEIRO",
            email="joao@teste.com",
            senha="senha123",
            urlFotoDocumento="https://exemplo.com/foto.jpg"
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(id_ciclista, dados)
        
        assert exc_info.value.status_code == 422
        # Verifica que repository não foi chamado
        self.mock_repository.atualizar.assert_not_called()
    
    def test_execute_erro_sem_cpf_e_sem_passaporte(self):
        # Arrange
        id_ciclista = 4
        dados = EdicaoCiclista(
            nome="João Silva",
            nascimento=date(1990, 1, 1),
            nacionalidade="BRASILEIRO",
            email="joao@teste.com",
            senha="senha123",
            urlFotoDocumento="https://exemplo.com/foto.jpg"
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(id_ciclista, dados)
        
        assert exc_info.value.status_code == 422
        # Verifica que repository não foi chamado
        self.mock_repository.atualizar.assert_not_called()
    
    def test_execute_erro_ciclista_inexistente(self):
        # Arrange
        id_ciclista = 999
        dados = EdicaoCiclista(
            nome="João Silva",
            nascimento=date(1990, 1, 1),
            cpf="12345678901",
            nacionalidade="BRASILEIRO",
            email="joao@teste.com",
            senha="senha123",
            urlFotoDocumento="https://exemplo.com/foto.jpg"
        )
        
        # Mock do repository para simular ciclista não encontrado
        self.mock_repository.atualizar.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(id_ciclista, dados)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Ciclista não encontrado"
        self.mock_repository.atualizar.assert_called_once_with(id_ciclista, dados.model_dump())
        # Verifica que email não foi enviado
        self.mock_externo_repo.enviar_email.assert_not_called()
