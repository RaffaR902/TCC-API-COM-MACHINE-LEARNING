from pathlib import Path
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
        "modelos": {},
        "previsao_teste": {}
    }

    # Verificar existência dos arquivos .joblib
    base = Path(__file__).resolve().parent.parent / "models"
    modelos_esperados = {
        "modelo_venda.joblib": base / "modelo_venda.joblib",
        "modelo_locacao.joblib": base / "modelo_locacao.joblib"
    }

    for nome, caminho in modelos_esperados.items():
        status["modelos"][nome] = "OK" if caminho.exists() else "Arquivo do modelo não encontrado"

    # Verificar se os modelos estão carregados
    status["modelos_carregados"] = {
        "venda": "OK" if model_loader.modelo_venda else "Erro: Não foi possível carregar o modelo de venda",
        "locacao": "OK" if model_loader.modelo_locacao else "Erro: Não foi possível carregar o modelo de locacao"
    }

    # Rodar uma previsão simples (para testar o funcionamento)
    try:
        X_teste = [[50, 2, 1, 1, 1, 1, "apartamento", "Centro"]]
        _ = model_loader.modelo_venda.predict(X_teste)
        status["previsao_teste"]["venda"] = "OK"
    except Exception as e:
        status["previsao_teste"]["venda"] = f"Erro: {str(e)}"

    try:
        X_teste = [[50, 2, 1, 1, 1, 1, "apartamento", "Centro"]]
        _ = model_loader.modelo_locacao.predict(X_teste)
        status["previsao_teste"]["locacao"] = "OK"
    except Exception as e:
        status["previsao_teste"]["locacao"] = f"Erro: {str(e)}"

    return status
