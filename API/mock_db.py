# mock_db.py
from fastapi import HTTPException

# --- Dados Falsos (Simulando um Banco de Dados) ---

_TIPOS_IMOVEIS = ["apartamento", "casa", "cobertura", "loft"]

_ESTADOS = ["SP"]

_CIDADES_POR_ESTADO = {
    "SP": ["São Paulo", "Campinas", "Santos"],
    
}

_BAIRROS_POR_CIDADE = {
    "SP": {
        "São Paulo": ["Pinheiros", "Moema", "Tatuapé", "Vila Madalena"],
        
    },
    
    
}

_ESTATISTICAS_BAIRRO = {
    "SP": {
        "São Paulo": {
            "Pinheiros": {
                "media_venda": 950000, "valor_minimo_venda": 650000, "valor_maximo_venda": 1500000,
                "media_aluguel": 3800, "valor_minimo_aluguel": 2500, "valor_maximo_aluguel": 5500
            },
            "Moema": {
                "media_venda": 1200000, "valor_minimo_venda": 800000, "valor_maximo_venda": 2000000,
                "media_aluguel": 4500, "valor_minimo_aluguel": 3000, "valor_maximo_aluguel": 6000
            }
        }
    }
}

# --- Funções de Acesso (CRUD Falso) ---

def get_tipos_imoveis():
    return {"tipos_disponiveis": _TIPOS_IMOVEIS}

def get_estados():
    return {"estados": _ESTADOS}

def get_cidades_por_estado(uf: str):
    uf_upper = uf.upper()
    if uf_upper not in _CIDADES_POR_ESTADO:
        raise HTTPException(status_code=404, detail=f"Estado (UF) '{uf}' não encontrado.")
    return {
        "estado": uf_upper,
        "cidades": _CIDADES_POR_ESTADO[uf_upper]
    }

def get_bairros_por_cidade(uf: str, cidade: str):
    uf_upper = uf.upper()
    if uf_upper not in _BAIRROS_POR_CIDADE:
        raise HTTPException(status_code=404, detail=f"Estado (UF) '{uf}' não encontrado.")
    
    cidades_do_estado = _BAIRROS_POR_CIDADE[uf_upper]
    
    # Procura pela cidade (case-insensitive)
    cidade_encontrada = next((c for c in cidades_do_estado if c.lower() == cidade.lower()), None)

    if not cidade_encontrada:
        raise HTTPException(status_code=404, detail=f"Cidade '{cidade}' não encontrada no estado '{uf_upper}'.")
        
    return {
        "estado": uf_upper,
        "cidade": cidade_encontrada,
        "bairros": cidades_do_estado[cidade_encontrada]
    }

def get_estatisticas_bairro(estado: str, cidade: str, bairro: str):
    uf_upper = estado.upper()
    
    if uf_upper not in _ESTATISTICAS_BAIRRO:
        raise HTTPException(status_code=404, detail=f"Dados não disponíveis para o estado '{uf_upper}'.")
    
    cidades_do_estado = _ESTATISTICAS_BAIRRO[uf_upper]
    cidade_encontrada = next((c for c in cidades_do_estado if c.lower() == cidade.lower()), None)
    
    if not cidade_encontrada:
        raise HTTPException(status_code=404, detail=f"Dados não disponíveis para a cidade '{cidade}'.")

    bairros_da_cidade = cidades_do_estado[cidade_encontrada]
    bairro_encontrado_key = next((b for b in bairros_da_cidade if b.lower() == bairro.lower()), None)
    
    if not bairro_encontrado_key:
        raise HTTPException(status_code=404, detail=f"Dados não disponíveis para o bairro '{bairro}'.")

    stats = bairros_da_cidade[bairro_encontrado_key]
    
    return {
        "estado": uf_upper,
        "cidade": cidade_encontrada,
        "bairro": bairro_encontrado_key,
       
    }

