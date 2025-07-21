import pytest
from unittest.mock import Mock
from fastapi import HTTPException
from datetime import date

from app.use_cases.buscar_bicicleta_alugada import BuscarBicicletaAlugada
from app.domain.entities.ciclista import Ciclista, StatusEnum, Passaporte, CartaoDeCredito
from app.domain.entities.aluguel import Aluguel
from app.domain.entities.bicicleta import Bicicleta, StatusBicicletaEnum


class TestBuscarBicicletaAlugada:
    def setup_method(self):
        self.aluguel_repo = Mock()
        self.ciclista_repo = Mock()
        self.equipamento_repo = Mock()
        self.use_case = BuscarBicicletaAlugada(
            self.aluguel_repo,
            self.ciclista_repo,
            self.equipamento_repo
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

    def test_execute_sem_aluguel_ativo(self):
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
        self.aluguel_repo.listar.return_value = []

        # Act
        result = self.use_case.execute(ciclista_id)

        # Assert
        assert result is None
        self.ciclista_repo.buscar_por_id.assert_called_once_with(ciclista_id)
        self.aluguel_repo.listar.assert_called_once()

    def test_execute_com_aluguel_ativo_mas_sem_dados_bicicleta(self):
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
        aluguel = Aluguel(
            ciclista=ciclista_id,
            trancaInicio=1,
            bicicleta=1,
            horaInicio="2024-01-01T10:00:00",
            trancaFim=None,
            horaFim=None,
            cobranca=None
        )
        
        self.ciclista_repo.buscar_por_id.return_value = ciclista
        self.aluguel_repo.listar.return_value = [aluguel]
        self.equipamento_repo.obter_bicicleta.return_value = None

        # Act
        result = self.use_case.execute(ciclista_id)

        # Assert
        assert result is None
        self.ciclista_repo.buscar_por_id.assert_called_once_with(ciclista_id)
        self.aluguel_repo.listar.assert_called_once()
        self.equipamento_repo.obter_bicicleta.assert_called_once_with(1)

    def test_execute_com_aluguel_ativo_e_dados_bicicleta(self):
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
        aluguel = Aluguel(
            ciclista=ciclista_id,
            trancaInicio=1,
            bicicleta=1,
            horaInicio="2024-01-01T10:00:00",
            trancaFim=None,
            horaFim=None,
            cobranca=None
        )
        bicicleta_data = {
            "id": 1,
            "marca": "Caloi",
            "modelo": "Mountain Bike",
            "ano": "2020",
            "numero": 12345,
            "status": "EM_USO"
        }
        
        self.ciclista_repo.buscar_por_id.return_value = ciclista
        self.aluguel_repo.listar.return_value = [aluguel]
        self.equipamento_repo.obter_bicicleta.return_value = bicicleta_data

        # Act
        result = self.use_case.execute(ciclista_id)

        # Assert
        assert result is not None
        assert isinstance(result, Bicicleta)
        assert result.id == 1
        assert result.marca == "Caloi"
        assert result.modelo == "Mountain Bike"
        assert result.ano == "2020"
        assert result.numero == 12345
        assert result.status == StatusBicicletaEnum.EM_USO
        
        self.ciclista_repo.buscar_por_id.assert_called_once_with(ciclista_id)
        self.aluguel_repo.listar.assert_called_once()
        self.equipamento_repo.obter_bicicleta.assert_called_once_with(1)

    def test_execute_com_aluguel_finalizado(self):
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
        aluguel_finalizado = Aluguel(
            ciclista=ciclista_id,
            trancaInicio=1,
            bicicleta=1,
            horaInicio="2024-01-01T10:00:00",
            trancaFim=2,
            horaFim="2024-01-01T11:00:00",
            cobranca=None
        )
        
        self.ciclista_repo.buscar_por_id.return_value = ciclista
        self.aluguel_repo.listar.return_value = [aluguel_finalizado]

        # Act
        result = self.use_case.execute(ciclista_id)

        # Assert
        assert result is None
        self.ciclista_repo.buscar_por_id.assert_called_once_with(ciclista_id)
        self.aluguel_repo.listar.assert_called_once()
        self.equipamento_repo.obter_bicicleta.assert_not_called()
