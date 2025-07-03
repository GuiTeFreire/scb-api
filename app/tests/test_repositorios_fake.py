from app.infra.repositories.fake_externo_repository import FakeExternoRepository
from app.infra.repositories.fake_funcionario_repository import fake_funcionario_repository
from app.infra.repositories.fake_aluguel_repository import fake_aluguel_repository
from app.domain.entities.funcionario import NovoFuncionario
from app.domain.entities.aluguel import Aluguel
from app.domain.repositories.equipamento_repository import EquipamentoRepository
from app.domain.repositories.externo_repository import ExternoRepository
from datetime import datetime

class TestFakeExterno:
    def setup_method(self):
        self.repository = FakeExternoRepository()
    
    def test_validar_cartao_credito_valido(self):
        cartao_data = {
            "numero": "4111111111111111",
            "nomeTitular": "João Silva",
            "validade": "2026-12-01",
            "cvv": "123"
        }
        
        resultado = self.repository.validar_cartao_credito(cartao_data)
        
        assert resultado["valido"] is True
        assert resultado["mensagem"] == "Cartão válido"
    
    def test_validar_cartao_credito_invalido_numero_curto(self):
        cartao_data = {
            "numero": "123456789",
            "nomeTitular": "João Silva",
            "validade": "2026-12-01",
            "cvv": "123"
        }
        
        resultado = self.repository.validar_cartao_credito(cartao_data)
        
        assert resultado["valido"] is False
        assert resultado["mensagem"] == "Número do cartão inválido"
    
    def test_validar_cartao_credito_invalido_nao_numerico(self):
        cartao_data = {
            "numero": "411111111111111a",
            "nomeTitular": "João Silva",
            "validade": "2026-12-01",
            "cvv": "123"
        }
        
        resultado = self.repository.validar_cartao_credito(cartao_data)
        
        assert resultado["valido"] is False
        assert resultado["mensagem"] == "Número do cartão inválido"
    
    def test_validar_cartao_credito_sem_numero(self):
        cartao_data = {
            "nomeTitular": "João Silva",
            "validade": "2026-12-01",
            "cvv": "123"
        }
        
        resultado = self.repository.validar_cartao_credito(cartao_data)
        
        assert resultado["valido"] is False
        assert resultado["mensagem"] == "Número do cartão inválido"
    
    def test_realizar_cobranca(self):
        resultado = self.repository.realizar_cobranca(123, 50.00)
        
        assert resultado["id_cobranca"] == 1234
        assert resultado["status"] == "APROVADA"
        assert resultado["valor"] == 50.00
        assert resultado["ciclista_id"] == 123
        assert "data_cobranca" in resultado
    
    def test_incluir_cobranca_fila(self):
        resultado = self.repository.incluir_cobranca_fila(456, 25.50)
        
        assert resultado["id_cobranca"] == 5678
        assert resultado["status"] == "PENDENTE"
        assert resultado["valor"] == 25.50
        assert resultado["ciclista_id"] == 456
        assert "data_inclusao" in resultado
    
    def test_enviar_email(self):
        resultado = self.repository.enviar_email(
            "teste@email.com",
            "Teste de Email",
            "Mensagem de teste"
        )
        
        assert resultado["id_email"] == 9999
        assert resultado["status"] == "ENVIADO"
        assert resultado["destinatario"] == "teste@email.com"
        assert "data_envio" in resultado

class TestFakeFuncionarioRepository:
    def test_buscar_por_email_retorna_funcionario_quando_existe(self):
        fake_funcionario_repository.resetar()
        
        dados = NovoFuncionario(
            nome="Maria Teste",
            idade=25,
            funcao="Atendente",
            cpf="12345678900",
            email="maria@teste.com",
            senha="senha123"
        )
        
        funcionario = fake_funcionario_repository.salvar(dados)
        
        resultado = fake_funcionario_repository.buscar_por_email("maria@teste.com")
        
        assert resultado is not None
        assert resultado.email == "maria@teste.com"
        assert resultado.nome == "Maria Teste"

    def test_buscar_por_email_retorna_none_quando_nao_existe(self):
        fake_funcionario_repository.resetar()
        
        resultado = fake_funcionario_repository.buscar_por_email("email_inexistente@teste.com")
        
        assert resultado is None

class TestFakeAluguelRepository:
    def test_listar_alugueis_retorna_alugueis_existentes(self):
        fake_aluguel_repository.resetar()

        aluguel = Aluguel(
            ciclista=1,
            trancaInicio=101,
            bicicleta=5678,
            horaInicio=datetime.now(),
            horaFim=None,
            trancaFim=None,
            cobranca=1234
        )

        fake_aluguel_repository.salvar(aluguel)

        resultado = fake_aluguel_repository.listar()

        assert isinstance(resultado, list)
        assert len(resultado) == 1
        assert resultado[0].ciclista == 1

