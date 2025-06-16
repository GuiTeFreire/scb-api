from pydantic import BaseModel
from datetime import datetime

class NovoDevolucao(BaseModel):
    ciclista: int
    trancaFim: int

class Devolucao(NovoDevolucao):
    bicicleta: int
    horaInicio: datetime
    horaFim: datetime
    cobranca: int
