from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.schemas import DirectorioCreate, DirectorioOut, DirectorioUpdate, DirectorioListResponse
from app.services.directorio_service import DirectorioService

router = APIRouter(prefix="/directorio", tags=["Directorio"])


def get_service(db: AsyncSession = Depends(get_db)) -> DirectorioService:
    return DirectorioService(db)


@router.get("", response_model=DirectorioListResponse)
async def get_directorio(
    activo: bool | None       = Query(None),
    svc: DirectorioService    = Depends(get_service),
):
    items, total = await svc.get_all(activo=activo)
    return DirectorioListResponse(data=[DirectorioOut.from_orm_directorio(i) for i in items], total=total)


@router.post("", response_model=DirectorioOut, status_code=status.HTTP_201_CREATED)
async def crear(
    data: DirectorioCreate,
    svc: DirectorioService    = Depends(get_service),
    current_user: Usuario     = Depends(get_current_user),
):
    item = await svc.crear(data)
    return DirectorioOut.from_orm_directorio(item)


@router.put("/{item_id}", response_model=DirectorioOut)
async def actualizar(
    item_id: int,
    data: DirectorioUpdate,
    svc: DirectorioService    = Depends(get_service),
    current_user: Usuario     = Depends(get_current_user),
):
    item = await svc.actualizar(item_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="Elemento no encontrado")
    return DirectorioOut.from_orm_directorio(item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar(
    item_id: int,
    svc: DirectorioService    = Depends(get_service),
    current_user: Usuario     = Depends(get_current_user),
):
    if not await svc.eliminar(item_id):
        raise HTTPException(status_code=404, detail="Elemento no encontrado")