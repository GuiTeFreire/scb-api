from fastapi import HTTPException
from app.domain.entities.ciclista import Ciclista
from app.domain.repositories.ciclista_repository import CiclistaRepository

class CadastrarCiclista:
    def __init__(self, repository: CiclistaRepository):
        self.repository = repository

    def execute(self, ciclista: Ciclista) -> Ciclista:
        if (ciclista.cpf and ciclista.passaporte) or (not ciclista.cpf and not ciclista.passaporte):
            raise HTTPException(
                status_code=422,
                detail="Informe apenas CPF ou Passaporte, e pelo menos um dos dois."
            )

        if self.repository.buscar_por_email(ciclista.email):
            raise HTTPException(
                status_code=422,
                detail="E-mail já cadastrado"
            )

        ciclista.status = "AGUARDANDO_CONFIRMACAO"

        return self.repository.salvar(ciclista)
