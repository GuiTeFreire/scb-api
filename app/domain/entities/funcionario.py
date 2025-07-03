from pydantic import BaseModel, EmailStr
from typing import Optional

class NovoFuncionario(BaseModel):
    senha: str
    confirmacaoSenha: Optional[str] = None
    email: EmailStr
    nome: str
    idade: int
    funcao: str
    cpf: str

class Funcionario(NovoFuncionario):
    matricula: str
