from pydantic import BaseModel

class ImovelEntrada(BaseModel):
    """
    Classe que representa os dados de entrada enviados pelo cliente
    para realizar a previsão de venda ou aluguel.
    Ela deve ter EXATAMENTE as mesmas features usadas no treinamento.
    """

    tipo: str          # Tipo do imóvel (ex: "Apartamento", "Casa")
    bairro: str        # Bairro do imóvel — importante para o OneHotEncoder
    area_util: float   # Área útil em metros quadrados (float)

    quartos: int       # Número de quartos
    suites: int        # Número de suítes
    vagas: int         # Número de vagas de garagem

    # Features derivadas usadas no treino:
    tem_suite: int     # 1 se tem suíte, 0 se não tem
    tem_vaga: int      # 1 se tem vaga, 0 se não tem


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
