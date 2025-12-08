import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.routes import previsoes, metadata, info

app = FastAPI(
    title="API de Previsão de Imóveis",
    description="API para previsão de venda e aluguel utilizando modelos de Machine Learning.",
    version="1.0.0"
)

# Tratamento personalizado de erros de validação
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, exc: RequestValidationError):
    """
    Captura erros de validação (tipo errado, campo faltando, valor negativo)
    e retorna uma mensagem limpa em português.
    """
    erros_detalhados = []
    
    for error in exc.errors():
        campo = error.get("loc")[-1]  # Pega o nome do campo (ex: 'quartos')
        msg = error.get("msg")       # Pega a mensagem técnica
        tipo_erro = error.get("type") # Pega o tipo do erro

        mensagem_erro = f"Erro no campo '{campo}': {msg}"
        
        if tipo_erro == "type_error.integer":
            mensagem_erro = f"O campo '{campo}' deve ser um número inteiro."
        elif tipo_erro == "type_error.float":
            mensagem_erro = f"O campo '{campo}' deve ser um número decimal."
        elif "missing" in tipo_erro:
            mensagem_erro = f"O campo '{campo}' é obrigatório e não foi enviado."
        elif "greater_than" in tipo_erro or "greater_than_equal" in tipo_erro:
            mensagem_erro = f"O campo '{campo}' tem um valor inválido (muito baixo)."

        erros_detalhados.append(mensagem_erro)

    return JSONResponse(
        status_code=422,
        content={
            "status": "erro",
            "mensagem": "Dados de entrada inválidos.",
            "detalhes": erros_detalhados
        },
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],  
    allow_headers=["*"],  
)

# Inclui os roteadores (endpoints organizados por módulo)
app.include_router(previsoes.router)
app.include_router(metadata.router)
app.include_router(info.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
