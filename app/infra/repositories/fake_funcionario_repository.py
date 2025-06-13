from typing import List
from app.domain.entities.funcionario import Funcionario, NovoFuncionario
from app.domain.repositories.funcionario_repository import FuncionarioRepository

class FakeFuncionarioRepository(FuncionarioRepository):
    def __init__(self):
        self._db: List[Funcionario] = []
        self._contador = 1

    def salvar(self, dados: NovoFuncionario) -> Funcionario:
        funcionario = Funcionario(
            matricula=str(self._contador),
            **dados.model_dump()
        )
        self._db.append(funcionario)
        self._contador += 1
        return funcionario
