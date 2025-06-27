from app.infra.repositories.fake_funcionario_repository import fake_funcionario_repository
from app.domain.entities.funcionario import NovoFuncionario

def test_buscar_por_email_retorna_funcionario_quando_existe():
    fake_funcionario_repository.resetar()
    
    # Criar funcionário
    dados = NovoFuncionario(
        nome="Maria Teste",
        idade=25,
        funcao="Atendente",
        cpf="12345678900",
        email="maria@teste.com",
        senha="senha123"
    )
    
    funcionario = fake_funcionario_repository.salvar(dados)
    
    # Buscar por email
    resultado = fake_funcionario_repository.buscar_por_email("maria@teste.com")
    
    assert resultado is not None
    assert resultado.email == "maria@teste.com"
    assert resultado.nome == "Maria Teste"

def test_buscar_por_email_retorna_none_quando_nao_existe():
    fake_funcionario_repository.resetar()
    
    resultado = fake_funcionario_repository.buscar_por_email("email_inexistente@teste.com")
    
    assert resultado is None 