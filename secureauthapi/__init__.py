from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from .conf import SecureAuthAPISettings
from .core import limiter, scheduler
from .routers.auth import router as auth_router


def setup_secureauthapi(app: FastAPI, config: dict, engine):
    """
    Configura SecureAuthAPI usando dict estilo Django.
    """
    # Construye settings de SecureAuthAPI
    settings = SecureAuthAPISettings(**config)

    # Guarda settings en app.state
    app.state.secureauthapi_settings = settings

    # ✅ Usa el engine del settings principal, no de config directo
    app.state.secureauthapi_engine = engine

    # Configurar Rate Limiting solo para rutas /auth
    app.state.limiter = limiter

    # ⚡ Agregar middleware de SlowAPI
    app.add_middleware(SlowAPIMiddleware)

    # Manejar exceptions de SlowAPI
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Agregar router de autenticación bajo prefijo /auth
    app.include_router(
        auth_router, tags=["Secure Auth API Integration"], prefix="/auth"
    )

    scheduler.start_scheduler()

    return app  # Opcional: por convención
