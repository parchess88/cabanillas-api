from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.schemas import (
    OrdenanzaCreate, OrdenanzaOut, OrdenanzaUpdate, OrdenanzasListResponse
)
from app.services.ordenanzas_service import OrdenanzasService

router = APIRouter(prefix="/ordenanzas", tags=["Ordenanzas"])


def get_service(db: AsyncSession = Depends(get_db)) -> OrdenanzasService:
    return OrdenanzasService(db)


# ── GET /ordenanzas ──────────────────────────────────────────
@router.get("", response_model=OrdenanzasListResponse)
async def get_ordenanzas(
    categoria: str | None  = Query(None),
    activa:    bool | None = Query(None),
    search:    str | None  = Query(None),
    page:      int         = Query(1, ge=1),
    pageSize:  int         = Query(50, ge=1, le=100),
    svc: OrdenanzasService = Depends(get_service),
):
    ordenanzas, total = await svc.get_all(
        categoria=categoria,
        activa=activa,
        search=search,
        page=page,
        page_size=pageSize,
    )
    return OrdenanzasListResponse(
        data=[OrdenanzaOut.from_orm_ordenanza(o) for o in ordenanzas],
        total=total,
        page=page,
        pageSize=pageSize,
    )


# ── GET /ordenanzas/{id} ─────────────────────────────────────
@router.get("/{ordenanza_id}", response_model=OrdenanzaOut)
async def get_ordenanza(
    ordenanza_id: int,
    svc: OrdenanzasService = Depends(get_service),
):
    ordenanza = await svc.get_by_id(ordenanza_id)
    if not ordenanza:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ordenanza no encontrada")
    return OrdenanzaOut.from_orm_ordenanza(ordenanza)


# ── POST /ordenanzas ─────────────────────────────────────────
@router.post("", response_model=OrdenanzaOut, status_code=status.HTTP_201_CREATED)
async def crear_ordenanza(
    data: OrdenanzaCreate,
    svc: OrdenanzasService = Depends(get_service),
    current_user: Usuario  = Depends(get_current_user),
):
    ordenanza = await svc.crear(data)
    return OrdenanzaOut.from_orm_ordenanza(ordenanza)


# ── PUT /ordenanzas/{id} ─────────────────────────────────────
@router.put("/{ordenanza_id}", response_model=OrdenanzaOut)
async def actualizar_ordenanza(
    ordenanza_id: int,
    data: OrdenanzaUpdate,
    svc: OrdenanzasService = Depends(get_service),
    current_user: Usuario  = Depends(get_current_user),
):
    ordenanza = await svc.actualizar(ordenanza_id, data)
    if not ordenanza:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ordenanza no encontrada")
    return OrdenanzaOut.from_orm_ordenanza(ordenanza)


# ── DELETE /ordenanzas/{id} ──────────────────────────────────
@router.delete("/{ordenanza_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_ordenanza(
    ordenanza_id: int,
    svc: OrdenanzasService = Depends(get_service),
    current_user: Usuario  = Depends(get_current_user),
):
    eliminada = await svc.eliminar(ordenanza_id)
    if not eliminada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ordenanza no encontrada")


@router.get("/total", tags=["Ordenanzas"])
async def get_total(svc: OrdenanzasService = Depends(get_service)):
    _, total = await svc.get_all(page=1, page_size=1)
    return {"total": total}