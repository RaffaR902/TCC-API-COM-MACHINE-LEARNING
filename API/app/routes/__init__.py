# Importa o objeto 'router' de dentro do arquivo 'previsoes.py'
# e o renomeia para 'previsoes_router' para evitar conflito de nomes.
from .previsoes import router as previsoes_router

# Faz o mesmo para o arquivo 'metadata.py'
from .metadata import router as metadata_router

# Faz o mesmo para o arquivo 'info.py'
from .info import router as info_router

# A lista __all__ define o que será exportado quando alguém fizer:
# "from app.routes import *"
# Isso garante que apenas os routers sejam expostos publicamente pelo pacote.
__all__ = [
    "previsoes_router",
    "metadata_router",
    "info_router"
]