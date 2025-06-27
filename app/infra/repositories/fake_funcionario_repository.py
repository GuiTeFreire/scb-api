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

    def buscar_por_email(self, email: str) -> Optional[Funcionario]:
        for f in self._db:
            if f.email == email:
                return f
        return None

    def resetar(self) -> None:
        self._db.clear()
        self._contador = 1

    def atualizar(self, id: int, dados: NovoFuncionario) -> Optional[Funcionario]:
        for f in self._db:
            if f.matricula == str(id):
                f.nome = dados.nome
                f.idade = dados.idade
                f.funcao = dados.funcao
                f.cpf = dados.cpf
                f.email = dados.email
                f.senha = dados.senha
                return f
        return None

    def remover(self, id: int) -> bool:
        for i, f in enumerate(self._db):
            if f.matricula == str(id):
                del self._db[i]
                return True
        return False

fake_funcionario_repository = FakeFuncionarioRepository()