from fastapi import HTTPException
from app.models.ciclista import RequisicaoCadastroCiclista, Ciclista

fake_db = {"ciclistas": []}
current_id = 1

def cadastrar_ciclista(payload: RequisicaoCadastroCiclista) -> Ciclista:
    global current_id

    cic = payload.ciclista

    if (cic.cpf and cic.passaporte) or (not cic.cpf and not cic.passaporte):
        raise HTTPException(
            status_code=422,
            detail="Informe apenas CPF ou Passaporte, e apenas um dos dois."
        )

    for c in fake_db["ciclistas"]:
        if c["email"] == cic.email:
            raise HTTPException(
                status_code=422,
                detail="E-mail já cadastrado"
            )

    novo = cic.model_dump()
    novo.update({"id": current_id, "status": "AGUARDANDO_CONFIRMACAO"})
    fake_db["ciclistas"].append(novo)
    current_id += 1
    return Ciclista(**novo)
