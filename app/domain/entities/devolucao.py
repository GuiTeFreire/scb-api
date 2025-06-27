from pydantic import BaseModel
from datetime import datetime

class NovoDevolucao(BaseModel):
    idTranca: int
    idBicicleta: int

class Devolucao(BaseModel):
    bicicleta: int
    horaInicio: datetime
    trancaFim: int
    horaFim: datetime
    cobranca: int
    ciclista: int
