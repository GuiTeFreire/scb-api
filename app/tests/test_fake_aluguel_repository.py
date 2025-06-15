from app.infra.repositories.fake_aluguel_repository import fake_aluguel_repository
from app.domain.entities.aluguel import Aluguel
from datetime import datetime


def test_listar_alugueis_retorna_alugueis_existentes():
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
