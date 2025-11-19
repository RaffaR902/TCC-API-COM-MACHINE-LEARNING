from fastapi import FastAPI
from app.routes import previsoes, metadata, info

app = FastAPI(
    title="API de Previsão Imobiliária",
    version="1.0.0"
)

# Rotas
app.include_router(previsoes.router)
app.include_router(metadata.router)
app.include_router(info.router)

@app.get("/")
def root():
    return {"mensagem": "API de Previsão Imobiliária funcionando"}
