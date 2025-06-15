from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Resetar banco
client.get("/restaurarBanco")

# Criar e ativar ciclista
payload_ciclista = {
    "ciclista": {
        "nome": "Marcos Bicicleta",
        "nascimento": "1993-01-01",
        "cpf": "32132132100",
        "nacionalidade": "BRASILEIRO",
        "email": "marcos@teste.com",
        "senha": "senha123",
        "urlFotoDocumento": "https://site.com/doc.png"
    },
    "meioDePagamento": {
        "nomeTitular": "Marcos Bicicleta",
        "numero": "4111111111111111",
        "validade": "2026-12-01",
        "cvv": "123"
    }
}

res_post = client.post("/ciclista", json=payload_ciclista)
print("Status criação ciclista:", res_post.status_code)
ciclista_id = res_post.json()["id"]
print("ID do ciclista:", ciclista_id)

res_ativar = client.post(f"/ciclista/{ciclista_id}/ativar")
print("Status ativação:", res_ativar.status_code)

# Criar aluguel
payload_aluguel = {
    "ciclista": ciclista_id,
    "trancaInicio": 101
}

res_aluguel = client.post("/aluguel", json=payload_aluguel)
print("Status aluguel:", res_aluguel.status_code)
print("Aluguel criado:", res_aluguel.json())

# Testar endpoint bicicletaAlugada
res = client.get(f"/ciclista/{ciclista_id}/bicicletaAlugada")
print("Status bicicleta alugada:", res.status_code)
print("Response bicicleta:", res.json())
print("Response headers:", res.headers) 