from fastapi.testclient import TestClient
from app.main import app
import pytest
from fastapi import HTTPException
from app.use_cases.realizar_aluguel import RealizarAluguel
from app.use_cases.cadastrar_ciclista import CadastrarCiclista
from app.infra.repositories import fake_aluguel_repository, fake_ciclista_repository, fake_externo_repository, fake_equipamento_repository
from app.domain.entities.aluguel import NovoAluguel
from app.domain.entities.ciclista import RequisicaoCadastroCiclista

client = TestClient(app)

def test_aluguel_sucesso():
    client.get("/restaurarBanco")

    payload_ciclista = {
        "ciclista": {
            "nome": "Lucas Alves",
            "nascimento": "1990-01-01",
            "cpf": "12345678901",
            "nacionalidade": "BRASILEIRO",
            "email": "lucas@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Lucas Alves",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_post = client.post("/ciclista", json=payload_ciclista)
    assert res_post.status_code == 201
    ciclista_id = res_post.json()["id"]

    res_ativar = client.post(f"/ciclista/{ciclista_id}/ativar")
    assert res_ativar.status_code == 200

    payload_aluguel = {
        "ciclista": ciclista_id,
        "trancaInicio": 101
    }

    res_aluguel = client.post("/aluguel", json=payload_aluguel)
    assert res_aluguel.status_code == 200
    assert res_aluguel.json()["ciclista"] == ciclista_id
    assert res_aluguel.json()["trancaInicio"] == 101
    assert res_aluguel.json()["horaFim"] is None


def test_aluguel_falha_com_aluguel_ativo():
    client.get("/restaurarBanco")

    payload_ciclista = {
        "ciclista": {
            "nome": "João Pedro",
            "nascimento": "1991-01-01",
            "cpf": "99999999999",
            "nacionalidade": "BRASILEIRO",
            "email": "joao@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "João Pedro",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_post = client.post("/ciclista", json=payload_ciclista)
    assert res_post.status_code == 201
    ciclista_id = res_post.json()["id"]

    res_ativar = client.post(f"/ciclista/{ciclista_id}/ativar")
    assert res_ativar.status_code == 200
    
    payload_aluguel = {
        "ciclista": ciclista_id,
        "trancaInicio": 102
    }

    res1 = client.post("/aluguel", json=payload_aluguel)
    print("ERRO PRIMEIRO ALUGUEL:", res1.status_code, res1.json())
    assert res1.status_code == 200

    res2 = client.post("/aluguel", json=payload_aluguel)
    assert res2.status_code == 422

def test_aluguel_falha_ciclista_inativo():
    client.get("/restaurarBanco")

    payload_ciclista = {
        "ciclista": {
            "nome": "Carlos Inativo",
            "nascimento": "1995-01-01",
            "cpf": "88888888888",
            "nacionalidade": "BRASILEIRO",
            "email": "inativo@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Carlos Inativo",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_post = client.post("/ciclista", json=payload_ciclista)
    assert res_post.status_code == 201
    ciclista_id = res_post.json()["id"]

    payload_aluguel = {
        "ciclista": ciclista_id,
        "trancaInicio": 105
    }

    res = client.post("/aluguel", json=payload_aluguel)
    assert res.status_code == 422

def test_aluguel_falha_tranca_invalida():
    client.get("/restaurarBanco")

    payload_ciclista = {
        "ciclista": {
            "nome": "Maria Tranca Invalida",
            "nascimento": "1992-01-01",
            "cpf": "77777777777",
            "nacionalidade": "BRASILEIRO",
            "email": "tranca@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Maria Tranca Invalida",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_post = client.post("/ciclista", json=payload_ciclista)
    assert res_post.status_code == 201
    ciclista_id = res_post.json()["id"]

    res_ativar = client.post(f"/ciclista/{ciclista_id}/ativar")
    assert res_ativar.status_code == 200

    # Testar com trancaInicio = 0 (inválido)
    payload_aluguel = {
        "ciclista": ciclista_id,
        "trancaInicio": 0
    }

    res = client.post("/aluguel", json=payload_aluguel)
    assert res.status_code == 422

    # Testar com trancaInicio negativo (inválido)
    payload_aluguel = {
        "ciclista": ciclista_id,
        "trancaInicio": -1
    }

    res = client.post("/aluguel", json=payload_aluguel)
    assert res.status_code == 422

def test_bicicleta_alugada_retorna_bicicleta_quando_ha_aluguel():
    client.get("/restaurarBanco")

    payload_ciclista = {
        "ciclista": {
            "nome": "Marcos Bicicleta",
            "nascimento": "1993-01-01",
            "cpf": "32132132100",
            "nacionalidade": "BRASILEIRO",
            "email": "marcos@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Marcos Bicicleta",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_post = client.post("/ciclista", json=payload_ciclista)
    assert res_post.status_code == 201
    ciclista_id = res_post.json()["id"]

    res_ativar = client.post(f"/ciclista/{ciclista_id}/ativar")
    assert res_ativar.status_code == 200

    payload_aluguel = {
        "ciclista": ciclista_id,
        "trancaInicio": 101
    }

    res_aluguel = client.post("/aluguel", json=payload_aluguel)
    assert res_aluguel.status_code == 200

    res = client.get(f"/ciclista/{ciclista_id}/bicicletaAlugada")
    assert res.status_code == 200
    assert res.json()["id"] == 5678  # mock retornado pelo sistema


def test_bicicleta_alugada_retorna_null_quando_nao_ha_aluguel():
    client.get("/restaurarBanco")

    payload_ciclista = {
        "ciclista": {
            "nome": "Lúcia Livre",
            "nascimento": "1990-05-20",
            "cpf": "55555555555",
            "nacionalidade": "BRASILEIRO",
            "email": "lucia@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Lúcia Livre",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_post = client.post("/ciclista", json=payload_ciclista)
    assert res_post.status_code == 201
    ciclista_id = res_post.json()["id"]

    res_ativar = client.post(f"/ciclista/{ciclista_id}/ativar")
    assert res_ativar.status_code == 200

    res = client.get(f"/ciclista/{ciclista_id}/bicicletaAlugada")
    assert res.status_code == 200
    assert res.json() is None


def test_bicicleta_alugada_ciclista_inexistente():
    client.get("/restaurarBanco")

    res = client.get("/ciclista/9999/bicicletaAlugada")
    assert res.status_code == 404
    assert res.json()["codigo"] == "404"

def test_permite_aluguel_retorna_true_quando_nao_tem_aluguel_ativo():
    client.get("/restaurarBanco")

    payload = {
        "ciclista": {
            "nome": "Maria Silva",
            "nascimento": "1995-01-01",
            "cpf": "12345678901",
            "nacionalidade": "BRASILEIRO",
            "email": "maria@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Maria Silva",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_post = client.post("/ciclista", json=payload)
    assert res_post.status_code == 201
    id_ciclista = res_post.json()["id"]

    res_ativar = client.post(f"/ciclista/{id_ciclista}/ativar")
    assert res_ativar.status_code == 200

    res = client.get(f"/ciclista/{id_ciclista}/permiteAluguel")
    assert res.status_code == 200
    assert res.json() is True

def test_permite_aluguel_404_para_ciclista_inexistente():
    client.get("/restaurarBanco")

    res = client.get("/ciclista/9999/permiteAluguel")
    assert res.status_code == 404

def test_permite_aluguel_retorna_false_para_ciclista_inativo():
    client.get("/restaurarBanco")

    payload = {
        "ciclista": {
            "nome": "Maria Silva",
            "nascimento": "1995-01-01",
            "cpf": "12345678901",
            "nacionalidade": "BRASILEIRO",
            "email": "maria@teste.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        "meioDePagamento": {
            "nomeTitular": "Maria Silva",
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    }

    res_post = client.post("/ciclista", json=payload)
    assert res_post.status_code == 201
    id_ciclista = res_post.json()["id"]

    res = client.get(f"/ciclista/{id_ciclista}/permiteAluguel")
    assert res.status_code == 200
    assert res.json() is False

def _criar_ciclista_ativo_para_casos_limite(nome, email, cpf):
    use_case = CadastrarCiclista(fake_ciclista_repository, fake_externo_repository)
    dados = RequisicaoCadastroCiclista(
        ciclista={
            "nome": nome,
            "nascimento": "1990-01-01",
            "cpf": cpf,
            "nacionalidade": "BRASILEIRO",
            "email": email,
            "senha": "senha123",
            "urlFotoDocumento": "https://site.com/doc.png"
        },
        meioDePagamento={
            "nomeTitular": nome,
            "numero": "4111111111111111",
            "validade": "2026-12-01",
            "cvv": "123"
        }
    )
    ciclista = use_case.execute(dados)
    ciclista.status = "ATIVO"
    return ciclista

def test_aluguel_tranca_nao_ocupada():
    fake_ciclista_repository.resetar()
    fake_aluguel_repository.resetar()
    
    ciclista = _criar_ciclista_ativo_para_casos_limite("João Teste", "joao@teste.com", "12345678901")
    
    # Mock da tranca com status LIVRE
    original_obter_tranca = fake_equipamento_repository.obter_tranca
    fake_equipamento_repository.obter_tranca = lambda id_tranca: {
        "id": id_tranca,
        "numero": id_tranca,
        "localizacao": "-22.9068,-43.1729",
        "anoDeFabricacao": "2020",
        "modelo": "MockTranca",
        "status": "LIVRE",
        "bicicleta": 5678
    }
    
    use_case = RealizarAluguel(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    dados = NovoAluguel(ciclista=ciclista.id, trancaInicio=103)
    
    with pytest.raises(HTTPException) as exc:
        use_case.execute(dados)
    
    assert exc.value.status_code == 422
    assert exc.value.detail == "Tranca não está ocupada"
    
    fake_equipamento_repository.obter_tranca = original_obter_tranca

def test_aluguel_bicicleta_em_reparo():
    fake_ciclista_repository.resetar()
    fake_aluguel_repository.resetar()
    
    ciclista = _criar_ciclista_ativo_para_casos_limite("Maria Teste", "maria@teste.com", "98765432109")
    
    # Mock da bicicleta com status EM_REPARO
    original_obter_bicicleta = fake_equipamento_repository.obter_bicicleta
    fake_equipamento_repository.obter_bicicleta = lambda id_bicicleta: {
        "id": id_bicicleta,
        "marca": "MockMarca",
        "modelo": "MockModelo",
        "ano": "2020",
        "numero": id_bicicleta,
        "status": "EM_REPARO"
    }
    
    use_case = RealizarAluguel(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    dados = NovoAluguel(ciclista=ciclista.id, trancaInicio=103)
    
    with pytest.raises(HTTPException) as exc:
        use_case.execute(dados)
    
    assert exc.value.status_code == 422
    assert exc.value.detail == "Bicicleta em reparo ou aposentada"
    
    fake_equipamento_repository.obter_bicicleta = original_obter_bicicleta

def test_aluguel_bicicleta_aposentada():
    fake_ciclista_repository.resetar()
    fake_aluguel_repository.resetar()
    
    ciclista = _criar_ciclista_ativo_para_casos_limite("Pedro Teste", "pedro@teste.com", "11122233344")
    
    # Mock da bicicleta com status APOSENTADA
    original_obter_bicicleta = fake_equipamento_repository.obter_bicicleta
    fake_equipamento_repository.obter_bicicleta = lambda id_bicicleta: {
        "id": id_bicicleta,
        "marca": "MockMarca",
        "modelo": "MockModelo",
        "ano": "2020",
        "numero": id_bicicleta,
        "status": "APOSENTADA"
    }
    
    use_case = RealizarAluguel(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    dados = NovoAluguel(ciclista=ciclista.id, trancaInicio=103)
    
    with pytest.raises(HTTPException) as exc:
        use_case.execute(dados)
    
    assert exc.value.status_code == 422
    assert exc.value.detail == "Bicicleta em reparo ou aposentada"
    
    fake_equipamento_repository.obter_bicicleta = original_obter_bicicleta

def test_aluguel_cobranca_nao_aprovada():
    fake_ciclista_repository.resetar()
    fake_aluguel_repository.resetar()
    
    ciclista = _criar_ciclista_ativo_para_casos_limite("Ana Teste", "ana@teste.com", "55566677788")
    
    # Mock da cobrança com status REJEITADA
    original_realizar_cobranca = fake_externo_repository.realizar_cobranca
    original_incluir_cobranca_fila = fake_externo_repository.incluir_cobranca_fila
    cobrancas_fila = []
    fake_externo_repository.realizar_cobranca = lambda ciclista_id, valor: {
        "id_cobranca": None,
        "status": "REJEITADA",
        "valor": valor,
        "ciclista_id": ciclista_id,
        "data_cobranca": "2024-01-01T10:00:00"
    }
    fake_externo_repository.incluir_cobranca_fila = lambda ciclista_id, valor: cobrancas_fila.append((ciclista_id, valor))
    
    use_case = RealizarAluguel(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    dados = NovoAluguel(ciclista=ciclista.id, trancaInicio=103)
    aluguel = use_case.execute(dados)
    
    assert aluguel is not None
    assert aluguel.ciclista == ciclista.id
    assert aluguel.trancaInicio == 103
    assert aluguel.cobranca is None
    assert cobrancas_fila == [(ciclista.id, 10.00)]
    
    fake_externo_repository.realizar_cobranca = original_realizar_cobranca
    fake_externo_repository.incluir_cobranca_fila = original_incluir_cobranca_fila

def test_aluguel_tranca_nao_encontrada():
    fake_ciclista_repository.resetar()
    fake_aluguel_repository.resetar()
    
    ciclista = _criar_ciclista_ativo_para_casos_limite("Tranca Falha", "tranca@falha.com", "11111111111")
    original_obter_tranca = fake_equipamento_repository.obter_tranca
    fake_equipamento_repository.obter_tranca = lambda id_tranca: None
    
    use_case = RealizarAluguel(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    dados = NovoAluguel(ciclista=ciclista.id, trancaInicio=999)
    
    with pytest.raises(HTTPException) as exc:
        use_case.execute(dados)
    
    assert exc.value.status_code == 422
    assert exc.value.detail == "Tranca não encontrada"
    fake_equipamento_repository.obter_tranca = original_obter_tranca

def test_aluguel_bicicleta_nao_encontrada_na_tranca():
    fake_ciclista_repository.resetar()
    fake_aluguel_repository.resetar()
    
    ciclista = _criar_ciclista_ativo_para_casos_limite("Sem Bike", "sembike@falha.com", "22222222222")
    original_obter_bicicleta_na_tranca = fake_equipamento_repository.obter_bicicleta_na_tranca
    fake_equipamento_repository.obter_bicicleta_na_tranca = lambda id_tranca: None
    
    use_case = RealizarAluguel(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    dados = NovoAluguel(ciclista=ciclista.id, trancaInicio=101)
    
    with pytest.raises(HTTPException) as exc:
        use_case.execute(dados)
    
    assert exc.value.status_code == 422
    assert exc.value.detail == "Nenhuma bicicleta encontrada na tranca"
    fake_equipamento_repository.obter_bicicleta_na_tranca = original_obter_bicicleta_na_tranca

def test_aluguel_bicicleta_nao_encontrada():
    fake_ciclista_repository.resetar()
    fake_aluguel_repository.resetar()
    
    ciclista = _criar_ciclista_ativo_para_casos_limite("Bike Falha", "bikefalha@falha.com", "33333333333")
    original_obter_bicicleta = fake_equipamento_repository.obter_bicicleta
    fake_equipamento_repository.obter_bicicleta = lambda id_bicicleta: None
    
    # Mock para garantir que a tranca está ocupada e tem uma bicicleta
    original_obter_tranca = fake_equipamento_repository.obter_tranca
    fake_equipamento_repository.obter_tranca = lambda id_tranca: {
        "id": id_tranca,
        "numero": id_tranca,
        "localizacao": "-22.9068,-43.1729",
        "anoDeFabricacao": "2020",
        "modelo": "MockTranca",
        "status": "OCUPADA",
        "bicicleta": 1234
    }
    original_obter_bicicleta_na_tranca = fake_equipamento_repository.obter_bicicleta_na_tranca
    fake_equipamento_repository.obter_bicicleta_na_tranca = lambda id_tranca: {"id": 1234}
    
    use_case = RealizarAluguel(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    dados = NovoAluguel(ciclista=ciclista.id, trancaInicio=101)
    
    with pytest.raises(HTTPException) as exc:
        use_case.execute(dados)
    
    assert exc.value.status_code == 422
    assert exc.value.detail == "Bicicleta não encontrada"
    
    fake_equipamento_repository.obter_bicicleta = original_obter_bicicleta
    fake_equipamento_repository.obter_tranca = original_obter_tranca
    fake_equipamento_repository.obter_bicicleta_na_tranca = original_obter_bicicleta_na_tranca