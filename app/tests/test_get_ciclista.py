import pytest
from app.use_cases.buscar_ciclista_por_id import BuscarCiclistaPorId
from app.infra.repositories.fake_ciclista_repository import fake_ciclista_repository
from app.domain.entities.ciclista import NovoCiclista, CartaoDeCredito, Ciclista
from fastapi import HTTPException
from datetime import date

@pytest.fixture(autouse=True)
def reset_repo():
    fake_ciclista_repository.resetar()

def test_get_ciclista_sucesso():
    novo_ciclista = NovoCiclista(
        nome="Maria Teste",
        nascimento=date(1995, 6, 1),
        cpf="12345678900",
        nacionalidade="BRASILEIRO",
        email="maria@get.com",
        senha="senha123",
        urlFotoDocumento="https://foto.com/doc.png"
    )
    cartao = CartaoDeCredito(
        id=1,
        nomeTitular="Maria Teste",
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
    use_case = BuscarCiclistaPorId(fake_ciclista_repository)

    resposta = use_case.execute(ciclista.id)

    assert resposta.id == ciclista.id
    assert resposta.email == "maria@get.com"

def test_get_ciclista_nao_encontrado():
    use_case = BuscarCiclistaPorId(fake_ciclista_repository)
    id_inexistente = 99999

    with pytest.raises(HTTPException) as exc:
        use_case.execute(id_inexistente)
    assert exc.value.status_code == 404
