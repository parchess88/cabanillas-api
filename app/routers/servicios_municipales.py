from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.schemas import (
    ServicioMunicipalCreate, ServicioMunicipalUpdate, ServicioMunicipalOut
)
from app.services.servicio_municipal_service import ServicioMunicipalService

router = APIRouter(prefix="/servicios-municipales", tags=["Servicios Municipales"])


def get_service(db: AsyncSession = Depends(get_db)) -> ServicioMunicipalService:
    return ServicioMunicipalService(db)


# ── Públicos ──────────────────────────────────────────────────────────────────

@router.get("", response_model=List[ServicioMunicipalOut])
async def get_servicios(
    solo_activos: bool = Query(True),
    svc: ServicioMunicipalService = Depends(get_service),
):
    servicios = await svc.get_all(solo_activos=solo_activos)
    return [ServicioMunicipalOut.from_orm_servicio(s) for s in servicios]


@router.get("/{servicio_id}", response_model=ServicioMunicipalOut)
async def get_servicio(
    servicio_id: int,
    svc: ServicioMunicipalService = Depends(get_service),
):
    servicio = await svc.get_by_id(servicio_id)
    if not servicio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servicio no encontrado")
    return ServicioMunicipalOut.from_orm_servicio(servicio)


@router.post("", response_model=ServicioMunicipalOut, status_code=status.HTTP_201_CREATED)
async def create_servicio(
    data: ServicioMunicipalCreate,
    svc: ServicioMunicipalService = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),
):
    servicio = await svc.create(data)
    return ServicioMunicipalOut.from_orm_servicio(servicio)


@router.put("/{servicio_id}", response_model=ServicioMunicipalOut)
async def update_servicio(
    servicio_id: int,
    data: ServicioMunicipalUpdate,
    svc: ServicioMunicipalService = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),
):
    servicio = await svc.update(servicio_id, data)
    if not servicio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servicio no encontrado")
    return ServicioMunicipalOut.from_orm_servicio(servicio)


@router.patch("/{servicio_id}/toggle", response_model=ServicioMunicipalOut)
async def toggle_activo(
    servicio_id: int,
    svc: ServicioMunicipalService = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),
):
    servicio = await svc.toggle_activo(servicio_id)
    if not servicio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servicio no encontrado")
    return ServicioMunicipalOut.from_orm_servicio(servicio)

@router.delete("/{servicio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_servicio(
    servicio_id: int,
    svc: ServicioMunicipalService = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),
):
    eliminado = await svc.delete(servicio_id)
    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servicio no encontrado")