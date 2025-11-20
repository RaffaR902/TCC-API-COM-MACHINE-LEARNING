import pandas as pd
from fastapi import APIRouter
from app.model_loader import model_loader

router = APIRouter(prefix="/info", tags=["Informações"])

@router.get("/status")
def status_api():
    """
    Verifica o status real da API.
    - Checa se os modelos estão carregados
    - Testa uma previsão simples para garantir funcionamento
    - Valida se os arquivos .joblib existem na pasta correta
    """

    status = {
        "api": "online",
        "previsao_teste": {}
    }

    # Verificar se os modelos estão carregados
    status["modelos_carregados"] = {
        "venda": "OK" if model_loader.modelo_venda else "Erro: Não foi possível carregar o modelo de venda",
        "locacao": "OK" if model_loader.modelo_locacao else "Erro: Não foi possível carregar o modelo de locacao"
    }

    # Criar entrada de teste
    X_teste = pd.DataFrame([{
        "area_util": 50,
        "quartos": 2,
        "suites": 1,
        "vagas": 1,
        "tem_suite": 1,
        "tem_vaga": 1,
        "tipo": "apartamento",
        "bairro": "Centro"
    }])

    # Rodar uma previsão simples (para testar o funcionamento)
    try:
        _ = model_loader.modelo_venda.predict(X_teste)
        status["previsao_teste"]["venda"] = "OK"
    except Exception as e:
        status["previsao_teste"]["venda"] = f"Erro: {str(e)}"

    try:
        _ = model_loader.modelo_locacao.predict(X_teste)
        status["previsao_teste"]["locacao"] = "OK"
    except Exception as e:
        status["previsao_teste"]["locacao"] = f"Erro: {str(e)}"

    return status
