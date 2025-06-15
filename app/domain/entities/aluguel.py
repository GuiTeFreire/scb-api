from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NovoAluguel(BaseModel):
    ciclista: int
    trancaInicio: int

class Aluguel(NovoAluguel):
    id: Optional[int] = None
    bicicleta: Optional[int] = None
    horaInicio: datetime
    trancaFim: Optional[int] = None
    horaFim: Optional[datetime] = None
    cobranca: Optional[int] = None

class AluguelResponse(BaseModel):
    bicicleta: Optional[int] = None
    horaInicio: datetime
    trancaFim: Optional[int] = None
    horaFim: Optional[datetime] = None
    cobranca: Optional[int] = None
    ciclista: int
    trancaInicio: int