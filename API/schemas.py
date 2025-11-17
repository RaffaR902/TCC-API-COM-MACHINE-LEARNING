# schemas.py
from pydantic import BaseModel, Field
from typing import List

# --- Esquemas de Previsão (Inputs e Outputs) ---

class ImovelFeatures(BaseModel):
    """Modelo de ENTRADA para predição."""
    tipo_imovel: str = Field(..., description="Tipo do imóvel (ex: apartamento, casa)")
    bairro: str = Field(..., description="Bairro do imóvel")
    cidade: str = Field(..., description="Cidade do imóvel")
    quartos: int = Field(..., ge=1, description="Número de quartos")
    suites: int = Field(..., ge=0, description="Número de suítes")
    vagas: int = Field(..., ge=0, description="Número de vagas de garagem")
    area_util: float = Field(..., gt=0, description="Área útil em m²")

    class Config:
        schema_extra = {
            "example": {
                "tipo_imovel": "apartamento",
                "bairro": "Pinheiros",
                "cidade": "São Paulo",
                "quartos": 2,
                "suites": 1,
                "vagas": 1,
                "area_util": 75.0
            }
        }

class PredicaoVendaOutput(BaseModel):
    valor_previsto_venda: float

class PredicaoAluguelOutput(BaseModel):
    valor_previsto_aluguel: float

class PredicaoImovelOutput(BaseModel):
    valor_previsto_venda: float
    valor_previsto_aluguel: float

# --- Esquemas de Consulta de Dados ---

class TiposImoveisOutput(BaseModel):
    tipos_disponiveis: List[str]

class EstadosOutput(BaseModel):
    estados: List[str]

class CidadesOutput(BaseModel):
    estado: str
    cidades: List[str]

class BairrosOutput(BaseModel):
    estado: str
    cidade: str
    bairros: List[str]

# --- Esquemas de Monitoramento ---

class StatusOutput(BaseModel):
    status: str
    versao: str
    modelo_atualizado: bool

class ModeloVersaoOutput(BaseModel):
    versao_modelo: str
    ultima_atualizacao: str

# --- Esquemas Avançados ---

class EstatisticasBairroOutput(BaseModel):
    estado: str
    cidade: str
    bairro: str
    media_venda: float
    valor_minimo_venda: float
    valor_maximo_venda: float
    media_aluguel: float
    valor_minimo_aluguel: float
    valor_maximo_aluguel: float

