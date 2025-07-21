import pytest
from unittest.mock import Mock
from fastapi import HTTPException
from datetime import date

from app.use_cases.verificar_permissao_aluguel import VerificarPermissaoAluguel
from app.domain.entities.ciclista import Ciclista, StatusEnum, Passaporte, CartaoDeCredito


class TestVerificarPermissaoAluguelCenariosAdicionais:
    def setup_method(self):
        self.ciclista_repo = Mock()
        self.aluguel_repo = Mock()
        self.use_case = VerificarPermissaoAluguel(
            self.ciclista_repo,
            self.aluguel_repo
        )

    def test_execute_ciclista_nao_encontrado(self):
        # Arrange
        ciclista_id = 1
        self.ciclista_repo.buscar_por_id.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(ciclista_id)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == {"codigo": "404", "mensagem": "Ciclista não encontrado"}
        self.ciclista_repo.buscar_por_id.assert_called_once_with(ciclista_id)
        self.aluguel_repo.tem_aluguel_ativo.assert_not_called()

    def test_execute_ciclista_inativo(self):
        # Arrange
        ciclista_id = 1
        passaporte = Passaporte(
            numero="AB123456",
            validade=date(2030, 12, 31),
            pais="Brasil"
        )
        cartao = CartaoDeCredito(
            id=1,
            nomeTitular="João Silva",
            numero="1234567890123456",
            validade="12/2025",
            cvv="123"
        )
        ciclista = Ciclista(
            id=ciclista_id,
            nome="João",
            nascimento=date(1990, 1, 1),
            cpf="12345678901",
            passaporte=passaporte,
            nacionalidade="Brasileiro",
            email="joao@email.com",
            urlFotoDocumento="http://foto.com",
            senha="senha123",
            status=StatusEnum.INATIVO,
            cartaoDeCredito=cartao
        )
        self.ciclista_repo.buscar_por_id.return_value = ciclista

        # Act
        result = self.use_case.execute(ciclista_id)

        # Assert
        assert result is False
        self.ciclista_repo.buscar_por_id.assert_called_once_with(ciclista_id)
        self.aluguel_repo.tem_aluguel_ativo.assert_not_called()

    def test_execute_ciclista_ativo_com_aluguel_ativo(self):
        # Arrange
        ciclista_id = 1
        passaporte = Passaporte(
            numero="AB123456",
            validade=date(2030, 12, 31),
            pais="Brasil"
        )
        cartao = CartaoDeCredito(
            id=1,
            nomeTitular="João Silva",
            numero="1234567890123456",
            validade="12/2025",
            cvv="123"
        )
        ciclista = Ciclista(
            id=ciclista_id,
            nome="João",
            nascimento=date(1990, 1, 1),
            cpf="12345678901",
            passaporte=passaporte,
            nacionalidade="Brasileiro",
            email="joao@email.com",
            urlFotoDocumento="http://foto.com",
            senha="senha123",
            status=StatusEnum.ATIVO,
            cartaoDeCredito=cartao
        )
        self.ciclista_repo.buscar_por_id.return_value = ciclista
        self.aluguel_repo.tem_aluguel_ativo.return_value = True

        # Act
        result = self.use_case.execute(ciclista_id)

        # Assert
        assert result is False
        self.ciclista_repo.buscar_por_id.assert_called_once_with(ciclista_id)
        self.aluguel_repo.tem_aluguel_ativo.assert_called_once_with(ciclista_id)

    def test_execute_ciclista_ativo_sem_aluguel_ativo(self):
        # Arrange
        ciclista_id = 1
        passaporte = Passaporte(
            numero="AB123456",
            validade=date(2030, 12, 31),
            pais="Brasil"
        )
        cartao = CartaoDeCredito(
            id=1,
            nomeTitular="João Silva",
            numero="1234567890123456",
            validade="12/2025",
            cvv="123"
        )
        ciclista = Ciclista(
            id=ciclista_id,
            nome="João",
            nascimento=date(1990, 1, 1),
            cpf="12345678901",
            passaporte=passaporte,
            nacionalidade="Brasileiro",
            email="joao@email.com",
            urlFotoDocumento="http://foto.com",
            senha="senha123",
            status=StatusEnum.ATIVO,
            cartaoDeCredito=cartao
        )
        self.ciclista_repo.buscar_por_id.return_value = ciclista
        self.aluguel_repo.tem_aluguel_ativo.return_value = False

        # Act
        result = self.use_case.execute(ciclista_id)

        # Assert
        assert result is True
        self.ciclista_repo.buscar_por_id.assert_called_once_with(ciclista_id)
        self.aluguel_repo.tem_aluguel_ativo.assert_called_once_with(ciclista_id) 