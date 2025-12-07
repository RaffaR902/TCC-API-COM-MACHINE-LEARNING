import os
import joblib
import numpy as np
import pandas as pd

# Caminho da pasta artifacts
ARTIFACTS_PATH = os.path.join(os.path.dirname(__file__), "..", "artifacts")

class ArtifactLoader:
    """
    Classe responsável por carregar e manter em memória os artefatos de Feature Engineering (médias, clusters, kmeans) para Venda e Locação.
    Evita leitura de disco a cada requisição.
    """
    def __init__(self):
        # Carrega tudo na inicialização
        self.artifacts = {
            "venda": self._load_set("venda"),
            "locacao": self._load_set("locacao")
        }

    def _load_set(self, tipo: str):
        """Carrega o kit de arquivos para um tipo específico (venda/locacao)"""
        try:
            media = joblib.load(os.path.join(ARTIFACTS_PATH, f"media_bairro_{tipo}.joblib"))
            map_clusters = joblib.load(os.path.join(ARTIFACTS_PATH, f"map_clusters_{tipo}.joblib"))
            kmeans = joblib.load(os.path.join(ARTIFACTS_PATH, f"kmeans_bairros_{tipo}.joblib"))
            
            # Pré-calcula a média geral para usar no dif_media_bairro (evita recalcular a cada request)
            media_geral = media.mean()
            
            return {
                "media_bairro": media,
                "map_clusters": map_clusters,
                "kmeans": kmeans,
                "media_geral": media_geral
            }
        except FileNotFoundError as e:
            print(f"ALERTA: Artefatos de {tipo} não encontrados: {e}")
            return None

# Instância global carregada ao iniciar a API
artifact_loader = ArtifactLoader()


# Função de preprocessamento
def preprocessar(df: pd.DataFrame, tipo: str):
    """
    Aplica as transformações no DataFrame usando os artefatos corretos
    baseado no 'tipo' (objetivo) passado pelo endpoint.
    """
    
    # Recupera o kit de artefatos da memória
    kit = artifact_loader.artifacts.get(tipo)
    
    if kit is None:
        raise ValueError(f"Artefatos para '{tipo}' não foram carregados ou não existem.")

    media_bairro = kit["media_bairro"]
    map_clusters = kit["map_clusters"]
    kmeans = kit["kmeans"]
    media_geral = kit["media_geral"]


    # Feature Engineering 

    # Razões Matemáticas
    df["quartos_area"] = df["quartos"] / df["area_util"]
    df["vagas_area"] = df["vagas"] / df["area_util"]
    df["densidade_quartos"] = df["quartos"] / (df["suites"] + 1)
    df["suites_ratio"] = df["suites"] / (df["quartos"] + 1)

    # Binárias
    df["tem_suite"] = (df["suites"] > 0).astype(int)
    df["tem_vaga"] = (df["vagas"] > 0).astype(int)

    # Média de Preço (media_preco)
    df["media_preco"] = df["bairro"].map(media_bairro)
    # Se bairro desconhecido, usa a média geral salva
    df["media_preco"] = df["media_preco"].fillna(media_geral)

    # Dif Média Bairro
    # Compara a média do bairro deste imóvel com a média geral da cidade
    df["dif_media_bairro"] = df["media_preco"] - media_geral

    # Cluster do Bairro
    df["cluster_bairro"] = df["bairro"].map(map_clusters)

    mask = df["cluster_bairro"].isna()
    if mask.any():
        # Previsão do cluster para bairros novos usando a média de preço
        df.loc[mask, "cluster_bairro"] = kmeans.predict(
            df.loc[mask, ["media_preco"]]
        )

    # Features de apoio
    df["area_por_quarto"] = df["area_util"] / df["quartos"].replace(0, np.nan)
    df["area_por_quarto"] = df["area_por_quarto"].fillna(df["area_util"])
    df["proporcao_suites"] = df["suites"] / df["quartos"].replace(0, np.nan)
    df["proporcao_suites"] = df["proporcao_suites"].fillna(0)
    
    # Seleção final de colunas

    # Garante a ordem e existência exata das colunas que o modelo espera
    cols_finais = [
        'area_util', 'quartos', 'suites', 'vagas', 'bairro', 'tipo', 'cidade',
        'media_preco', 'dif_media_bairro', 'cluster_bairro', 
        'quartos_area', 'vagas_area', 'densidade_quartos', 'suites_ratio',
        'tem_suite', 'tem_vaga', 'area_por_quarto', 'proporcao_suites'
    ]
    
    # Filtra apenas o que existe no DataFrame
    cols_existentes = [c for c in cols_finais if c in df.columns]
    
    return df[cols_existentes]
