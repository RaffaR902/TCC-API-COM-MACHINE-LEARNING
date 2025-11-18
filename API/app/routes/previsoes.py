from fastapi import APIRouter
from app.schemas import ImovelEntrada, VendaResposta, AluguelResposta, CompletoResposta
from app.model_loader import model_loader

router = APIRouter(prefix="/prever", tags=["Previsões"])

@router.post("/venda", response_model=VendaResposta)
def prever_venda(imovel: ImovelEntrada):
    # Transforme o input no formato que seu modelo espera
    
    # montar features derivadas
    tem_suite = 1 if imovel.suites > 0 else 0
    tem_vaga = 1 if imovel.vagas > 0 else 0

    # vetor final na ORDEM usada no treinamento
    X = [[
        imovel.area_util,
        imovel.quartos,
        imovel.suites,
        imovel.vagas,
        tem_suite,
        tem_vaga,
        imovel.tipo,
        imovel.bairro
    ]]

    pred = model_loader.modelo_venda.predict(X)[0]
    return {"valor_previsto_venda": float(pred)}


@router.post("/aluguel", response_model=AluguelResposta)
def prever_aluguel(imovel: ImovelEntrada):
    X = [[
        imovel.area_m2,
        imovel.quartos or 0,
        imovel.banheiros or 0,
    ]]

    pred = model_loader.modelo_aluguel.predict(X)[0]
    return {"valor_previsto_aluguel": float(pred)}


@router.post("/completo", response_model=CompletoResposta)
def prever_completo(imovel: ImovelEntrada):
    X = [[
        imovel.area_m2,
        imovel.quartos or 0,
        imovel.banheiros or 0,
    ]]

    venda = model_loader.modelo_venda.predict(X)[0]
    aluguel = model_loader.modelo_aluguel.predict(X)[0]

    return {
        "valor_previsto_venda": float(venda),
        "valor_previsto_aluguel": float(aluguel),
    }
