import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException

from app.use_cases.realizar_aluguel import RealizarAluguel
from app.domain.entities.aluguel import NovoAluguel
from app.domain.entities.ciclista import StatusEnum

class TestRealizarAluguel:
    def setup_method(self):
        self.mock_aluguel_repo = Mock()
        self.mock_ciclista_repo = Mock()
        self.mock_externo_repo = Mock()
        self.mock_equipamento_repo = Mock()
        
        # Mock padrão para cobrança aprovada
        self.mock_externo_repo.realizar_cobranca.return_value = {
            "status": "APROVADA",
            "id_cobranca": 123
        }
        
        # Mock padrão para envio de email
        self.mock_externo_repo.enviar_email.return_value = None
        
        # Mock padrão para salvamento
        self.mock_aluguel_repo.salvar.return_value = Mock()
    
    def test_execute_sucesso(self):
        # Arrange
        dados = NovoAluguel(ciclista=1, trancaInicio=123)
        
        # Mock do ciclista ativo
        ciclista_mock = Mock()
        ciclista_mock.status = StatusEnum.ATIVO
        ciclista_mock.email = "teste@email.com"
        self.mock_ciclista_repo.buscar_por_id.return_value = ciclista_mock
        
        # Mock da verificação de permissão
        with patch('app.use_cases.realizar_aluguel.VerificarPermissaoAluguel') as mock_verificador_class:
            mock_verificador = Mock()
            mock_verificador.execute.return_value = True
            mock_verificador_class.return_value = mock_verificador
            
            # Mock da tranca ocupada
            self.mock_equipamento_repo.obter_tranca.return_value = {"status": "OCUPADA"}
            
            # Mock da bicicleta na tranca
            self.mock_equipamento_repo.obter_bicicleta_na_tranca.return_value = {"id": 456}
            
            # Mock da bicicleta disponível
            self.mock_equipamento_repo.obter_bicicleta.return_value = {"status": "DISPONIVEL"}
            
            # Criar use case com mocks
            use_case = RealizarAluguel(
                self.mock_aluguel_repo,
                self.mock_ciclista_repo,
                self.mock_externo_repo,
                self.mock_equipamento_repo
            )
            
            # Act
            result = use_case.execute(dados)
            
            # Assert
            self.mock_ciclista_repo.buscar_por_id.assert_called_once_with(1)
            mock_verificador.execute.assert_called_once_with(1)
            self.mock_equipamento_repo.obter_tranca.assert_called_once_with(123)
            self.mock_equipamento_repo.obter_bicicleta_na_tranca.assert_called_once_with(123)
            self.mock_equipamento_repo.obter_bicicleta.assert_called_once_with(456)
            self.mock_externo_repo.realizar_cobranca.assert_called_once_with(1, 10.00)
            self.mock_externo_repo.incluir_cobranca_fila.assert_not_called()  # Não deve ser chamado quando aprovada
            self.mock_equipamento_repo.alterar_status_bicicleta.assert_called_once_with(456, "EM_USO")
            self.mock_equipamento_repo.alterar_status_tranca.assert_called_once_with(123, "LIVRE")
            self.mock_externo_repo.enviar_email.assert_called_once()
            self.mock_aluguel_repo.salvar.assert_called_once()
            assert result is not None
    
    def test_execute_erro_tranca_invalida(self):
        # Arrange
        dados = NovoAluguel(ciclista=1, trancaInicio=0)
        
        # Criar use case com mocks
        use_case = RealizarAluguel(
            self.mock_aluguel_repo,
            self.mock_ciclista_repo,
            self.mock_externo_repo,
            self.mock_equipamento_repo
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            use_case.execute(dados)
        
        assert exc_info.value.status_code == 422
        assert exc_info.value.detail == "Número da tranca inválido"
    
    def test_execute_erro_ciclista_inexistente(self):
        # Arrange
        dados = NovoAluguel(ciclista=1, trancaInicio=123)
        
        # Mock do ciclista não encontrado
        self.mock_ciclista_repo.buscar_por_id.return_value = None
        
        # Criar use case com mocks
        use_case = RealizarAluguel(
            self.mock_aluguel_repo,
            self.mock_ciclista_repo,
            self.mock_externo_repo,
            self.mock_equipamento_repo
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            use_case.execute(dados)
        
        assert exc_info.value.status_code == 422
        assert exc_info.value.detail == "Ciclista não existe"
        self.mock_ciclista_repo.buscar_por_id.assert_called_once_with(1)
    
    def test_execute_erro_ciclista_inativo(self):
        # Arrange
        dados = NovoAluguel(ciclista=1, trancaInicio=123)
        
        # Mock do ciclista inativo
        ciclista_mock = Mock()
        ciclista_mock.status = StatusEnum.AGUARDANDO_CONFIRMACAO
        self.mock_ciclista_repo.buscar_por_id.return_value = ciclista_mock
        
        # Criar use case com mocks
        use_case = RealizarAluguel(
            self.mock_aluguel_repo,
            self.mock_ciclista_repo,
            self.mock_externo_repo,
            self.mock_equipamento_repo
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            use_case.execute(dados)
        
        assert exc_info.value.status_code == 422
        assert exc_info.value.detail == "Ciclista não está ativo"
        self.mock_ciclista_repo.buscar_por_id.assert_called_once_with(1)
    
    def test_execute_erro_aluguel_ativo(self):
        # Arrange
        dados = NovoAluguel(ciclista=1, trancaInicio=123)
        
        # Mock do ciclista ativo
        ciclista_mock = Mock()
        ciclista_mock.status = StatusEnum.ATIVO
        self.mock_ciclista_repo.buscar_por_id.return_value = ciclista_mock
        
        # Mock da verificação de permissão retornando False
        with patch('app.use_cases.realizar_aluguel.VerificarPermissaoAluguel') as mock_verificador_class:
            mock_verificador = Mock()
            mock_verificador.execute.return_value = False
            mock_verificador_class.return_value = mock_verificador
            
            # Criar use case com mocks
            use_case = RealizarAluguel(
                self.mock_aluguel_repo,
                self.mock_ciclista_repo,
                self.mock_externo_repo,
                self.mock_equipamento_repo
            )
            
            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                use_case.execute(dados)
            
            assert exc_info.value.status_code == 422
            assert exc_info.value.detail == "Ciclista já possui aluguel ativo"
            mock_verificador.execute.assert_called_once_with(1)
    
    def test_execute_erro_tranca_nao_encontrada(self):
        # Arrange
        dados = NovoAluguel(ciclista=1, trancaInicio=123)
        
        # Mock do ciclista ativo
        ciclista_mock = Mock()
        ciclista_mock.status = StatusEnum.ATIVO
        self.mock_ciclista_repo.buscar_por_id.return_value = ciclista_mock
        
        # Mock da verificação de permissão
        with patch('app.use_cases.realizar_aluguel.VerificarPermissaoAluguel') as mock_verificador_class:
            mock_verificador = Mock()
            mock_verificador.execute.return_value = True
            mock_verificador_class.return_value = mock_verificador
            
            # Mock da tranca não encontrada
            self.mock_equipamento_repo.obter_tranca.return_value = None
            
            # Criar use case com mocks
            use_case = RealizarAluguel(
                self.mock_aluguel_repo,
                self.mock_ciclista_repo,
                self.mock_externo_repo,
                self.mock_equipamento_repo
            )
            
            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                use_case.execute(dados)
            
            assert exc_info.value.status_code == 422
            assert exc_info.value.detail == "Tranca não encontrada"
            self.mock_equipamento_repo.obter_tranca.assert_called_once_with(123)
    
    def test_execute_erro_tranca_nao_ocupada(self):
        # Arrange
        dados = NovoAluguel(ciclista=1, trancaInicio=123)
        
        # Mock do ciclista ativo
        ciclista_mock = Mock()
        ciclista_mock.status = StatusEnum.ATIVO
        self.mock_ciclista_repo.buscar_por_id.return_value = ciclista_mock
        
        # Mock da verificação de permissão
        with patch('app.use_cases.realizar_aluguel.VerificarPermissaoAluguel') as mock_verificador_class:
            mock_verificador = Mock()
            mock_verificador.execute.return_value = True
            mock_verificador_class.return_value = mock_verificador
            
            # Mock da tranca livre
            self.mock_equipamento_repo.obter_tranca.return_value = {"status": "LIVRE"}
            
            # Criar use case com mocks
            use_case = RealizarAluguel(
                self.mock_aluguel_repo,
                self.mock_ciclista_repo,
                self.mock_externo_repo,
                self.mock_equipamento_repo
            )
            
            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                use_case.execute(dados)
            
            assert exc_info.value.status_code == 422
            assert exc_info.value.detail == "Tranca não está ocupada"
            self.mock_equipamento_repo.obter_tranca.assert_called_once_with(123)
    
    def test_execute_erro_bicicleta_em_reparo(self):
        # Arrange
        dados = NovoAluguel(ciclista=1, trancaInicio=123)
        
        # Mock do ciclista ativo
        ciclista_mock = Mock()
        ciclista_mock.status = StatusEnum.ATIVO
        self.mock_ciclista_repo.buscar_por_id.return_value = ciclista_mock
        
        # Mock da verificação de permissão
        with patch('app.use_cases.realizar_aluguel.VerificarPermissaoAluguel') as mock_verificador_class:
            mock_verificador = Mock()
            mock_verificador.execute.return_value = True
            mock_verificador_class.return_value = mock_verificador
            
            # Mock da tranca ocupada
            self.mock_equipamento_repo.obter_tranca.return_value = {"status": "OCUPADA"}
            
            # Mock da bicicleta na tranca
            self.mock_equipamento_repo.obter_bicicleta_na_tranca.return_value = {"id": 456}
            
            # Mock da bicicleta em reparo
            self.mock_equipamento_repo.obter_bicicleta.return_value = {"status": "EM_REPARO"}
            
            # Criar use case com mocks
            use_case = RealizarAluguel(
                self.mock_aluguel_repo,
                self.mock_ciclista_repo,
                self.mock_externo_repo,
                self.mock_equipamento_repo
            )
            
            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                use_case.execute(dados)
            
            assert exc_info.value.status_code == 422
            assert exc_info.value.detail == "Bicicleta em reparo ou aposentada"
            self.mock_equipamento_repo.obter_bicicleta.assert_called_once_with(456)

    def test_execute_cobranca_reprovada(self):
        # Arrange
        dados = NovoAluguel(ciclista=1, trancaInicio=123)
        
        # Criar mocks específicos para este teste
        aluguel_repo = Mock()
        ciclista_repo = Mock()
        externo_repo = Mock()
        equipamento_repo = Mock()
        
        # Mock do ciclista ativo
        ciclista_mock = Mock()
        ciclista_mock.status = StatusEnum.ATIVO
        ciclista_mock.email = "teste@email.com"
        ciclista_repo.buscar_por_id.return_value = ciclista_mock
        
        # Mock da verificação de permissão
        with patch('app.use_cases.realizar_aluguel.VerificarPermissaoAluguel') as mock_verificador_class:
            mock_verificador = Mock()
            mock_verificador.execute.return_value = True
            mock_verificador_class.return_value = mock_verificador
            
            # Mock da tranca ocupada
            equipamento_repo.obter_tranca.return_value = {"status": "OCUPADA"}
            
            # Mock da bicicleta na tranca
            equipamento_repo.obter_bicicleta_na_tranca.return_value = {"id": 456}
            
            # Mock da bicicleta disponível
            equipamento_repo.obter_bicicleta.return_value = {"status": "DISPONIVEL"}
            
            # Mock da cobrança NÃO aprovada
            externo_repo.realizar_cobranca.return_value = {"status": "REJEITADA"}
            
            # Mock do salvamento
            aluguel_repo.salvar.return_value = Mock()
            
            # Criar use case com mocks
            use_case = RealizarAluguel(
                aluguel_repo,
                ciclista_repo,
                externo_repo,
                equipamento_repo
            )
            
            # Act
            result = use_case.execute(dados)
            
            # Assert
            externo_repo.incluir_cobranca_fila.assert_called_once_with(1, 10.00)
            assert result is not None

    def test_execute_cobranca_aprovada(self):
        # Arrange
        dados = NovoAluguel(ciclista=1, trancaInicio=123)
        
        # Criar mocks específicos para este teste
        aluguel_repo = Mock()
        ciclista_repo = Mock()
        externo_repo = Mock()
        equipamento_repo = Mock()
        
        # Mock do ciclista ativo
        ciclista_mock = Mock()
        ciclista_mock.status = StatusEnum.ATIVO
        ciclista_mock.email = "teste@email.com"
        ciclista_repo.buscar_por_id.return_value = ciclista_mock
        
        # Mock da verificação de permissão
        with patch('app.use_cases.realizar_aluguel.VerificarPermissaoAluguel') as mock_verificador_class:
            mock_verificador = Mock()
            mock_verificador.execute.return_value = True
            mock_verificador_class.return_value = mock_verificador
            
            # Mock da tranca ocupada
            equipamento_repo.obter_tranca.return_value = {"status": "OCUPADA"}
            
            # Mock da bicicleta na tranca
            equipamento_repo.obter_bicicleta_na_tranca.return_value = {"id": 456}
            
            # Mock da bicicleta disponível
            equipamento_repo.obter_bicicleta.return_value = {"status": "DISPONIVEL"}
            
            # Mock da cobrança APROVADA (linha 53)
            externo_repo.realizar_cobranca.return_value = {
                "status": "APROVADA",
                "id_cobranca": 999
            }
            
            # Mock do salvamento
            aluguel_repo.salvar.return_value = Mock()
            
            # Criar use case com mocks
            use_case = RealizarAluguel(
                aluguel_repo,
                ciclista_repo,
                externo_repo,
                equipamento_repo
            )
            
            # Act
            result = use_case.execute(dados)
            
            # Assert
            externo_repo.incluir_cobranca_fila.assert_not_called()
            assert result is not None

    def test_execute_erro_nenhuma_bicicleta_na_tranca(self):
        # Arrange
        dados = NovoAluguel(ciclista=1, trancaInicio=123)
        
        # Mock do ciclista ativo
        ciclista_mock = Mock()
        ciclista_mock.status = StatusEnum.ATIVO
        self.mock_ciclista_repo.buscar_por_id.return_value = ciclista_mock
        
        # Mock da verificação de permissão
        with patch('app.use_cases.realizar_aluguel.VerificarPermissaoAluguel') as mock_verificador_class:
            mock_verificador = Mock()
            mock_verificador.execute.return_value = True
            mock_verificador_class.return_value = mock_verificador
            
            # Mock da tranca ocupada
            self.mock_equipamento_repo.obter_tranca.return_value = {"status": "OCUPADA"}
            
            # Mock da bicicleta na tranca retornando None
            self.mock_equipamento_repo.obter_bicicleta_na_tranca.return_value = None
            
            # Criar use case com mocks
            use_case = RealizarAluguel(
                self.mock_aluguel_repo,
                self.mock_ciclista_repo,
                self.mock_externo_repo,
                self.mock_equipamento_repo
            )
            
            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                use_case.execute(dados)
            
            assert exc_info.value.status_code == 422
            assert exc_info.value.detail == "Nenhuma bicicleta encontrada na tranca"
            self.mock_equipamento_repo.obter_bicicleta_na_tranca.assert_called_once_with(123)

    def test_execute_erro_bicicleta_nao_encontrada(self):
        # Arrange
        dados = NovoAluguel(ciclista=1, trancaInicio=123)
        
        # Mock do ciclista ativo
        ciclista_mock = Mock()
        ciclista_mock.status = StatusEnum.ATIVO
        self.mock_ciclista_repo.buscar_por_id.return_value = ciclista_mock
        
        # Mock da verificação de permissão
        with patch('app.use_cases.realizar_aluguel.VerificarPermissaoAluguel') as mock_verificador_class:
            mock_verificador = Mock()
            mock_verificador.execute.return_value = True
            mock_verificador_class.return_value = mock_verificador
            
            # Mock da tranca ocupada
            self.mock_equipamento_repo.obter_tranca.return_value = {"status": "OCUPADA"}
            
            # Mock da bicicleta na tranca
            self.mock_equipamento_repo.obter_bicicleta_na_tranca.return_value = {"id": 456}
            
            # Mock da bicicleta não encontrada
            self.mock_equipamento_repo.obter_bicicleta.return_value = None
            
            # Criar use case com mocks
            use_case = RealizarAluguel(
                self.mock_aluguel_repo,
                self.mock_ciclista_repo,
                self.mock_externo_repo,
                self.mock_equipamento_repo
            )
            
            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                use_case.execute(dados)
            
            assert exc_info.value.status_code == 422
            assert exc_info.value.detail == "Bicicleta não encontrada"
            self.mock_equipamento_repo.obter_bicicleta.assert_called_once_with(456) 