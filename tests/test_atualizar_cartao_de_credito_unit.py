import pytest
from unittest.mock import Mock
from datetime import datetime
from fastapi import HTTPException

from app.use_cases.atualizar_cartao_de_credito import AtualizarCartaoDeCredito
from app.domain.entities.ciclista import NovoCartaoDeCredito

class TestAtualizarCartaoDeCredito:
    def setup_method(self):
        self.mock_repository = Mock()
        self.mock_externo_repo = Mock()
        self.use_case = AtualizarCartaoDeCredito(self.mock_repository, self.mock_externo_repo)
    
    def test_execute_sucesso(self):
        # Arrange
        id_ciclista = 1
        
        # Mock do ciclista existente
        ciclista_mock = Mock()
        ciclista_mock.id = id_ciclista
        ciclista_mock.email = "joao@teste.com"
        ciclista_mock.cartaoDeCredito = Mock()
        self.mock_repository.buscar_por_id.return_value = ciclista_mock
        
        # Mock do novo cartão
        novo_cartao = NovoCartaoDeCredito(
            nomeTitular="João Silva Atualizado",
            numero="4222222222222222",
            validade=datetime(2025, 12, 31).date(),
            cvv="456"
        )
        
        # Mock do email enviado
        self.mock_externo_repo.enviar_email.return_value = {"status": "enviado"}
        
        # Act
        result = self.use_case.execute(id_ciclista, novo_cartao)
        
        # Assert
        self.mock_repository.buscar_por_id.assert_called_once_with(id_ciclista)
        self.mock_externo_repo.enviar_email.assert_called_once_with(
            email="joao@teste.com",
            assunto="Cadstro  realizado com sucesso",
            mensagem="Seu cadastro foi realizado. Clique no link para ativar sua conta."
        )
        self.mock_repository.atualizar.assert_called_once()
        
        # Verifica se o cartão foi atualizado corretamente
        assert result is not None
        assert result.nomeTitular == "João Silva Atualizado"
        assert result.numero == "4222222222222222"
        assert result.validade == datetime(2025, 12, 31).date()
        assert result.cvv == "456"
    
    def test_execute_ciclista_inexistente(self):
        # Arrange
        id_ciclista = 999
        
        # Mock do repository para simular ciclista não encontrado
        self.mock_repository.buscar_por_id.return_value = None
        
        novo_cartao = NovoCartaoDeCredito(
            nomeTitular="Teste",
            numero="4111111111111111",
            validade=datetime(2025, 12, 31).date(),
            cvv="123"
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(id_ciclista, novo_cartao)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail["codigo"] == "404"
        assert exc_info.value.detail["mensagem"] == "Ciclista não encontrado"
        
        # Verifica que não houve chamadas adicionais
        self.mock_repository.buscar_por_id.assert_called_once_with(id_ciclista)
        self.mock_externo_repo.enviar_email.assert_not_called()
        self.mock_repository.atualizar.assert_not_called()
    