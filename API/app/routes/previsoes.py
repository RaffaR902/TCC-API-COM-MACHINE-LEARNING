from fastapi import APIRouter, HTTPException
import pandas as pd

from app.model_loader import model_loader 
from app.feature_engineering import preprocessar
from app.schemas import ImovelEntrada, VendaResposta, LocacaoResposta, CompletoResposta

router = APIRouter()


# ENDPOINT: VENDA
@router.post("/venda", response_model=VendaResposta)
def prever_venda(imovel: ImovelEntrada):
    """
    Retorna apenas o valor previsto de venda.
    """
    # 1. Converter Pydantic -> DataFrame
    df = pd.DataFrame([imovel.dict()])

    # 2. Preprocessar usando artefatos de VENDA
    try:
        X = preprocessar(df, tipo="venda")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento (venda): {str(e)}")

    # 3. Previsão
    if not model_loader.modelo_venda:
        raise HTTPException(status_code=503, detail="Modelo de venda não carregado.")
    
    pred = model_loader.modelo_venda.predict(X)[0]

    return {"valor_previsto_venda": float(pred)}


# ENDPOINT: LOCAÇÃO
@router.post("/locacao", response_model=LocacaoResposta)
def prever_locacao(imovel: ImovelEntrada):
    """
    Retorna apenas o valor previsto de locação.
    """
    # 1. Converter Pydantic -> DataFrame
    df = pd.DataFrame([imovel.dict()])

    # 2. Preprocessar usando artefatos de locação
    try:
        X = preprocessar(df, tipo="locacao")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento (locacao): {str(e)}")

    # 3. Previsão
    if not model_loader.modelo_locacao:
        raise HTTPException(status_code=503, detail="Modelo de locação não carregado.")

    pred = model_loader.modelo_locacao.predict(X)[0]

    return {"valor_previsto_locacao": float(pred)}


# ENDPOINT: COMPLETO (Venda + Locação)
@router.post("/completo", response_model=CompletoResposta)
def prever_completo(imovel: ImovelEntrada):
    """
    Retorna previsão conjunta de valor de venda e locação.
    Processa os dados duas vezes, pois cada modelo exige transformações específicas.
    """
    df_base = pd.DataFrame([imovel.dict()])

    # Previsão Venda 
    if not model_loader.modelo_venda:
        raise HTTPException(status_code=503, detail="Modelo de venda não carregado.")
    
    # Usar .copy() para não alterar o dataframe original e afetar a próxima etapa
    X_venda = preprocessar(df_base.copy(), tipo="venda")
    pred_venda = model_loader.modelo_venda.predict(X_venda)[0]

    # Previsão Locação
    if not model_loader.modelo_locacao:
        raise HTTPException(status_code=503, detail="Modelo de locação não carregado.")
        
    X_locacao = preprocessar(df_base.copy(), tipo="locacao")
    pred_locacao = model_loader.modelo_locacao.predict(X_locacao)[0]

    return {
        "valor_previsto_venda": float(pred_venda),
        "valor_previsto_locacao": float(pred_locacao),
    }