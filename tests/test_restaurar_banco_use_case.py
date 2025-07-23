from app.use_cases.restaurar_banco import RestaurarBanco
from app.infra.repositories import fake_funcionario_repository, fake_ciclista_repository, fake_aluguel_repository

def test_restaurar_dados_iniciais_popula_dados():
    uc = RestaurarBanco(
        funcionario_repo=fake_funcionario_repository,
        ciclista_repo=fake_ciclista_repository,
        aluguel_repo=fake_aluguel_repository
    )
    uc.restaurar_dados_iniciais()
    # Verifica funcionários
    funcionarios = fake_funcionario_repository.listar_todos()
    assert any(f.email == "employee@example.com" for f in funcionarios)
    # Verifica ciclistas
    ciclistas = fake_ciclista_repository._db
    assert any(c.email == "user@example.com" for c in ciclistas)
    # Verifica alugueis
    alugueis = fake_aluguel_repository._db
    assert any(a.ciclista == 3 for a in alugueis) 