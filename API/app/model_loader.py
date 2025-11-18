import pickle
from pathlib import Path

class ModelLoader:
    def __init__(self):
        base_path = Path(__file__).resolve().parent.parent / "models"

        self.modelo_venda = self.load_model(base_path / "modelo_venda.pkl")
        self.modelo_aluguel = self.load_model(base_path / "modelo_aluguel.pkl")

    def load_model(self, path: Path):
        with open(path, "rb") as f:
            return pickle.load(f)

model_loader = ModelLoader()
