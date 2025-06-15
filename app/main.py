from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.api import ciclista, funcionario, restaurar

app = FastAPI(
    title="SCB - Sistema de Controle de Bicicletário",
    description="API do sistema SCB para gerenciamento de bicicletas compartilhadas.",
    version="1.0.0"
)

app.include_router(ciclista.router)
app.include_router(funcionario.router)
app.include_router(restaurar.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=[
            {"codigo": "422", "mensagem": "Dados Inválidos"}
        ]
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Se o detail já é uma lista, não modificar
    if isinstance(exc.detail, list):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "codigo": str(exc.status_code),
                "mensagem": exc.detail
            }
        )
    
    # Se o detail é um dicionário, não modificar
    if isinstance(exc.detail, dict):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )
    
    # Para outros casos, usar o formato padrão
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "codigo": str(exc.status_code),
            "mensagem": exc.detail or "Erro inesperado"
        }
    )