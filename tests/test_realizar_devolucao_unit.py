import pytest
from unittest.mock import Mock
from datetime import datetime, timedelta
from fastapi import HTTPException

from app.use_cases.realizar_devolucao import RealizarDevolucao

class TestRealizarDevolucao:
    def setup_method(self):
        self.mock_aluguel_repo = Mock()
        self.mock_ciclista_repo = Mock()
        self.mock_externo_repo = Mock()
        self.mock_equipamento_repo = Mock()
        
        self.use_case = RealizarDevolucao(
            self.mock_aluguel_repo,
            self.mock_ciclista_repo,
            self.mock_externo_repo,
            self.mock_equipamento_repo
        )
    
    def test_execute_sucesso(self):
        # Arrange
        id_bicicleta = 5678
        id_tranca = 201
        
        # Mock do payload
        payload = Mock()
        payload.idBicicleta = id_bicicleta
        payload.idTranca = id_tranca
        
        # Mock do aluguel ativo
        aluguel_mock = Mock()
        aluguel_mock.bicicleta = id_bicicleta
        aluguel_mock.horaFim = None
        aluguel_mock.horaInicio = datetime.now() - timedelta(hours=1)
        aluguel_mock.ciclista = 1
        aluguel_mock.cobranca = 10.00
        
        self.mock_aluguel_repo.listar.return_value = [aluguel_mock]
        
        # Mock do ciclista
        ciclista_mock = Mock()
        ciclista_mock.email = "joao@teste.com"
        self.mock_ciclista_repo.buscar_por_id.return_value = ciclista_mock
        
        # Act
        result = self.use_case.execute(payload)
        
        # Assert
        assert result.bicicleta == id_bicicleta
        assert result.trancaFim == id_tranca
        assert result.horaFim is not None
        assert result.cobranca == 10
        assert result.ciclista == 1
        
        # Verifica chamadas aos repositories
        self.mock_equipamento_repo.trancar_tranca.assert_called_once_with(id_tranca, id_bicicleta)
        self.mock_externo_repo.enviar_email.assert_called_once()
    
    def test_execute_bicicleta_invalida_none(self):
        # Arrange
        payload = Mock()
        payload.idBicicleta = None
        payload.idTranca = 201
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(payload)
        
        assert exc_info.value.status_code == 422
        assert exc_info.value.detail == "Número da bicicleta inválido"
    
    def test_execute_bicicleta_invalida_zero(self):
        # Arrange
        payload = Mock()
        payload.idBicicleta = 0
        payload.idTranca = 201
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(payload)
        
        assert exc_info.value.status_code == 422
        assert exc_info.value.detail == "Número da bicicleta inválido"
    
    def test_execute_bicicleta_invalida_negativa(self):
        # Arrange
        payload = Mock()
        payload.idBicicleta = -1
        payload.idTranca = 201
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(payload)
        
        assert exc_info.value.status_code == 422
        assert exc_info.value.detail == "Número da bicicleta inválido"
    
    def test_execute_bicicleta_nao_alugada(self):
        # Arrange
        payload = Mock()
        payload.idBicicleta = 9999
        payload.idTranca = 201
        
        # Mock do repository para simular bicicleta não alugada
        self.mock_aluguel_repo.listar.return_value = []
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(payload)
        
        assert exc_info.value.status_code == 422
        assert exc_info.value.detail == "Bicicleta não está alugada"
    
    def test_execute_bicicleta_ja_devolvida(self):
        # Arrange
        payload = Mock()
        payload.idBicicleta = 5678
        payload.idTranca = 201
        
        # Mock do aluguel já finalizado
        aluguel_mock = Mock()
        aluguel_mock.bicicleta = 5678
        aluguel_mock.horaFim = datetime.now()
        
        self.mock_aluguel_repo.listar.return_value = [aluguel_mock]
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.execute(payload)
        
        assert exc_info.value.status_code == 422
        assert exc_info.value.detail == "Bicicleta não está alugada"
    
    def test_execute_com_valor_extra(self):
        # Arrange
        id_bicicleta = 5678
        id_tranca = 201
        
        payload = Mock()
        payload.idBicicleta = id_bicicleta
        payload.idTranca = id_tranca
        
        # Mock do aluguel com tempo excedido (3 horas)
        aluguel_mock = Mock()
        aluguel_mock.bicicleta = id_bicicleta
        aluguel_mock.horaFim = None
        aluguel_mock.horaInicio = datetime.now() - timedelta(hours=3)
        aluguel_mock.ciclista = 1
        aluguel_mock.cobranca = 10.00
        
        self.mock_aluguel_repo.listar.return_value = [aluguel_mock]
        
        # Mock do ciclista
        ciclista_mock = Mock()
        ciclista_mock.email = "maria@teste.com"
        self.mock_ciclista_repo.buscar_por_id.return_value = ciclista_mock

        # Mock da cobrança extra
        self.mock_externo_repo.realizar_cobranca.return_value = {'id_cobranca': 99, 'status': 'APROVADA'}

        # Act
        result = self.use_case.execute(payload)
        
        # Assert
        assert result.cobranca == 99
        
        # Verifica se a cobrança extra foi incluída na fila
    
    def test_execute_sem_valor_extra(self):
        # Arrange
        id_bicicleta = 5678
        id_tranca = 201
        
        payload = Mock()
        payload.idBicicleta = id_bicicleta
        payload.idTranca = id_tranca
        
        # Mock do aluguel dentro do tempo limite (1 hora)
        aluguel_mock = Mock()
        aluguel_mock.bicicleta = id_bicicleta
        aluguel_mock.horaFim = None
        aluguel_mock.horaInicio = datetime.now() - timedelta(hours=1)
        aluguel_mock.ciclista = 1
        aluguel_mock.cobranca = 10.00
        
        self.mock_aluguel_repo.listar.return_value = [aluguel_mock]
        
        # Mock do ciclista
        ciclista_mock = Mock()
        ciclista_mock.email = "pedro@teste.com"
        self.mock_ciclista_repo.buscar_por_id.return_value = ciclista_mock
        
        # Act
        result = self.use_case.execute(payload)
        
        # Assert
        assert result.cobranca == 10
        
        # Verifica que não houve cobrança extra
        self.mock_externo_repo.incluir_cobranca_fila.assert_not_called()
    
    def test_execute_ciclista_nao_encontrado(self):
        # Arrange
        payload = Mock()
        payload.idBicicleta = 5678
        payload.idTranca = 201
        
        aluguel_mock = Mock()
        aluguel_mock.bicicleta = 5678
        aluguel_mock.horaFim = None
        aluguel_mock.horaInicio = datetime.now() - timedelta(hours=1)
        aluguel_mock.ciclista = 999
        aluguel_mock.cobranca = 10.00
        
        self.mock_aluguel_repo.listar.return_value = [aluguel_mock]
        
        # Mock do repository para simular ciclista não encontrado
        self.mock_ciclista_repo.buscar_por_id.return_value = None
        
        # Act
        result = self.use_case.execute(payload)
        
        # Assert
        assert result is not None
        # Verifica que o email não foi enviado quando ciclista não é encontrado
        self.mock_externo_repo.enviar_email.assert_not_called() 