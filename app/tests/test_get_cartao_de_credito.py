import pytest
from app.use_cases.obter_cartao_de_credito import ObterCartaoDeCredito
from app.infra.repositories.fake_ciclista_repository import fake_ciclista_repository
from app.domain.entities.ciclista import NovoCiclista, CartaoDeCredito, Ciclista
from fastapi import HTTPException
from datetime import date

@pytest.fixture(autouse=True)
def reset_repo():
    fake_ciclista_repository.resetar()

def test_get_cartao_credito_sucesso():
    novo_ciclista = NovoCiclista(
        nome="Carlos",
        nascimento=date(1980, 1, 1),
        cpf="12345678901",
        nacionalidade="BRASILEIRO",
        email="carlos@bike.com",
        senha="senha123",
        urlFotoDocumento="https://foto.com/doc.png"
    )
    cartao = CartaoDeCredito(
        id=1,
        nomeTitular="Carlos",
        numero="4111111111111111",
        validade=date(2026, 10, 1),
        cvv="123"
    )
    ciclista = Ciclista(
        **novo_ciclista.model_dump(),
        id=0,
        cartaoDeCredito=cartao
    )
    ciclista = fake_ciclista_repository.salvar(ciclista)
    use_case = ObterCartaoDeCredito(fake_ciclista_repository)

    cartao_retornado = use_case.execute(ciclista.id)

    assert cartao_retornado.nomeTitular == "Carlos"

def test_get_cartao_credito_erro_ciclista_nao_encontrado():
    use_case = ObterCartaoDeCredito(fake_ciclista_repository)
    id_inexistente = 999

    with pytest.raises(HTTPException) as exc:
        use_case.execute(id_inexistente)
    assert exc.value.status_code == 404

def test_get_cartao_credito_id_invalido():
    use_case = ObterCartaoDeCredito(fake_ciclista_repository)
    id_invalido = "abc"

    with pytest.raises(Exception):
        use_case.execute(id_invalido)