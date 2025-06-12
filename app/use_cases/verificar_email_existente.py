from app.domain.repositories.ciclista_repository import CiclistaRepository

class VerificarEmailExistente:
    def __init__(self, repository: CiclistaRepository):
        self.repository = repository

    def execute(self, email: str) -> bool:
        return self.repository.buscar_por_email(email) is not None
