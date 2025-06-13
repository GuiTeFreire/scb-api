from typing import List, Optional
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
    
    def listar_todos(self) -> List[Funcionario]:
        return self._db
    
    def buscar_por_id(self, id: int) -> Optional[Funcionario]:
        for f in self._db:
            if f.matricula == str(id):
                return f
        return None

    def resetar(self) -> None:
        self._db.clear()
        self._contador = 1

fake_funcionario_repository = FakeFuncionarioRepository()