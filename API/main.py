from fastapi import FastAPI
from app.routes import previsoes, metadata, info

# Cria a aplicação FastAPI
app = FastAPI(
    title="API de Previsão de Imóveis",
    description="API para previsão de venda e aluguel utilizando modelos de Machine Learning.",
    version="1.0.0"
)

# Inclui os roteadores (endpoints organizados por módulo)
app.include_router(previsoes.router)
app.include_router(metadata.router)
app.include_router(info.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
