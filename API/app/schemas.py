from pydantic import BaseModel

class ImovelEntrada(BaseModel):
    """
    Classe que representa os dados de entrada enviados pelo cliente
    para realizar a previsão de venda ou aluguel.
    Ela deve ter EXATAMENTE as mesmas features usadas no treinamento.
    """

    tipo: str          # Tipo do imóvel (ex: "Apartamento", "Casa")
    bairro: str        # Bairro do imóvel
    cidade: str        # Cidade do imóvel
    
    area_util: float   # Área útil em metros quadrados (float)
    quartos: int       # Número de quartos
    suites: int        # Número de suítes
    vagas: int         # Número de vagas de garagem


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
