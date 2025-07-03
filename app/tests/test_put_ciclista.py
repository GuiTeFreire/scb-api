import pytest
from app.use_cases.atualizar_ciclista import AtualizarCiclista
from app.use_cases.cadastrar_ciclista import CadastrarCiclista
from app.infra.repositories.fake_ciclista_repository import fake_ciclista_repository
from app.infra.repositories.fake_externo_repository import fake_externo_repository
from app.domain.entities.ciclista import EdicaoCiclista, RequisicaoCadastroCiclista
from fastapi import HTTPException
from datetime import date

@pytest.fixture(autouse=True)
def reset_repo():
    fake_ciclista_repository.resetar()

def test_edicao_ciclista_com_sucesso():
    use_case_cadastro = CadastrarCiclista(fake_ciclista_repository, fake_externo_repository)
    payload = RequisicaoCadastroCiclista(
        ciclista={
            "nome": "Ana Original",
            "nascimento": date(1992, 3, 10),
            "cpf": "12345678901",
            "nacionalidade": "BRASILEIRO",
            "email": "ana@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://example.com/doc.png"
        },
        meioDePagamento={
            "nomeTitular": "Ana Original",
            "numero": "4111111111111111",
            "validade": date(2026, 10, 1),
            "cvv": "123"
        }
    )
    ciclista = use_case_cadastro.execute(payload)
    use_case_edicao = AtualizarCiclista(fake_ciclista_repository)
    novo_dados = EdicaoCiclista(
        nome="Ana Editada",
        nascimento=date(1992, 3, 10),
        cpf="12345678901",
        nacionalidade="BRASILEIRO",
        email="ana-editada@teste.com",
        urlFotoDocumento="https://example.com/doc-novo.png"
    )
    resultado = use_case_edicao.execute(ciclista.id, novo_dados)
    assert resultado.nome == "Ana Editada"
    assert resultado.email == "ana-editada@teste.com"

def test_edicao_ciclista_inexistente():
    use_case_edicao = AtualizarCiclista(fake_ciclista_repository)
    novo_dados = EdicaoCiclista(
        nome="Fulano",
        nascimento=date(2000, 1, 1),
        cpf="11111111111",
        nacionalidade="BRASILEIRO",
        email="fulano@teste.com",
        urlFotoDocumento=None
    )
    with pytest.raises(HTTPException) as exc:
        use_case_edicao.execute(99999, novo_dados)
    assert exc.value.status_code == 404

def test_edicao_ciclista_com_cpf_e_passaporte():
    use_case_cadastro = CadastrarCiclista(fake_ciclista_repository, fake_externo_repository)
    payload = RequisicaoCadastroCiclista(
        ciclista={
            "nome": "Fulano",
            "nascimento": date(1990, 1, 1),
            "cpf": "88888888888",
            "nacionalidade": "BRASILEIRO",
            "email": "duplicado@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://example.com/doc.png"
        },
        meioDePagamento={
            "nomeTitular": "Fulano",
            "numero": "4111111111111111",
            "validade": date(2026, 10, 1),
            "cvv": "123"
        }
    )
    ciclista = use_case_cadastro.execute(payload)
    use_case_edicao = AtualizarCiclista(fake_ciclista_repository)
    novo_dados = EdicaoCiclista(
        nome="Fulano",
        nascimento=date(1990, 1, 1),
        cpf="88888888888",
        passaporte={
            "numero": "XP123456",
            "validade": date(2030, 1, 1),
            "pais": "US"
        },
        nacionalidade="ESTRANGEIRO",
        email="duplicado@teste.com",
        urlFotoDocumento="https://example.com/doc2.png"
    )
    with pytest.raises(HTTPException) as exc:
        use_case_edicao.execute(ciclista.id, novo_dados)
    assert exc.value.status_code == 422
