import pytest
from app.use_cases.verificar_email_existente import VerificarEmailExistente
from app.infra.repositories.fake_ciclista_repository import fake_ciclista_repository
from app.domain.entities.ciclista import NovoCiclista, CartaoDeCredito, Ciclista
from datetime import date

@pytest.fixture(autouse=True)
def reset_repo():
    fake_ciclista_repository.resetar()

def test_email_existe_true():
    novo_ciclista = NovoCiclista(
        nome="Teste Email",
        nascimento=date(1995, 1, 1),
        cpf="11111111111",
        nacionalidade="BRASILEIRO",
        email="email@existe.com",
        senha="senha123",
        urlFotoDocumento="https://example.com/doc.png"
    )
    cartao = CartaoDeCredito(
        id=1,
        nomeTitular="Teste Email",
        numero="4111111111111111",
        validade=date(2026, 12, 31),
        cvv="123"
    )
    ciclista = Ciclista(
        **novo_ciclista.model_dump(),
        id=0,
        cartaoDeCredito=cartao
    )
    fake_ciclista_repository.salvar(ciclista)
    use_case = VerificarEmailExistente(fake_ciclista_repository)

    assert use_case.execute("email@existe.com") is True

def test_email_existe_false():
    use_case = VerificarEmailExistente(fake_ciclista_repository)
    assert use_case.execute("email_inexistente@teste.com") is False
