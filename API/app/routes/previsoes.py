from fastapi import APIRouter
from app.schemas import ImovelEntrada, VendaResposta, LocacaoResposta, CompletoResposta
from app.model_loader import model_loader

router = APIRouter(prefix="/prever", tags=["Previsões"])


def montar_features(imovel: ImovelEntrada):
    """
    Constroi o vetor de entrada no exato formato e ordem usados durante o treinamento do modelo.
    Essa função evita duplicação de código nos endpoints.
    """

    # Features derivadas usadas no treino
    tem_suite = 1 if imovel.suites > 0 else 0
    tem_vaga = 1 if imovel.vagas > 0 else 0

    # Ordem das features deve ser exatamente igual à usada no treinamento:
    # ['area_util', 'quartos', 'suites', 'vagas', 'tem_suite', 'tem_vaga', 'tipo', 'bairro']
    return [[
        imovel.area_util,
        imovel.quartos,
        imovel.suites,
        imovel.vagas,
        tem_suite,
        tem_vaga,
        imovel.tipo,
        imovel.bairro
    ]]


@router.post("/venda", response_model=VendaResposta)
def prever_venda(imovel: ImovelEntrada):
    """Retorna o valor previsto de venda de um imóvel."""
    X = montar_features(imovel)
    pred = model_loader.modelo_venda.predict(X)[0]
    return {"valor_previsto_venda": float(pred)}


@router.post("/locacao", response_model=LocacaoResposta)
def prever_locacao(imovel: ImovelEntrada):
    """Retorna o valor previsto de locacao de um imóvel."""
    X = montar_features(imovel)
    pred = model_loader.modelo_locacao.predict(X)[0]
    return {"valor_previsto_locacao": float(pred)}


@router.post("/completo", response_model=CompletoResposta)
def prever_completo(imovel: ImovelEntrada):
    """Retorna previsão conjunta de valor de venda e locacao."""
    X = montar_features(imovel)
    venda = model_loader.modelo_venda.predict(X)[0]
    locacao = model_loader.modelo_locacao.predict(X)[0]

    return {
        "valor_previsto_venda": float(venda),
        "valor_previsto_locacao": float(locacao),
    }
