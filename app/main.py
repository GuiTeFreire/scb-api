from fastapi import FastAPI

app = FastAPI(
    title="SCB - Sistema de Controle de Bicicletário",
    description="API do sistema SCB para gerenciamento de bicicletas compartilhadas.",
    version="1.0.0"
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Alô mundo do SCB!"}
