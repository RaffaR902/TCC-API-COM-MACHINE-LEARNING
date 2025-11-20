from fastapi import APIRouter

# Cria um roteador para endpoints relacionados a informações gerais da API
router = APIRouter(prefix="/info", tags=["Informações"])

# Lista de tipos de imóveis que a API suporta para previsão
TIPOS_IMOVEIS = [
    "casa", "apartamento"
]

# Dicionário com estados e suas respectivas cidades atendidas pelo modelo
ESTADOS = {
    "SP": ["São Paulo"]
}

@router.get("/tipos-imoveis")
def listar_tipos():
    """
    Retorna a lista de tipos de imóveis suportados pela API.
    """
    return {"tipos_suportados": TIPOS_IMOVEIS}

@router.get("/estados")
def listar_estados():
    """
    Retorna todos os estados disponíveis para previsão de preços.
    """
    return {"estados_disponiveis": list(ESTADOS.keys())}

@router.get("/cidades/{estado}")
def listar_cidades(estado: str):
    """
    Retorna as cidades disponíveis para um estado específico.
    O estado é enviado na URL (exemplo: /cidades/SP).
    """
    estado = estado.upper()
    
    if estado not in ESTADOS:
        return {"erro": "Estado não encontrado."}

    return {"estado": estado, "cidades": ESTADOS[estado]}
