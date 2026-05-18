from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.routers.auth import router as auth_router
from app.routers.noticias import router as noticias_router
from app.routers.eventos import router as eventos_router
from app.routers.usuarios import router as usuarios_router
from app.routers.ordenanzas import router as ordenanzas_router
from app.routers.presupuestos import router as presupuestos_router
from app.routers.reglamentos import router as reglamentos_router
from app.routers.plenos import router as plenos_router
from app.routers.corporacion import router as corporacion_router
from app.routers.tiempo import router as tiempo_router
from app.routers.directorio import router as directorio_router
from app.routers.contacto import router as contacto_router
from app.routers.paginas import router as paginas_router
from app.routers.ine import router as ine_router
from app.routers.servicios_municipales import router as servicios_municipales_router
from app.routers.telefonos import router as telefonos_router
from app.routers.politica_privacidad import router as politica_router
from app.routers.imagen import router as imagenes_router


import traceback
from fastapi import Request
from fastapi.responses import JSONResponse



settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Acciones al arrancar y apagar la aplicación"""
    print("🚀 Cabanillas API arrancando...")
    yield
    print("🛑 Cabanillas API detenida")


app = FastAPI(
    title="Ayuntamiento de Cabanillas de la Sierra — API",
    description="Backend para la web municipal y el CMS",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     # ReDoc
)

# ── CORS ─────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_detail = traceback.format_exc()
    print("=== ERROR COMPLETO ===")
    print(error_detail)
    print("=== FIN ERROR ===")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "traceback": error_detail}
    )
# ── Routers ──────────────────────────────────────────────────
PREFIX = "/api"

app.include_router(auth_router,      prefix=PREFIX)
app.include_router(noticias_router,  prefix=PREFIX)
app.include_router(eventos_router,   prefix=PREFIX)
app.include_router(usuarios_router,  prefix=PREFIX)
app.include_router(usuarios_router,  prefix=PREFIX)
app.include_router(ordenanzas_router, prefix=PREFIX)
app.include_router(reglamentos_router, prefix=PREFIX)
app.include_router(presupuestos_router, prefix=PREFIX)
app.include_router(plenos_router, prefix=PREFIX)
app.include_router(tiempo_router, prefix=PREFIX)
app.include_router(corporacion_router, prefix=PREFIX)
app.include_router(directorio_router, prefix=PREFIX)
app.include_router(contacto_router, prefix=PREFIX)
app.include_router(paginas_router, prefix=PREFIX)
app.include_router(ine_router, prefix=PREFIX)
app.include_router(servicios_municipales_router, prefix=PREFIX)
app.include_router(telefonos_router, prefix=PREFIX)
app.include_router(politica_router, prefix=PREFIX)
app.include_router(imagenes_router, prefix=PREFIX)

# ── Health check ─────────────────────────────────────────────
@app.get("/", tags=["Estado"])
async def root():
    return {
        "estado": "ok",
        "api": "Cabanillas de la Sierra",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["Estado"])
async def health():
    return {"status": "healthy"}
