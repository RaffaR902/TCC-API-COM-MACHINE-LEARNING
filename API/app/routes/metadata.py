from fastapi import APIRouter

router = APIRouter(prefix="/info", tags=["Informações"])

TIPOS_IMOVEIS = [
    "casa", "apartamento"
]

ESTADOS = {
    "SP": ["São Paulo"]
}

@router.get("/tipos-imoveis")
def listar_tipos():
    return {"tipos_suportados": TIPOS_IMOVEIS}

@router.get("/estados")
def listar_estados():
    return {"estados_disponiveis": list(ESTADOS.keys())}

@router.get("/cidades/{estado}")
def listar_cidades(estado: str):
    estado = estado.upper()
    if estado not in ESTADOS:
        return {"erro": "Estado não encontrado."}
    return {"estado": estado, "cidades": ESTADOS[estado]}

@router.get("/status")
def status():
    return {"status": "OK", "mensagem": "API operando normalmente"}

@router.get("/modelo/versao")
def versao_modelo():
    return {"versao_modelo": "1.0.0"}
