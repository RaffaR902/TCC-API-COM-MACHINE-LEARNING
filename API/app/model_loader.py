from pathlib import Path
import joblib

class ModelLoader:
    """
    Classe responsável por carregar os modelos de previsão usados pela API.
    Ela centraliza o carregamento para evitar recarregar arquivos .joblib
    a cada requisição, melhorando a performance.
    """

    def __init__(self):
        # Caminho base onde os modelos .joblib estão armazenados
        base_path = Path(__file__).resolve().parent.parent / "models"

        # Carrega o modelo de previsão de venda
        self.modelo_venda = self.load_model(base_path / "modelo_venda.joblib")

        # Carrega o modelo de previsão de locacao
        self.modelo_locacao = self.load_model(base_path / "modelo_locacao.joblib")

    def load_model(self, path: Path):
        """
        Carrega um arquivo .joblib do caminho informado e retorna o modelo.
        """
        with open(path, "rb") as f:
            return joblib.load(f)

# Instância única da classe, utilizada pelos endpoints
model_loader = ModelLoader()
