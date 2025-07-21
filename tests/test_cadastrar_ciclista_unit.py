import pytest
from unittest.mock import Mock
from fastapi import HTTPException
from datetime import date

from app.use_cases.cadastrar_ciclista import CadastrarCiclista
from app.domain.entities.ciclista import RequisicaoCadastroCiclista

class TestCadastrarCiclista:
    def setup_method(self):
        self.mock_repository = Mock()
        self.mock_externo_repo = Mock()
        self.use_case = CadastrarCiclista(self.mock_repository, self.mock_externo_repo)
        
        # Mock do próximo ID
        self.mock_repository.proximo_id.return_value = 1
        
        # Mock da validação de cartão
        self.mock_externo_repo.validar_cartao_credito.return_value = {"valido": True, "mensagem": "OK"}
        
        # Mock do envio de email
        self.mock_externo_repo.enviar_email.return_value = None
        
        # Mock do salvamento
        self.mock_repository.salvar.return_value = Mock()
    
    def test_execute_sucesso_ciclista_brasileiro(self):
        # Arrange
        payload = RequisicaoCadastroCiclista(
            ciclista={
                "nome": "João Silva",
                "nascimento": date(1990, 1, 1),
                "cpf": "12345678901",
                "nacionalidade": "BRASILEIRO",
                "email": "joao@teste.com",
                "senha": "senha123",
                "urlFotoDocumento": "https://exemplo.com/foto.jpg"
            },
            meioDePagamento={
                "nomeTitular": "João Silva",
                "numero": "4111111111111111",
                "validade": "12/2025",
                "cvv": "123"
            }
        )
        
        # Mock do repository para simular email não existente
        self.mock_repository.buscar_por_email.return_value = None
        
        # Act
        result = self.use_case.execute(payload)
        
        # Assert
        self.mock_repository.buscar_por_email.assert_called_once_with("joao@teste.com")
        self.mock_externo_repo.validar_cartao_credito.assert_called_once()
        self.mock_externo_repo.enviar_email.assert_called_once()
        self.mock_repository.salvar.assert_called_once()
        assert result is not None
    
    def test_execute_erro_cpf_e_passaporte_simultaneos(self):
        # Arrange
        payload = RequisicaoCadastroCiclista(
            ciclista={
                "nome": "João Silva",
                "nascimento": date(1990, 1, 1),
                "cpf": "12345678901",
                "passaporte": {"numero": "ABC123", "validade": date(2030, 12, 31), "pais": "US"},
                "nacionalidade": "BRASILEIRO",
                "email": "joao@teste.com",
                "senha": "senha123",
                "urlFotoDocumento": "https://exemplo.com/foto.jpg"
            },
            meioDePagamento={
                "nomeTitular": "João Silva",
                "numero": "4111111111111111",
                "validade": "12/2025",
                "cvv": "123"
            }
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(payload)
        
        assert exc_info.value.status_code == 422
        assert "Informe apenas CPF ou Passaporte" in exc_info.value.detail
    
    def test_execute_erro_sem_cpf_e_sem_passaporte(self):
        # Arrange
        payload = RequisicaoCadastroCiclista(
            ciclista={
                "nome": "João Silva",
                "nascimento": date(1990, 1, 1),
                "nacionalidade": "BRASILEIRO",
                "email": "joao@teste.com",
                "senha": "senha123",
                "urlFotoDocumento": "https://exemplo.com/foto.jpg"
            },
            meioDePagamento={
                "nomeTitular": "João Silva",
                "numero": "4111111111111111",
                "validade": "12/2025",
                "cvv": "123"
            }
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(payload)
        
        assert exc_info.value.status_code == 422
        assert "Informe apenas CPF ou Passaporte" in exc_info.value.detail
    
    def test_execute_erro_email_duplicado(self):
        # Arrange
        payload = RequisicaoCadastroCiclista(
            ciclista={
                "nome": "João Silva",
                "nascimento": date(1990, 1, 1),
                "cpf": "12345678901",
                "nacionalidade": "BRASILEIRO",
                "email": "joao@teste.com",
                "senha": "senha123",
                "urlFotoDocumento": "https://exemplo.com/foto.jpg"
            },
            meioDePagamento={
                "nomeTitular": "João Silva",
                "numero": "4111111111111111",
                "validade": "12/2025",
                "cvv": "123"
            }
        )
        
        # Mock do repository para simular email existente
        self.mock_repository.buscar_por_email.return_value = Mock()
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(payload)
        
        assert exc_info.value.status_code == 422
        assert exc_info.value.detail == "E-mail já cadastrado"
        self.mock_repository.buscar_por_email.assert_called_once_with("joao@teste.com")
    
    def test_execute_erro_cartao_invalido(self):
        # Arrange
        payload = RequisicaoCadastroCiclista(
            ciclista={
                "nome": "João Silva",
                "nascimento": date(1990, 1, 1),
                "cpf": "12345678901",
                "nacionalidade": "BRASILEIRO",
                "email": "joao@teste.com",
                "senha": "senha123",
                "urlFotoDocumento": "https://exemplo.com/foto.jpg"
            },
            meioDePagamento={
                "nomeTitular": "João Silva",
                "numero": "4111111111111111",
                "validade": "12/2025",
                "cvv": "123"
            }
        )
        
        # Mock do repository para simular email não existente
        self.mock_repository.buscar_por_email.return_value = None
        
        # Mock da validação de cartão para retornar inválido
        self.mock_externo_repo.validar_cartao_credito.return_value = {
            "valido": False, 
            "mensagem": "Cartão expirado"
        }
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(payload)
        
        assert exc_info.value.status_code == 422
        assert "Cartão de crédito inválido" in exc_info.value.detail
        self.mock_externo_repo.validar_cartao_credito.assert_called_once()
    
    def test_execute_sucesso_ciclista_estrangeiro(self):
        # Arrange
        payload = RequisicaoCadastroCiclista(
            ciclista={
                "nome": "John Smith",
                "nascimento": date(1990, 1, 1),
                "passaporte": {"numero": "ABC123", "validade": date(2030, 12, 31), "pais": "US"},
                "nacionalidade": "AMERICANO",
                "email": "john@teste.com",
                "senha": "senha123",
                "urlFotoDocumento": "https://exemplo.com/foto.jpg"
            },
            meioDePagamento={
                "nomeTitular": "John Smith",
                "numero": "4111111111111111",
                "validade": "12/2025",
                "cvv": "123"
            }
        )
        
        # Mock do repository para simular email não existente
        self.mock_repository.buscar_por_email.return_value = None
        
        # Act
        result = self.use_case.execute(payload)
        
        # Assert
        self.mock_repository.buscar_por_email.assert_called_once_with("john@teste.com")
        self.mock_externo_repo.validar_cartao_credito.assert_called_once()
        self.mock_externo_repo.enviar_email.assert_called_once()
        self.mock_repository.salvar.assert_called_once()
        assert result is not None 