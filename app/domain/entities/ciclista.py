from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import date
from enum import Enum

class StatusEnum(str, Enum):
    AGUARDANDO_CONFIRMACAO: str = "AGUARDANDO_CONFIRMACAO"
    ATIVO: str = "ATIVO"
    INATIVO: str = "INATIVO"

class Passaporte(BaseModel):
    numero: str
    validade: date
    pais: str

class NovoCiclista(BaseModel):
    nome: str
    nascimento: date
    cpf: Optional[str] = None
    passaporte: Optional[Passaporte] = None
    nacionalidade: str
    email: EmailStr
    urlFotoDocumento: Optional[str] = None
    senha: str

class NovoCartaoDeCredito(BaseModel):
    nomeTitular: str
    numero: str
    validade: date
    cvv: str

    @field_validator("numero")
    @classmethod
    def validar_numero_cartao(cls, v):
        if not v.isdigit() or not 13 <= len(v) <= 19:
            raise ValueError("Número do cartão deve conter entre 13 e 19 dígitos numéricos.")
        return v

    @field_validator("cvv")
    @classmethod
    def validar_cvv(cls, v):
        if not v.isdigit() or not 3 <= len(v) <= 4:
            raise ValueError("CVV deve conter 3 ou 4 dígitos numéricos.")
        return v
    
class CartaoDeCredito(NovoCartaoDeCredito):
    id: int

class RequisicaoCadastroCiclista(BaseModel):
    ciclista: NovoCiclista
    meioDePagamento: NovoCartaoDeCredito

class Ciclista(NovoCiclista):
    id: int
    status: StatusEnum = Field(default="AGUARDANDO_CONFIRMACAO")
    cartaoDeCredito: CartaoDeCredito

class CiclistaResposta(BaseModel):
    id: int
    status: StatusEnum
    nome: str
    nascimento: date
    cpf: Optional[str] = None
    passaporte: Optional[Passaporte] = None
    nacionalidade: str
    email: EmailStr
    urlFotoDocumento: Optional[str] = None

class EdicaoCiclista(BaseModel):
    nome: str
    nascimento: date
    cpf: Optional[str] = None
    passaporte: Optional[Passaporte] = None
    nacionalidade: str
    email: EmailStr
    urlFotoDocumento: Optional[str] = None
