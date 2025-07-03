from fastapi import HTTPException
from app.domain.entities.ciclista import NovoCartaoDeCredito
from app.domain.repositories.ciclista_repository import CiclistaRepository
from app.domain.repositories.externo_repository import ExternoRepository

class AtualizarCartaoDeCredito:
    def __init__(self, repository: CiclistaRepository, externo_repo: ExternoRepository):
        self.repository = repository
        self.externo_repo = externo_repo

    def execute(self, id_ciclista: int, novo_cartao: NovoCartaoDeCredito):
        ciclista = self.repository.buscar_por_id(id_ciclista)
        if not ciclista:
            raise HTTPException(
                status_code=404,
                detail={"codigo": "404", "mensagem": "Ciclista não encontrado"}
            )
        
        # Sistema envia email (integração com microsserviço externo)
        self.externo_repo.enviar_email(
            email=ciclista.email,
            assunto="Cadstro  realizado com sucesso",
            mensagem=f"Seu cadastro foi realizado. Clique no link para ativar sua conta."
        )

        ciclista.cartaoDeCredito = novo_cartao.model_copy(update={"id": id_ciclista})
        self.repository.atualizar(id_ciclista, {"cartaoDeCredito": ciclista.cartaoDeCredito})
        return ciclista.cartaoDeCredito
