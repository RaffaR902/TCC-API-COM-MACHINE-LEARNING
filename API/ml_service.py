# ml_service.py (ATUALIZADO)
import joblib
import pandas as pd
from schemas import ImovelFeatures
from datetime import date

# --- Constantes do Modelo ---
MODELO_VERSAO = "1.0.3"
MODELO_ATUALIZACAO = "2025-08-15" # Simula data da última atualização

# Lista de colunas na ordem EXATA que o modelo foi treinado
# (Deve bater com 'ALL_FEATURES' do script mock_model_generator.py)
FEATURE_COLUMNS = [
    'area_util', 'quartos', 'suites', 'vagas',
    'tipo_imovel', 'bairro', 'cidade'
]

# --- Carregamento dos Modelos ---
try:
    MODELO_VENDA = joblib.load("models/venda_pipeline.joblib")
    MODELO_ALUGUEL = joblib.load("models/aluguel_pipeline.joblib")
    _MODELOS_CARREGADOS = True
    print(f"LOG: Modelos (v{MODELO_VERSAO}) carregados com sucesso.")
except FileNotFoundError:
    MODELO_VENDA = None
    MODELO_ALUGUEL = None
    _MODELOS_CARREGADOS = False
    print("ERRO: Arquivos de modelo não encontrados! Endpoints de predição ficarão inativos.")

def are_models_loaded() -> bool:
    """Verifica se os modelos foram carregados com sucesso."""
    return _MODELOS_CARREGADOS

def get_model_version_info():
    """Retorna as informações de versão do modelo."""
    return {
        "versao_modelo": MODELO_VERSAO,
        "ultima_atualizacao": MODELO_ATUALIZACAO
    }

def _preparar_dataframe(imovel: ImovelFeatures) -> pd.DataFrame:
    """Converte o objeto Pydantic em um DataFrame do Pandas."""
    dados_dict = imovel.dict()
    df = pd.DataFrame([dados_dict])
    
    # Garante a ordem correta das colunas
    try:
        return df[FEATURE_COLUMNS]
    except KeyError as e:
        raise ValueError(f"Feature de entrada ausente ou inesperada: {e}")

# --- Funções de Predição ---

def prever_venda(imovel: ImovelFeatures) -> float:
    """Executa a predição de valor de VENDA."""
    if not are_models_loaded():
        raise RuntimeError("Modelo de Venda não está carregado.")
        
    df_predicao = _preparar_dataframe(imovel)
    valor_predito = MODELO_VENDA.predict(df_predicao)
    return float(valor_predito[0])

def prever_aluguel(imovel: ImovelFeatures) -> float:
    """Executa a predição de valor de ALUGUEL."""
    if not are_models_loaded():
        raise RuntimeError("Modelo de Aluguel não está carregado.")
        
    df_predicao = _preparar_dataframe(imovel)
    valor_predito = MODELO_ALUGUEL.predict(df_predicao)
    return float(valor_predito[0])

