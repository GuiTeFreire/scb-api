import pytest
from app.use_cases.atualizar_cartao_de_credito import AtualizarCartaoDeCredito
from app.infra.repositories.fake_ciclista_repository import fake_ciclista_repository
from app.domain.entities.ciclista import NovoCiclista, CartaoDeCredito, Ciclista, NovoCartaoDeCredito, StatusEnum
from fastapi import HTTPException
from datetime import date
from app.infra.repositories.fake_externo_repository import fake_externo_repository

@pytest.fixture(autouse=True)
def reset_repo():
    fake_ciclista_repository.resetar()

def test_atualizar_cartao_com_sucesso():
    novo_ciclista = NovoCiclista(
        nome="Cartão Update",
        nascimento=date(1990, 1, 1),
        cpf="88888888888",
        nacionalidade="BRASILEIRO",
        email="update@cartao.com",
        senha="senha123",
        urlFotoDocumento="https://site.com/doc.png"
    )
    cartao = CartaoDeCredito(
        id=1,
        nomeTitular="Cartão Update",
        numero="4111111111111111",
        validade=date(2026, 10, 1),
        cvv="123"
    )
    ciclista = Ciclista(
        **novo_ciclista.model_dump(),
        id=0,
        cartaoDeCredito=cartao,
        status=StatusEnum.ATIVO
    )
    ciclista = fake_ciclista_repository.salvar(ciclista)

    use_case = AtualizarCartaoDeCredito(fake_ciclista_repository, fake_externo_repository)
    update = NovoCartaoDeCredito(
        nomeTitular="Nome Atualizado",
        numero="4222222222222",
        validade=date(2027, 1, 1),
        cvv="456"
    )
    resultado = use_case.execute(ciclista.id, update)
    assert resultado.nomeTitular == "Nome Atualizado"
    assert resultado.numero == "4222222222222"
    assert resultado.validade == date(2027, 1, 1)
    assert resultado.cvv == "456"

def test_atualizar_cartao_ciclista_inexistente():
    use_case = AtualizarCartaoDeCredito(fake_ciclista_repository, fake_externo_repository)
    update = NovoCartaoDeCredito(
        nomeTitular="Inexistente",
        numero="4000000000000",
        validade=date(2027, 1, 1),
        cvv="123"
    )
    with pytest.raises(HTTPException) as exc:
        use_case.execute(999, update)
    assert exc.value.status_code == 404
