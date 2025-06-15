from pydantic import BaseModel

class Bicicleta(BaseModel):
    id: int
    marca: str
    modelo: str
    ano: int
    numero: int
    status: str