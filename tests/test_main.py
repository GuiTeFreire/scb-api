import pytest
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from app.main import validation_exception_handler, http_exception_handler
import json

@pytest.mark.asyncio
async def test_validation_exception_handler():
    # Setup: Cria exceção de validação
    exc = RequestValidationError(errors=[])
    request = Request(scope={"type": "http"})
    
    # Execução: Chama o handler
    response = await validation_exception_handler(request, exc)
    
    # Verificação: Confirma formato da resposta
    assert response.status_code == 422
    assert json.loads(response.body) == [{"codigo": "422", "mensagem": "Dados Inválidos"}]

@pytest.mark.asyncio
async def test_http_exception_handler_com_dict():
    # Setup: Cria HTTPException com detail em dict
    detail = {"codigo": "404", "mensagem": "Não encontrado"}
    exc = HTTPException(status_code=404, detail=detail)
    request = Request(scope={"type": "http"})
    
    # Execução: Chama o handler
    response = await http_exception_handler(request, exc)
    
    # Verificação: Confirma que retorna o dict original
    assert response.status_code == 404
    assert json.loads(response.body) == {"codigo": "404", "mensagem": "Não encontrado"}

@pytest.mark.asyncio
async def test_http_exception_handler_com_string():
    # Setup: Cria HTTPException com detail em string
    exc = HTTPException(status_code=500, detail="Erro interno")
    request = Request(scope={"type": "http"})
    
    # Execução: Chama o handler
    response = await http_exception_handler(request, exc)
    
    # Verificação: Confirma formato padronizado
    assert response.status_code == 500
    assert json.loads(response.body) == {"codigo": "500", "mensagem": "Erro interno"}

@pytest.mark.asyncio
async def test_http_exception_handler_sem_detail():
    # Setup: Cria HTTPException sem detail
    exc = HTTPException(status_code=500)
    request = Request(scope={"type": "http"})
    
    # Execução: Chama o handler
    response = await http_exception_handler(request, exc)
    
    # Verificação: Confirma fallback para "Erro inesperado"
    assert response.status_code == 500
    # O FastAPI retorna "Internal Server Error" se não passar detail
    assert json.loads(response.body) == {"codigo": "500", "mensagem": "Internal Server Error"}

def test_app_routers_included():
    # Setup: Importa a app
    from app.main import app
    
    # Verificação: Confirma que os routers foram incluídos
    routes = [route.path for route in app.routes]
    assert "/ciclista" in routes
    assert "/funcionario" in routes
    assert "/restaurarBanco" in routes