class TestRepositoriosAbstratos:
    def test_equipamento_repository_metodos_abstratos(self):
        class DummyEquipamento(EquipamentoRepository):
            def obter_bicicleta(self, id_bicicleta: int):
                return EquipamentoRepository.obter_bicicleta(self, id_bicicleta)
            def obter_tranca(self, id_tranca: int):
                return EquipamentoRepository.obter_tranca(self, id_tranca)
            def alterar_status_bicicleta(self, id_bicicleta: int, status: str):
                return EquipamentoRepository.alterar_status_bicicleta(self, id_bicicleta, status)
            def alterar_status_tranca(self, id_tranca: int, status: str):
                return EquipamentoRepository.alterar_status_tranca(self, id_tranca, status)
            def obter_bicicleta_na_tranca(self, id_tranca: int):
                return EquipamentoRepository.obter_bicicleta_na_tranca(self, id_tranca)
        
        repo = DummyEquipamento()
        assert repo.obter_bicicleta(1) is None
        assert repo.obter_tranca(1) is None
        assert repo.alterar_status_bicicleta(1, "status") is None
        assert repo.alterar_status_tranca(1, "status") is None
        assert repo.obter_bicicleta_na_tranca(1) is None

    def test_externo_repository_metodos_abstratos(self):
        class DummyExterno(ExternoRepository):
            def validar_cartao_credito(self, cartao_data):
                return ExternoRepository.validar_cartao_credito(self, cartao_data)
            def realizar_cobranca(self, ciclista_id: int, valor: float):
                return ExternoRepository.realizar_cobranca(self, ciclista_id, valor)
            def incluir_cobranca_fila(self, ciclista_id: int, valor: float):
                return ExternoRepository.incluir_cobranca_fila(self, ciclista_id, valor)
            def enviar_email(self, email: str, assunto: str, mensagem: str):
                return ExternoRepository.enviar_email(self, email, assunto, mensagem)
        
        repo = DummyExterno()
        assert repo.validar_cartao_credito({}) is None
        assert repo.realizar_cobranca(1, 10.0) is None
        assert repo.incluir_cobranca_fila(1, 10.0) is None
        assert repo.enviar_email("a@a.com", "assunto", "msg") is None

    def test_equipamento_repository_implementacao(self):
        class MockEquipamentoRepository(EquipamentoRepository):
            def obter_bicicleta(self, id_bicicleta: int):
                return {"id": id_bicicleta, "status": "DISPONIVEL"}
            def obter_tranca(self, id_tranca: int):
                return {"id": id_tranca, "status": "LIVRE"}
            def alterar_status_bicicleta(self, id_bicicleta: int, status: str):
                return True
            def alterar_status_tranca(self, id_tranca: int, status: str):
                return True
            def obter_bicicleta_na_tranca(self, id_tranca: int):
                return {"id": 123, "tranca": id_tranca}
        
        repo = MockEquipamentoRepository()
        assert repo.obter_bicicleta(1) == {"id": 1, "status": "DISPONIVEL"}
        assert repo.obter_tranca(2) == {"id": 2, "status": "LIVRE"}
        assert repo.alterar_status_bicicleta(1, "ALUGADA") is True
        assert repo.alterar_status_tranca(2, "OCUPADA") is True
        assert repo.obter_bicicleta_na_tranca(2) == {"id": 123, "tranca": 2}

    def test_externo_repository_implementacao(self):
        class MockExternoRepository(ExternoRepository):
            def validar_cartao_credito(self, cartao_data):
                return {"valido": True, "mensagem": "Cartão válido"}
            def realizar_cobranca(self, ciclista_id: int, valor: float):
                return {"sucesso": True, "valor": valor}
            def incluir_cobranca_fila(self, ciclista_id: int, valor: float):
                return {"enviado": True, "valor": valor}
            def enviar_email(self, email: str, assunto: str, mensagem: str):
                return {"enviado": True, "email": email}
        
        repo = MockExternoRepository()
        assert repo.validar_cartao_credito({}) == {"valido": True, "mensagem": "Cartão válido"}
        assert repo.realizar_cobranca(1, 10.0) == {"sucesso": True, "valor": 10.0}
        assert repo.incluir_cobranca_fila(1, 5.0) == {"enviado": True, "valor": 5.0}
        assert repo.enviar_email("test@test.com", "Teste", "Mensagem") == {"enviado": True, "email": "test@test.com"}