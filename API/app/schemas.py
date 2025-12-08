from pydantic import BaseModel, Field

class ImovelEntrada(BaseModel):
    """
    Classe que representa os dados de entrada enviados pelo cliente
    para realizar a previsão de venda ou aluguel.
    Ela deve ter EXATAMENTE as mesmas features usadas no treinamento.
    """

    tipo: str = Field(..., min_length=2, description="Tipo do imóvel (ex: casa, apartamento)")
    bairro: str = Field(..., min_length=2)
    cidade: str = Field(..., min_length=2)
    
    # Validação Numérica
    # gt=0 -> Greater Than 0
    area_util: float = Field(..., gt=0, description="Área deve ser maior que 0")
    
    # ge=0 -> Greater or Equal to 0
    quartos: int = Field(..., ge=0, description="Não pode ser negativo")
    suites: int = Field(..., ge=0, description="Não pode ser negativo")
    vagas: int = Field(..., ge=0, description="Não pode ser negativo")


class VendaResposta(BaseModel):
    """
    Estrutura de resposta para previsão de valor de venda.
    """
    valor_previsto_venda: float


class LocacaoResposta(BaseModel):
    """
    Estrutura de resposta para previsão de valor de locacao.
    """
    valor_previsto_locacao: float


class CompletoResposta(BaseModel):
    """
    Estrutura de resposta contendo previsão de venda e locacao juntas.
    """
    valor_previsto_venda: float
    valor_previsto_locacao: float
