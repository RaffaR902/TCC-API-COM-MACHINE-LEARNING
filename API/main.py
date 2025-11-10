# main.py (ATUALIZADO)
import uvicorn
from fastapi import FastAPI, HTTPException, Path
from typing import List

# Importa os esquemas (modelos Pydantic)
import schemas

# Importa os serviços de ML e do "Banco de Dados"
import ml_service
import mock_db

API_VERSION = "1.0.0"

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="API de Precificação de Imóveis (ML)",
    description="API completa com endpoints de previsão, consulta e monitoramento.",
    version=API_VERSION
)

# --- Funções de Tratamento de Erro (Helpers) ---

def _handle_prediction_error(e: Exception):
    """Trata erros que podem ocorrer durante a predição."""
    if isinstance(e, RuntimeError):
        # Erro de modelo não carregado
        raise HTTPException(status_code=503, detail=f"Serviço indisponível: {e}")
    if isinstance(e, ValueError):
        # Erro nos dados de entrada (ex: feature ausente)
        raise HTTPException(status_code=400, detail=f"Erro nos dados de entrada: {e}")
    # Outros erros inesperados
    raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {e}")

# --- 0. Endpoint Raiz ---
@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Bem-vindo à API de Precificação", "docs": "/docs"}

# --- 🔹 Endpoints de Previsão (1, 2, 3) ---

@app.post("/predict/venda", 
          response_model=schemas.PredicaoVendaOutput, 
          tags=["Previsão"])
async def endpoint_prever_venda(imovel: schemas.ImovelFeatures):
    """Retorna o valor previsto de **venda** de um imóvel."""
    try:
        valor = ml_service.prever_venda(imovel)
        return schemas.PredicaoVendaOutput(valor_previsto_venda=round(valor, 2))
    except Exception as e:
        _handle_prediction_error(e)

@app.post("/predict/aluguel", 
          response_model=schemas.PredicaoAluguelOutput, 
          tags=["Previsão"])
async def endpoint_prever_aluguel(imovel: schemas.ImovelFeatures):
    """Retorna o valor previsto de **aluguel** de um imóvel."""
    try:
        valor = ml_service.prever_aluguel(imovel)
        return schemas.PredicaoAluguelOutput(valor_previsto_aluguel=round(valor, 2))
    except Exception as e:
        _handle_prediction_error(e)

@app.post("/predict/imovel", 
          response_model=schemas.PredicaoImovelOutput, 
          tags=["Previsão"])
async def endpoint_prever_imovel(imovel: schemas.ImovelFeatures):
    """Retorna os valores previstos de **venda e aluguel** para o imóvel."""
    try:
        # Executa ambas as predições
        valor_venda = ml_service.prever_venda(imovel)
        valor_aluguel = ml_service.prever_aluguel(imovel)
        
        return schemas.PredicaoImovelOutput(
            valor_previsto_venda=round(valor_venda, 2),
            valor_previsto_aluguel=round(valor_aluguel, 2)
        )
    except Exception as e:
        _handle_prediction_error(e)

# --- 🔹 Endpoints de Consulta de Dados (4, 5, 6, 7) ---

@app.get("/tipos-imoveis", 
         response_model=schemas.TiposImoveisOutput, 
         tags=["Consulta"])
async def endpoint_listar_tipos_imoveis():
    """Lista os tipos de imóveis suportados pelo modelo."""
    return mock_db.get_tipos_imoveis()

@app.get("/estados", 
         response_model=schemas.EstadosOutput, 
         tags=["Consulta"])
async def endpoint_listar_estados():
    """Lista os estados (UFs) que possuem dados."""
    return mock_db.get_estados()

@app.get("/estados/{uf}/cidades", 
         response_model=schemas.CidadesOutput, 
         tags=["Consulta"])
async def endpoint_listar_cidades_por_estado(
    uf: str = Path(..., min_length=2, max_length=2, description="Sigla do estado (ex: SP)")
):
    """Lista as cidades disponíveis para um determinado estado (UF)."""
    # A lógica de erro 404 é tratada pela função do mock_db
    return mock_db.get_cidades_por_estado(uf)

@app.get("/estados/{uf}/cidades/{cidade}/bairros", 
         response_model=schemas.BairrosOutput, 
         tags=["Consulta"])
async def endpoint_listar_bairros_por_cidade(
    uf: str = Path(..., min_length=2, max_length=2, description="Sigla do estado (ex: SP)"),
    cidade: str = Path(..., min_length=2, description="Nome da cidade (ex: São Paulo)")
):
    """Lista os bairros disponíveis para uma determinada cidade."""
    return mock_db.get_bairros_por_cidade(uf, cidade)

# --- 🔹 Endpoints de Monitoramento (8, 10) ---

@app.get("/status", 
         response_model=schemas.StatusOutput, 
         tags=["Monitoramento"])
async def endpoint_status():
    """Verifica o status da API e dos modelos de ML."""
    return schemas.StatusOutput(
        status="ok",
        versao=API_VERSION,
        modelo_atualizado=ml_service.are_models_loaded()
    )

@app.get("/modelo/versao", 
         response_model=schemas.ModeloVersaoOutput, 
         tags=["Monitoramento"])
async def endpoint_obter_versao_modelo():
    """Retorna a versão e data de atualização dos modelos de ML."""
    return ml_service.get_model_version_info()

# --- 🔹 Endpoints Avançados (9) ---

@app.get("/estatisticas/{estado}/{cidade}/{bairro}", 
         response_model=schemas.EstatisticasBairroOutput, 
         tags=["Avançado"])
async def endpoint_estatisticas_bairro(
    estado: str = Path(..., min_length=2, max_length=2, description="Sigla do estado (ex: SP)"),
    cidade: str = Path(..., min_length=2, description="Nome da cidade (ex: São Paulo)"),
    bairro: str = Path(..., min_length=2, description="Nome do bairro (ex: Pinheiros)")
):
    """Retorna estatísticas agregadas (média, mín, máx) para o bairro."""
    return mock_db.get_estatisticas_bairro(estado, cidade, bairro)

# --- Execução ---
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
