import pytest
from fastapi import HTTPException
from app.use_cases.realizar_aluguel import RealizarAluguel
from app.use_cases.cadastrar_ciclista import CadastrarCiclista
from app.infra.repositories import fake_aluguel_repository, fake_ciclista_repository, fake_externo_repository, fake_equipamento_repository
from app.domain.entities.aluguel import NovoAluguel
from app.domain.entities.ciclista import RequisicaoCadastroCiclista, NovoCiclista, CartaoDeCredito, Ciclista, StatusEnum
from app.use_cases.verificar_permissao_aluguel import VerificarPermissaoAluguel
from app.use_cases.buscar_bicicleta_alugada import BuscarBicicletaAlugada
from datetime import date

# Função auxiliar para criar ciclistas ativos nos testes
def _criar_ciclista_ativo(nome, email, cpf):
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

def test_aluguel_sucesso():
    # Setup: Limpa repositórios e cria ciclista ativo
    fake_ciclista_repository.resetar()
    fake_aluguel_repository.resetar()
    ciclista = _criar_ciclista_ativo("Lucas Alves", "lucas@teste.com", "12345678901")
    
    # Execução: Realiza o aluguel
    use_case = RealizarAluguel(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    dados = NovoAluguel(ciclista=ciclista.id, trancaInicio=101)
    aluguel = use_case.execute(dados)
    
    # Verificação: Confirma que o aluguel foi criado corretamente
    assert aluguel.ciclista == ciclista.id
    assert aluguel.trancaInicio == 101
    assert aluguel.horaFim is None  # Aluguel ainda não foi finalizado
    assert aluguel.bicicleta is not None  # Bicicleta foi associada
    assert aluguel.cobranca == 1234  # Cobrança foi gerada

def test_aluguel_falha_com_aluguel_ativo():
    # Setup: Limpa repositórios e cria ciclista ativo
    fake_aluguel_repository.resetar()
    fake_ciclista_repository.resetar()
    ciclista = _criar_ciclista_ativo("João Pedro", "joao@teste.com", "99999999999")
    
    # Execução: Realiza primeiro aluguel (deve funcionar)
    use_case = RealizarAluguel(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    dados = NovoAluguel(ciclista=ciclista.id, trancaInicio=102)
    aluguel1 = use_case.execute(dados)
    assert aluguel1.ciclista == ciclista.id
    
    # Execução: Tenta realizar segundo aluguel (deve falhar)
    with pytest.raises(HTTPException) as exc:
        use_case.execute(dados)
    assert exc.value.status_code == 422

def test_aluguel_falha_ciclista_inativo():
    # Setup: Limpa repositórios e cria ciclista inativo
    fake_aluguel_repository.resetar()
    fake_ciclista_repository.resetar()
    novo_ciclista = NovoCiclista(
        nome="Carlos Inativo",
        nascimento=date(1995, 1, 1),
        cpf="88888888888",
        nacionalidade="BRASILEIRO",
        email="inativo@teste.com",
        senha="senha123",
        urlFotoDocumento="https://site.com/doc.png"
    )
    cartao = CartaoDeCredito(
        id=1,
        nomeTitular="Carlos Inativo",
        numero="4111111111111111",
        validade=date(2026, 12, 1),
        cvv="123"
    )
    ciclista = Ciclista(
        **novo_ciclista.model_dump(),
        id=0,
        cartaoDeCredito=cartao,
        status=StatusEnum.AGUARDANDO_CONFIRMACAO  # Status inativo
    )
    ciclista = fake_ciclista_repository.salvar(ciclista)
    
    # Execução: Tenta alugar com ciclista inativo
    use_case = RealizarAluguel(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    dados = NovoAluguel(ciclista=ciclista.id, trancaInicio=105)
    with pytest.raises(HTTPException) as exc:
        use_case.execute(dados)
    assert exc.value.status_code == 422

def test_aluguel_falha_tranca_invalida():
    # Setup: Limpa repositórios e cria ciclista ativo
    fake_aluguel_repository.resetar()
    fake_ciclista_repository.resetar()
    ciclista = _criar_ciclista_ativo("Maria Tranca Invalida", "tranca@teste.com", "77777777777")
    
    # Execução: Tenta alugar com tranca ID 0
    use_case = RealizarAluguel(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    dados1 = NovoAluguel(ciclista=ciclista.id, trancaInicio=0)
    with pytest.raises(HTTPException) as exc:
        use_case.execute(dados1)
    assert exc.value.status_code == 422
    
    # Execução: Tenta alugar com tranca ID negativo
    dados2 = NovoAluguel(ciclista=ciclista.id, trancaInicio=-1)
    with pytest.raises(HTTPException) as exc:
        use_case.execute(dados2)
    assert exc.value.status_code == 422

def test_bicicleta_alugada_retorna_bicicleta_quando_ha_aluguel():
    # Setup: Limpa repositórios e cria ciclista ativo
    fake_aluguel_repository.resetar()
    fake_ciclista_repository.resetar()
    ciclista = _criar_ciclista_ativo("Marcos Bicicleta", "marcos@teste.com", "32132132100")
    
    # Execução: Realiza aluguel para criar contexto
    use_case_aluguel = RealizarAluguel(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_externo_repository,
        fake_equipamento_repository
    )
    dados = NovoAluguel(ciclista=ciclista.id, trancaInicio=101)
    aluguel = use_case_aluguel.execute(dados)
    assert aluguel is not None
    assert aluguel.bicicleta is not None
    
    # Execução: Testa o use case BuscarBicicletaAlugada
    use_case_buscar = BuscarBicicletaAlugada(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_equipamento_repository
    )
    bicicleta = use_case_buscar.execute(ciclista.id)
    
    # Verificação: Confirma que retorna a bicicleta correta
    assert bicicleta is not None
    assert bicicleta.id == aluguel.bicicleta
    assert bicicleta.status == "EM_USO"

def test_bicicleta_alugada_retorna_null_quando_nao_ha_aluguel():
    # Setup: Limpa repositórios e cria ciclista ativo (sem aluguel)
    fake_aluguel_repository.resetar()
    fake_ciclista_repository.resetar()
    ciclista = _criar_ciclista_ativo("Lúcia Livre", "lucia@teste.com", "55555555555")
    
    # Execução: Testa o use case BuscarBicicletaAlugada
    use_case = BuscarBicicletaAlugada(
        fake_aluguel_repository,
        fake_ciclista_repository,
        fake_equipamento_repository
    )
    bicicleta = use_case.execute(ciclista.id)
    
    # Verificação: Confirma que retorna None quando não há aluguel ativo
    assert bicicleta is None

def test_permite_aluguel_retorna_true_quando_nao_tem_aluguel_ativo():
    # Setup: Limpa repositórios e cria ciclista ativo
    fake_aluguel_repository.resetar()
    fake_ciclista_repository.resetar()
    ciclista = _criar_ciclista_ativo("Maria Silva", "maria@teste.com", "12345678901")
    
    # Execução: Verifica permissão de aluguel
    use_case = VerificarPermissaoAluguel(fake_ciclista_repository, fake_aluguel_repository)
    permitido = use_case.execute(ciclista.id)
    assert permitido is True

def test_permite_aluguel_404_para_ciclista_inexistente():
    # Setup: Limpa repositórios
    fake_aluguel_repository.resetar()
    fake_ciclista_repository.resetar()
    
    # Execução: Tenta verificar permissão de ciclista inexistente
    use_case = VerificarPermissaoAluguel(fake_ciclista_repository, fake_aluguel_repository)
    with pytest.raises(HTTPException) as exc:
        use_case.execute(9999)
    assert exc.value.status_code == 404
    assert exc.value.detail["codigo"] == "404"

def test_permite_aluguel_retorna_false_para_ciclista_inativo():
    # Setup: Limpa repositórios e cria ciclista inativo
    fake_aluguel_repository.resetar()
    fake_ciclista_repository.resetar()
    novo_ciclista = NovoCiclista(
        nome="Maria Silva",
        nascimento=date(1995, 1, 1),
        cpf="12345678901",
        nacionalidade="BRASILEIRO",
        email="maria@teste.com",
        senha="senha123",
        urlFotoDocumento="https://site.com/doc.png"
    )
    cartao = CartaoDeCredito(
        id=1,
        nomeTitular="Maria Silva",
        numero="4111111111111111",
        validade=date(2026, 12, 1),
        cvv="123"
    )
    ciclista = Ciclista(
        **novo_ciclista.model_dump(),
        id=0,
        cartaoDeCredito=cartao,
        status=StatusEnum.AGUARDANDO_CONFIRMACAO  # Status inativo
    )
    ciclista = fake_ciclista_repository.salvar(ciclista)
    
    # Execução: Verifica permissão de aluguel para ciclista inativo
    use_case = VerificarPermissaoAluguel(fake_ciclista_repository, fake_aluguel_repository)
    permitido = use_case.execute(ciclista.id)
    assert permitido is False

def test_aluguel_tranca_nao_ocupada():
    # Setup: Limpa repositórios e cria ciclista ativo
    fake_ciclista_repository.resetar()
    fake_aluguel_repository.resetar()
    ciclista = _criar_ciclista_ativo("João Teste", "joao@teste.com", "12345678901")
    
    # Mock: Simula tranca com status LIVRE (não ocupada)
    obter_tranca = fake_equipamento_repository.obter_tranca
    try:
        fake_equipamento_repository.obter_tranca = lambda id_tranca: {
            "id": id_tranca,
            "numero": id_tranca,
            "localizacao": "-22.9068,-43.1729",
            "anoDeFabricacao": "2020",
            "modelo": "MockTranca",
            "status": "LIVRE",  # Status que impede aluguel
            "bicicleta": 5678
        }
        
        # Execução: Tenta alugar em tranca livre
        use_case = RealizarAluguel(
            fake_aluguel_repository,
            fake_ciclista_repository,
            fake_externo_repository,
            fake_equipamento_repository
        )
        dados = NovoAluguel(ciclista=ciclista.id, trancaInicio=103)
        
        with pytest.raises(HTTPException) as exc:
            use_case.execute(dados)
        
        # Verificação: Confirma erro esperado
        assert exc.value.status_code == 422
        assert exc.value.detail == "Tranca não está ocupada"
    finally:
        # Cleanup: Restaura método original
        fake_equipamento_repository.obter_tranca = obter_tranca

def test_aluguel_bicicleta_em_reparo():
    # Setup: Limpa repositórios e cria ciclista ativo
    fake_ciclista_repository.resetar()
    fake_aluguel_repository.resetar()
    ciclista = _criar_ciclista_ativo("Maria Teste", "maria@teste.com", "98765432109")
    
    # Mock: Simula bicicleta com status EM_REPARO
    obter_bicicleta = fake_equipamento_repository.obter_bicicleta
    try:
        fake_equipamento_repository.obter_bicicleta = lambda id_bicicleta: {
            "id": id_bicicleta,
            "marca": "MockMarca",
            "modelo": "MockModelo",
            "ano": "2020",
            "numero": id_bicicleta,
            "status": "EM_REPARO"  # Status que impede aluguel
        }
        
        # Execução: Tenta alugar bicicleta em reparo
        use_case = RealizarAluguel(
            fake_aluguel_repository,
            fake_ciclista_repository,
            fake_externo_repository,
            fake_equipamento_repository
        )
        dados = NovoAluguel(ciclista=ciclista.id, trancaInicio=103)
        
        with pytest.raises(HTTPException) as exc:
            use_case.execute(dados)
        
        # Verificação: Confirma erro esperado
        assert exc.value.status_code == 422
        assert exc.value.detail == "Bicicleta em reparo ou aposentada"
    finally:
        # Cleanup: Restaura método original
        fake_equipamento_repository.obter_bicicleta = obter_bicicleta

def test_aluguel_bicicleta_aposentada():
    # Setup: Limpa repositórios e cria ciclista ativo
    fake_ciclista_repository.resetar()
    fake_aluguel_repository.resetar()
    ciclista = _criar_ciclista_ativo("Pedro Teste", "pedro@teste.com", "11122233344")
    
    # Mock: Simula bicicleta com status APOSENTADA
    obter_bicicleta = fake_equipamento_repository.obter_bicicleta
    try:
        fake_equipamento_repository.obter_bicicleta = lambda id_bicicleta: {
            "id": id_bicicleta,
            "marca": "MockMarca",
            "modelo": "MockModelo",
            "ano": "2020",
            "numero": id_bicicleta,
            "status": "APOSENTADA"  # Status que impede aluguel
        }
        
        # Execução: Tenta alugar bicicleta aposentada
        use_case = RealizarAluguel(
            fake_aluguel_repository,
            fake_ciclista_repository,
            fake_externo_repository,
            fake_equipamento_repository
        )
        dados = NovoAluguel(ciclista=ciclista.id, trancaInicio=103)
        
        with pytest.raises(HTTPException) as exc:
            use_case.execute(dados)
        
        # Verificação: Confirma erro esperado
        assert exc.value.status_code == 422
        assert exc.value.detail == "Bicicleta em reparo ou aposentada"
    finally:
        # Cleanup: Restaura método original
        fake_equipamento_repository.obter_bicicleta = obter_bicicleta

def test_aluguel_cobranca_nao_aprovada():
    # Setup: Limpa repositórios e cria ciclista ativo
    fake_ciclista_repository.resetar()
    fake_aluguel_repository.resetar()
    ciclista = _criar_ciclista_ativo("Ana Teste", "ana@teste.com", "55566677788")
    
    # Mock: Simula cobrança rejeitada e fila de cobranças
    realizar_cobranca = fake_externo_repository.realizar_cobranca
    incluir_cobranca_fila = fake_externo_repository.incluir_cobranca_fila
    cobrancas_fila = []
    try:
        fake_externo_repository.realizar_cobranca = lambda ciclista_id, valor: {
            "id_cobranca": None,
            "status": "REJEITADA",  # Cobrança rejeitada
            "valor": valor,
            "ciclista_id": ciclista_id,
            "data_cobranca": "2024-01-01T10:00:00"
        }
        fake_externo_repository.incluir_cobranca_fila = lambda ciclista_id, valor: cobrancas_fila.append((ciclista_id, valor))
        
        # Execução: Realiza aluguel com cobrança rejeitada
        use_case = RealizarAluguel(
            fake_aluguel_repository,
            fake_ciclista_repository,
            fake_externo_repository,
            fake_equipamento_repository
        )
        dados = NovoAluguel(ciclista=ciclista.id, trancaInicio=103)
        aluguel = use_case.execute(dados)
        
        # Verificação: Confirma que aluguel foi criado e cobrança foi para fila
        assert aluguel is not None
        assert aluguel.ciclista == ciclista.id
        assert aluguel.trancaInicio == 103
        assert aluguel.cobranca is None  # Sem cobrança aprovada
        assert cobrancas_fila == [(ciclista.id, 10.00)]  # Cobrança na fila
    finally:
        # Cleanup: Restaura métodos originais
        fake_externo_repository.realizar_cobranca = realizar_cobranca
        fake_externo_repository.incluir_cobranca_fila = incluir_cobranca_fila

def test_aluguel_tranca_nao_encontrada():
    # Setup: Limpa repositórios e cria ciclista ativo
    fake_ciclista_repository.resetar()
    fake_aluguel_repository.resetar()
    ciclista = _criar_ciclista_ativo("Tranca Falha", "tranca@falha.com", "11111111111")
    
    # Mock: Simula tranca inexistente (retorna None)
    obter_tranca = fake_equipamento_repository.obter_tranca
    try:
        fake_equipamento_repository.obter_tranca = lambda id_tranca: None
        
        # Execução: Tenta alugar em tranca inexistente
        use_case = RealizarAluguel(
            fake_aluguel_repository,
            fake_ciclista_repository,
            fake_externo_repository,
            fake_equipamento_repository
        )
        dados = NovoAluguel(ciclista=ciclista.id, trancaInicio=999)
        
        with pytest.raises(HTTPException) as exc:
            use_case.execute(dados)
        
        # Verificação: Confirma erro esperado
        assert exc.value.status_code == 422
        assert exc.value.detail == "Tranca não encontrada"
    finally:
        # Cleanup: Restaura método original
        fake_equipamento_repository.obter_tranca = obter_tranca

def test_aluguel_bicicleta_nao_encontrada_na_tranca():
    # Setup: Limpa repositórios e cria ciclista ativo
    fake_ciclista_repository.resetar()
    fake_aluguel_repository.resetar()
    ciclista = _criar_ciclista_ativo("Sem Bike", "sembike@falha.com", "22222222222")
    
    # Mock: Simula tranca sem bicicleta
    obter_bicicleta_na_tranca = fake_equipamento_repository.obter_bicicleta_na_tranca
    try:
        fake_equipamento_repository.obter_bicicleta_na_tranca = lambda id_tranca: None
        
        # Execução: Tenta alugar em tranca sem bicicleta
        use_case = RealizarAluguel(
            fake_aluguel_repository,
            fake_ciclista_repository,
            fake_externo_repository,
            fake_equipamento_repository
        )
        dados = NovoAluguel(ciclista=ciclista.id, trancaInicio=101)
        
        with pytest.raises(HTTPException) as exc:
            use_case.execute(dados)
        
        # Verificação: Confirma erro esperado
        assert exc.value.status_code == 422
        assert exc.value.detail == "Nenhuma bicicleta encontrada na tranca"
    finally:
        # Cleanup: Restaura método original
        fake_equipamento_repository.obter_bicicleta_na_tranca = obter_bicicleta_na_tranca