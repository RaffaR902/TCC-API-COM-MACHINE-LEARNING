from pydantic import BaseModel

class ImovelEntrada(BaseModel):
    tipo: str
    estado: str
    cidade: str
    area_m2: float
    quartos: int | None = None
    banheiros: int | None = None


class VendaResposta(BaseModel):
    valor_previsto_venda: float


class AluguelResposta(BaseModel):
    valor_previsto_aluguel: float


class CompletoResposta(BaseModel):
    valor_previsto_venda: float
    valor_previsto_aluguel: float
