from pydantic import BaseModel

class Erro(BaseModel):
    codigo: str
    mensagem: str
