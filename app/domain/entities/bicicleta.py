from pydantic import BaseModel
from enum import Enum

class StatusBicicletaEnum(str, Enum):
    DISPONIVEL = 'DISPONÍVEL'
    EM_USO = 'EM_USO'
    NOVA = 'NOVA'
    APOSENTADA = 'APOSENTADA'
    REPARO_SOLICITADO = 'REPARO_SOLICITADO'
    EM_REPARO = 'EM_REPARO'

class Bicicleta(BaseModel):
    id: int
    marca: str
    modelo: str
    ano: str
    numero: int
    status: StatusBicicletaEnum