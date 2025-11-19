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
    - Valida se os arquivos .pkl existem na pasta correta
    """

    status = {
        "api": "online",
        "modelos": {},
        "previsao_teste": {}
    }

    # Verificar existência dos arquivos .pkl
    base = Path(__file__).resolve().parent.parent / "models"
    modelos_esperados = {
        "modelo_venda.pkl": base / "modelo_venda.pkl",
        "modelo_aluguel.pkl": base / "modelo_aluguel.pkl"
    }

    for nome, caminho in modelos_esperados.items():
        status["modelos"][nome] = "OK" if caminho.exists() else "Arquivo não encontrado"

    # Verificar se os modelos estão carregados
    status["modelos_carregados"] = {
        "venda": "OK" if model_loader.modelo_venda else "Erro",
        "aluguel": "OK" if model_loader.modelo_aluguel else "Erro"
    }

    # Rodar uma previsão simples (não precisa ser real, só para testar funcionamento)
    try:
        X_teste = [[50, 2, 1, 1, 1, 1, "apartamento", "Centro"]]
        _ = model_loader.modelo_venda.predict(X_teste)
        status["previsao_teste"]["venda"] = "OK"
    except Exception as e:
        status["previsao_teste"]["venda"] = f"Erro: {str(e)}"

    try:
        X_teste = [[50, 2, 1, 1, 1, 1, "apartamento", "Centro"]]
        _ = model_loader.modelo_aluguel.predict(X_teste)
        status["previsao_teste"]["aluguel"] = "OK"
    except Exception as e:
        status["previsao_teste"]["aluguel"] = f"Erro: {str(e)}"

    return status
