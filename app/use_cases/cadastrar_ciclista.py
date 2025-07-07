from fastapi import HTTPException

from app.domain.entities.ciclista import RequisicaoCadastroCiclista, CartaoDeCredito, Ciclista, StatusEnum
from app.domain.repositories.ciclista_repository import CiclistaRepository
from app.domain.repositories.externo_repository import ExternoRepository

class CadastrarCiclista:
    def __init__(self, repository: CiclistaRepository, externo_repo: ExternoRepository):
        self.repository = repository
        self.externo_repo = externo_repo

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

        # Validar cartão de crédito no microsserviço externo
        resultado_validacao = self.externo_repo.validar_cartao_credito(dados.meioDePagamento.model_dump())
        if not resultado_validacao["valido"]:
            raise HTTPException(
                status_code=422,
                detail=f"Cartão de crédito inválido: {resultado_validacao['mensagem']}"
            )

        novo_id = self.repository.proximo_id()
        cartao = CartaoDeCredito(id=novo_id, **dados.meioDePagamento.model_dump())

        ciclista = Ciclista(
            id=novo_id,
            status=StatusEnum.AGUARDANDO_CONFIRMACAO,
            cartaoDeCredito=cartao,
            **cic.model_dump()
        )

        # Sistema envia email (integração com microsserviço externo)
        self.externo_repo.enviar_email(
            email=ciclista.email,
            assunto="Cadstro  realizado com sucesso",
            mensagem="Seu cadastro foi realizado. Clique no link para ativar sua conta."
        )

        return self.repository.salvar(ciclista)

