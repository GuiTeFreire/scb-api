import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.use_cases.ativar_ciclista import AtivarCiclista
from app.infra.repositories.fake_ciclista_repository import fake_ciclista_repository
from app.domain.entities.ciclista import NovoCiclista, CartaoDeCredito, Ciclista, StatusEnum, NovoCartaoDeCredito
from app.use_cases.cadastrar_ciclista import CadastrarCiclista
from app.infra.repositories.fake_externo_repository import fake_externo_repository
from app.domain.entities.ciclista import RequisicaoCadastroCiclista
from datetime import date

@pytest.fixture(autouse=True)
def reset_repo():
    fake_ciclista_repository.resetar()

# Função auxiliar para criar payloads de cadastro nos testes
def _criar_payload_cadastro(cpf=None, passaporte=None, email="user@sucesso.com", numero_cartao="4111111111111111"):
    ciclista = {
        "nome": "Usuário Sucesso",
        "nascimento": date(1985, 7, 20),
        "nacionalidade": "BRASILEIRO",
        "email": email,
        "senha": "senha123",
        "urlFotoDocumento": "https://example.com/foto.png"
    }
    if cpf:
        ciclista["cpf"] = cpf
    if passaporte:
        ciclista["passaporte"] = passaporte

    return RequisicaoCadastroCiclista(
        ciclista=ciclista,
        meioDePagamento={
            "nomeTitular": "Usuário Sucesso",
            "numero": numero_cartao,
            "validade": date(2026, 10, 1),
            "cvv": "123"
        }
    )

def test_cadastro_ciclista_brasileiro_com_sucesso():
    # Setup: Cria payload para ciclista brasileiro
    use_case = CadastrarCiclista(fake_ciclista_repository, fake_externo_repository)
    payload = _criar_payload_cadastro(cpf="12345678901", email="brasileiro@sucesso.com")
    
    # Execução: Cadastra o ciclista
    ciclista = use_case.execute(payload)
    
    # Verificação: Confirma que o cadastro foi realizado com sucesso
    assert ciclista.email == "brasileiro@sucesso.com"
    assert ciclista.status == "AGUARDANDO_CONFIRMACAO"

def test_cadastro_ciclista_estrangeiro_com_sucesso():
    # Setup: Cria payload para ciclista estrangeiro
    use_case = CadastrarCiclista(fake_ciclista_repository, fake_externo_repository)
    passaporte = {"numero": "XPT123", "validade": date(2030, 12, 31), "pais": "US"}
    payload = _criar_payload_cadastro(passaporte=passaporte, email="estrangeiro@sucesso.com")
    
    # Execução: Cadastra o ciclista
    ciclista = use_case.execute(payload)
    
    # Verificação: Confirma que o cadastro foi realizado com sucesso
    assert ciclista.email == "estrangeiro@sucesso.com"
    assert ciclista.status == "AGUARDANDO_CONFIRMACAO"

def test_ativar_ciclista_sucesso():
    # Setup: Cria e salva um ciclista para ativação
    novo_ciclista = NovoCiclista(
        nome="Clara Ativa",
        nascimento=date(1995, 1, 1),
        cpf="77777777777",
        nacionalidade="BRASILEIRO",
        email="clara@ativar.com",
        senha="segura123",
        urlFotoDocumento="https://site.com/doc.png"
    )
    cartao = CartaoDeCredito(
        id=1,
        nomeTitular="Clara Ativa",
        numero="4111111111111111",
        validade=date(2026, 12, 1),
        cvv="123"
    )
    ciclista = Ciclista(
        **novo_ciclista.model_dump(),
        id=0,
        cartaoDeCredito=cartao
    )
    ciclista = fake_ciclista_repository.salvar(ciclista)
    
    # Execução: Ativa o ciclista
    use_case = AtivarCiclista(fake_ciclista_repository)
    ciclista_ativado = use_case.execute(ciclista.id)
    
    # Verificação: Confirma que o status foi alterado para ATIVO
    assert ciclista_ativado.status == StatusEnum.ATIVO

def test_ativar_ciclista_inexistente():
    # Setup: Prepara use case para ativação
    use_case = AtivarCiclista(fake_ciclista_repository)
    id_inexistente = 99999
    
    # Execução: Tenta ativar ciclista inexistente
    with pytest.raises(HTTPException) as exc:
        use_case.execute(id_inexistente)
    
    # Verificação: Confirma erro 404 com mensagem apropriada
    assert exc.value.status_code == 404
    assert exc.value.detail == "Ciclista não encontrado"

def test_erro_cpf_e_passaporte_ao_mesmo_tempo():
    # Setup: Cria payload com CPF e passaporte simultaneamente
    use_case = CadastrarCiclista(fake_ciclista_repository, fake_externo_repository)
    passaporte = {"numero": "XPTO999", "validade": "2031-01-01", "pais": "US"}
    payload = _criar_payload_cadastro(cpf="12345678900", passaporte=passaporte, email="duplo@regra.com")
    
    # Execução: Tenta cadastrar com ambos os documentos
    with pytest.raises(HTTPException) as exc:
        use_case.execute(payload)
    
    # Verificação: Confirma erro 422 (regra de negócio violada)
    assert exc.value.status_code == 422

def test_erro_sem_cpf_e_sem_passaporte():
    # Setup: Cria payload sem CPF e sem passaporte
    use_case = CadastrarCiclista(fake_ciclista_repository, fake_externo_repository)
    payload = _criar_payload_cadastro(cpf=None, passaporte=None, email="vazio@regra.com")
    
    # Execução: Tenta cadastrar sem documento
    with pytest.raises(HTTPException) as exc:
        use_case.execute(payload)
    
    # Verificação: Confirma erro 422 (regra de negócio violada)
    assert exc.value.status_code == 422

def test_erro_email_duplicado():
    # Setup: Cadastra primeiro ciclista
    use_case = CadastrarCiclista(fake_ciclista_repository, fake_externo_repository)
    payload = _criar_payload_cadastro(cpf="98765432100", email="duplicado@regra.com")
    use_case.execute(payload)
    
    # Execução: Tenta cadastrar segundo ciclista com mesmo email
    with pytest.raises(HTTPException) as exc:
        use_case.execute(payload)
    
    # Verificação: Confirma erro 422 (email duplicado)
    assert exc.value.status_code == 422

def test_erro_cartao_numero_invalido():
    # Setup: Prepara use case para cadastro
    use_case = CadastrarCiclista(fake_ciclista_repository, fake_externo_repository)
    
    # Execução: Tenta cadastrar com número de cartão inválido
    with pytest.raises(ValidationError):
        payload = _criar_payload_cadastro(cpf="12312312399", email="cartao@regra.com", numero_cartao="abcdefg")
        use_case.execute(payload)

def test_email_invalido():
    # Execução: Tenta criar payload com email inválido
    with pytest.raises(ValidationError):
        _criar_payload_cadastro(cpf="12345678901", email="invalid-email")

def test_cvv_invalido():
    # Execução: Tenta criar cartão com CVV inválido
    with pytest.raises(ValidationError):
        NovoCartaoDeCredito(
            nomeTitular="CVV Inválido",
            numero="4111111111111111",
            validade=date(2026, 12, 31),
            cvv="12"
        )