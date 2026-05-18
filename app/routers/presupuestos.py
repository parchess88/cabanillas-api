from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.schemas import (
    PresupuestoCreate, PresupuestoOut, PresupuestoUpdate, PresupuestosListResponse
)
from app.services.presupuestos_services import PresupuestosService
router = APIRouter(prefix="/presupuestos", tags=["Presupuestos"])


def get_service(db: AsyncSession = Depends(get_db)) -> PresupuestosService:
    return PresupuestosService(db)


@router.get("", response_model=PresupuestosListResponse)
async def get_presupuestos(
    activo:   bool | None = Query(None),
    page:     int         = Query(1, ge=1),
    pageSize: int         = Query(50, ge=1, le=100),
    svc: PresupuestosService = Depends(get_service),
):
    presupuestos, total = await svc.get_all(
        activo=activo, page=page, page_size=pageSize,
    )
    return PresupuestosListResponse(
        data=[PresupuestoOut.from_orm_presupuesto(p) for p in presupuestos],
        total=total, page=page, pageSize=pageSize,
    )


@router.get("/ultimo", response_model=PresupuestoOut)
async def get_ultimo(svc: PresupuestosService = Depends(get_service)):
    presupuesto = await svc.get_ultimo()
    if not presupuesto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay presupuestos")
    return PresupuestoOut.from_orm_presupuesto(presupuesto)


@router.get("/{presupuesto_id}", response_model=PresupuestoOut)
async def get_presupuesto(
    presupuesto_id: int,
    svc: PresupuestosService = Depends(get_service),
):
    presupuesto = await svc.get_by_id(presupuesto_id)
    if not presupuesto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Presupuesto no encontrado")
    return PresupuestoOut.from_orm_presupuesto(presupuesto)


@router.post("", response_model=PresupuestoOut, status_code=status.HTTP_201_CREATED)
async def crear_presupuesto(
    data: PresupuestoCreate,
    svc: PresupuestosService  = Depends(get_service),
    current_user: Usuario     = Depends(get_current_user),
):
    presupuesto = await svc.crear(data)
    return PresupuestoOut.from_orm_presupuesto(presupuesto)


@router.put("/{presupuesto_id}", response_model=PresupuestoOut)
async def actualizar_presupuesto(
    presupuesto_id: int,
    data: PresupuestoUpdate,
    svc: PresupuestosService = Depends(get_service),
    current_user: Usuario    = Depends(get_current_user),
):
    presupuesto = await svc.actualizar(presupuesto_id, data)
    if not presupuesto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Presupuesto no encontrado")
    return PresupuestoOut.from_orm_presupuesto(presupuesto)


@router.delete("/{presupuesto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_presupuesto(
    presupuesto_id: int,
    svc: PresupuestosService = Depends(get_service),
    current_user: Usuario    = Depends(get_current_user),
):
    eliminado = await svc.eliminar(presupuesto_id)
    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Presupuesto no encontrado")