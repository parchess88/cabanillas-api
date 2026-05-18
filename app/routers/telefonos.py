from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.schemas import TelefonoInteresCreate, TelefonoInteresOut, TelefonoInteresUpdate, TelefonosListResponse
from app.services.telefonos_service import TelefonosService

router = APIRouter(prefix="/telefonos", tags=["Teléfonos de Interés"])


def get_service(db: AsyncSession = Depends(get_db)) -> TelefonosService:
    return TelefonosService(db)


@router.get("", response_model=TelefonosListResponse)
async def get_telefonos(
    activo: bool | None    = Query(None),
    svc: TelefonosService  = Depends(get_service),
):
    items, total = await svc.get_all(activo=activo)
    return TelefonosListResponse(data=[TelefonoInteresOut.from_orm_telefono(i) for i in items], total=total)


@router.post("", response_model=TelefonoInteresOut, status_code=status.HTTP_201_CREATED)
async def crear(
    data: TelefonoInteresCreate,
    svc: TelefonosService  = Depends(get_service),
    current_user: Usuario  = Depends(get_current_user),
):
    item = await svc.crear(data)
    return TelefonoInteresOut.from_orm_telefono(item)


@router.put("/{item_id}", response_model=TelefonoInteresOut)
async def actualizar(
    item_id: int,
    data: TelefonoInteresUpdate,
    svc: TelefonosService  = Depends(get_service),
    current_user: Usuario  = Depends(get_current_user),
):
    item = await svc.actualizar(item_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="No encontrado")
    return TelefonoInteresOut.from_orm_telefono(item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar(
    item_id: int,
    svc: TelefonosService  = Depends(get_service),
    current_user: Usuario  = Depends(get_current_user),
):
    if not await svc.eliminar(item_id):
        raise HTTPException(status_code=404, detail="No encontrado")