import pandas as pd
from fastapi import APIRouter
from app.model_loader import model_loader
from app.feature_engineering import preprocessar

router = APIRouter(prefix="/info", tags=["Informações"])

@router.get("/status")
def status_api():
    status = {
        "api": "online",
        "previsao_teste": {}
    }

    # 1. Checar carregamento dos modelos
    status["modelos_carregados"] = {
        "venda": "OK" if model_loader.modelo_venda else "Erro: Modelo venda OFF",
        "locacao": "OK" if model_loader.modelo_locacao else "Erro: Modelo locacao OFF"
    }

    # 2. Criar dados brutos de teste
    # Incluímos 'cidade' pois é obrigatório
    X_teste_raw = pd.DataFrame([{
        "area_util": 65,
        "quartos": 2,
        "suites": 1,
        "vagas": 1,
        "tipo": "apartamento",
        "bairro": "Centro",
        "cidade": "São Paulo"
    }])

    # 3. Testar Venda
    try:
        # preprocessar agora insere automaticamente 'objetivo', 'preco_medio_bairro', etc.
        X_venda = preprocessar(X_teste_raw.copy(), tipo='venda')
        
        if model_loader.modelo_venda:
            _ = model_loader.modelo_venda.predict(X_venda)
            status["previsao_teste"]["venda"] = "OK"
        else:
            status["previsao_teste"]["venda"] = "Modelo OFF"
    except Exception as e:
        status["previsao_teste"]["venda"] = f"Erro: {str(e)}"

    # 4. Testar Locação
    try:
        X_locacao = preprocessar(X_teste_raw.copy(), tipo='locacao')
        
        if model_loader.modelo_locacao:
            _ = model_loader.modelo_locacao.predict(X_locacao)
            status["previsao_teste"]["locacao"] = "OK"
        else:
            status["previsao_teste"]["locacao"] = "Modelo OFF"
    except Exception as e:
        status["previsao_teste"]["locacao"] = f"Erro: {str(e)}"

    return status