from app.infra.repositories.fake_externo_repository import FakeExternoRepository

def test_validar_cartao_credito_valido():
    repo = FakeExternoRepository()
    result = repo.validar_cartao_credito({"numero": "4012001037141112"})
    assert result["valido"] is True

def test_validar_cartao_credito_invalido():
    repo = FakeExternoRepository()
    result = repo.validar_cartao_credito({"numero": "123"})
    assert result["valido"] is False

def test_realizar_cobranca():
    repo = FakeExternoRepository()
    result = repo.realizar_cobranca(1, 10.0)
    assert result["status"] == "APROVADA"
    assert result["valor"] == 10.0
    assert result["ciclista_id"] == 1

def test_incluir_cobranca_fila():
    repo = FakeExternoRepository()
    result = repo.incluir_cobranca_fila(2, 20.0)
    assert result["status"] == "PENDENTE"
    assert result["valor"] == 20.0
    assert result["ciclista_id"] == 2

def test_enviar_email():
    repo = FakeExternoRepository()
    result = repo.enviar_email("a@a.com", "Teste", "Mensagem")
    assert result["status"] == "ENVIADO"
    assert result["destinatario"] == "a@a.com" 