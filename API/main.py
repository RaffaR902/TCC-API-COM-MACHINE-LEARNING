from fastapi import FastAPI
from app.routes import previsoes, metadata, info
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="API de Previsão de Imóveis",
    description="API para previsão de venda e aluguel utilizando modelos de Machine Learning.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
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
