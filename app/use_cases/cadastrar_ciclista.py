from fastapi import HTTPException

from app.domain.entities.ciclista import RequisicaoCadastroCiclista, CartaoDeCredito, Ciclista
from app.domain.repositories.ciclista_repository import CiclistaRepository

class CadastrarCiclista:
    def __init__(self, repository: CiclistaRepository):
        self.repository = repository

    def execute(self, dados: RequisicaoCadastroCiclista) -> Ciclista:
        cic = dados.ciclista

        if (cic.cpf and cic.passaporte) or (not cic.cpf and not cic.passaporte):
            raise HTTPException(
                status_code=422,
                detail="Informe apenas CPF ou Passaporte, e pelo menos um dos dois."
            )

        if self.repository.buscar_por_email(cic.email):
            raise HTTPException(
                status_code=422,
                detail="E-mail já cadastrado"
            )

        novo_id = self.repository.proximo_id()
        cartao = CartaoDeCredito(id=novo_id, **dados.meioDePagamento.model_dump())

        ciclista = Ciclista(
            id=novo_id,
            status="AGUARDANDO_CONFIRMACAO",
            cartaoDeCredito=cartao,
            **cic.model_dump()
        )

        return self.repository.salvar(ciclista)

