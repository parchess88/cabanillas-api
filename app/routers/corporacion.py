from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.schemas import (
    PartidoCreate, PartidoOut, PartidoUpdate, PartidosListResponse,
    MiembroCreate, MiembroOut, MiembroUpdate
)
from app.services.corporacion_service import CorporacionService

router = APIRouter(prefix="/corporacion", tags=["Corporación"])


def get_service(db: AsyncSession = Depends(get_db)) -> CorporacionService:
    return CorporacionService(db)


# ── Partidos ──────────────────────────────────────────────────

@router.get("/partidos", response_model=PartidosListResponse)
async def get_partidos(
    activo: bool | None    = Query(None),
    svc: CorporacionService = Depends(get_service),
):
    partidos = await svc.get_partidos(activo=activo)
    return PartidosListResponse(data=[PartidoOut.from_orm_partido(p) for p in partidos], total=len(partidos))


@router.get("/partidos/{partido_id}", response_model=PartidoOut)
async def get_partido(
    partido_id: int,
    svc: CorporacionService = Depends(get_service),
):
    partido = await svc.get_partido(partido_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return PartidoOut.from_orm_partido(partido)


@router.post("/partidos", response_model=PartidoOut, status_code=status.HTTP_201_CREATED)
async def crear_partido(
    data: PartidoCreate,
    svc: CorporacionService  = Depends(get_service),
    current_user: Usuario    = Depends(get_current_user),
):
    partido = await svc.crear_partido(data)
    return PartidoOut.from_orm_partido(partido)


@router.put("/partidos/{partido_id}", response_model=PartidoOut)
async def actualizar_partido(
    partido_id: int,
    data: PartidoUpdate,
    svc: CorporacionService  = Depends(get_service),
    current_user: Usuario    = Depends(get_current_user),
):
    partido = await svc.actualizar_partido(partido_id, data)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return PartidoOut.from_orm_partido(partido)


@router.delete("/partidos/{partido_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_partido(
    partido_id: int,
    svc: CorporacionService  = Depends(get_service),
    current_user: Usuario    = Depends(get_current_user),
):
    if not await svc.eliminar_partido(partido_id):
        raise HTTPException(status_code=404, detail="Partido no encontrado")


# ── Miembros ──────────────────────────────────────────────────

@router.post("/miembros", response_model=MiembroOut, status_code=status.HTTP_201_CREATED)
async def crear_miembro(
    data: MiembroCreate,
    svc: CorporacionService  = Depends(get_service),
    current_user: Usuario    = Depends(get_current_user),
):
    miembro = await svc.crear_miembro(data)
    return MiembroOut.from_orm_miembro(miembro)


@router.put("/miembros/{miembro_id}", response_model=MiembroOut)
async def actualizar_miembro(
    miembro_id: int,
    data: MiembroUpdate,
    svc: CorporacionService  = Depends(get_service),
    current_user: Usuario    = Depends(get_current_user),
):
    miembro = await svc.actualizar_miembro(miembro_id, data)
    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    return MiembroOut.from_orm_miembro(miembro)


@router.delete("/miembros/{miembro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_miembro(
    miembro_id: int,
    svc: CorporacionService  = Depends(get_service),
    current_user: Usuario    = Depends(get_current_user),
):
    if not await svc.eliminar_miembro(miembro_id):
        raise HTTPException(status_code=404, detail="Miembro no encontrado")