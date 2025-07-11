from fastapi import HTTPException
from app.domain.entities.ciclista import Ciclista
from app.domain.repositories.ciclista_repository import CiclistaRepository
from app.domain.entities.ciclista import EdicaoCiclista
from app.domain.repositories.externo_repository import ExternoRepository

class AtualizarCiclista:
    def __init__(self, repository: CiclistaRepository, externo_repo: ExternoRepository):
        self.repository = repository
        self.externo_repo = externo_repo

    def execute(self, id_ciclista: int, dados: EdicaoCiclista) -> Ciclista:
        if (dados.cpf and dados.passaporte) or (not dados.cpf and not dados.passaporte):
            raise HTTPException(status_code=422)

        ciclista = self.repository.atualizar(id_ciclista, dados.model_dump())
        if not ciclista:
            raise HTTPException(status_code=404, detail="Ciclista não encontrado")

        # Sistema envia email (integração com microsserviço externo)
        self.externo_repo.enviar_email(
            email=ciclista.email,
            assunto="Dados atualizados",
            mensagem="Seus dados pessoais foram atualizados com sucesso."
        )
        return ciclista
