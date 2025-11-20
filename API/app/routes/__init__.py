from .previsoes import router as previsoes_router
from .metadata import router as metadata_router
from .info import router as info_router

__all__ = [
    "previsoes_router",
    "metadata_router",
    "info_router"
]
