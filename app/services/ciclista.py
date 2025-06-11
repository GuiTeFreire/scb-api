from fastapi import HTTPException
from app.models.ciclista import RequisicaoCadastroCiclista, Ciclista, EdicaoCiclista

fake_db = {"ciclistas": []}
current_id = 1

def email_existe(email: str) -> bool:
    return any(c["email"] == email for c in fake_db["ciclistas"])

def cadastrar_ciclista(payload: RequisicaoCadastroCiclista) -> Ciclista:
    global current_id

    cic = payload.ciclista

    if email_existe(cic.email):
        raise HTTPException(status_code=422, detail="E-mail já cadastrado")

    if (cic.cpf and cic.passaporte) or (not cic.cpf and not cic.passaporte):
        raise HTTPException(
            status_code=422,
            detail="Informe apenas CPF ou Passaporte, e apenas um dos dois."
        )

    novo = cic.model_dump()
    novo.update({"id": current_id, "status": "AGUARDANDO_CONFIRMACAO"})
    fake_db["ciclistas"].append(novo)
    current_id += 1
    return Ciclista(**novo)

def buscar_ciclista_por_id(idCiclista: int) -> Ciclista:
    for c in fake_db["ciclistas"]:
        if c["id"] == idCiclista:
            return Ciclista(**c)

    raise HTTPException(
        status_code=404,
        detail="Ciclista não encontrado"
    )

def atualizar_ciclista(idCiclista: int, dados: EdicaoCiclista) -> Ciclista:
    for cic in fake_db["ciclistas"]:
        if cic["id"] == idCiclista:
            if (dados.cpf and dados.passaporte) or (not dados.cpf and not dados.passaporte):
                raise HTTPException(status_code=422)

            cic.update(dados.model_dump())
            return Ciclista(**cic)

    raise HTTPException(status_code=404)

