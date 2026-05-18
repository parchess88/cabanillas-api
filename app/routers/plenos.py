from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.schemas import (
    PlenoCreate, PlenoOut, PlenoUpdate, PlenosListResponse
)
from app.services.plenos_services import PlenosService

router = APIRouter(prefix="/plenos", tags=["Plenos"])


def get_service(db: AsyncSession = Depends(get_db)) -> PlenosService:
    return PlenosService(db)


@router.get("", response_model=PlenosListResponse)
async def get_plenos(
    anio:     int | None  = Query(None),
    activo:   bool | None = Query(None),
    page:     int         = Query(1, ge=1),
    pageSize: int         = Query(50, ge=1, le=100),
    svc: PlenosService    = Depends(get_service),
):
    plenos, total = await svc.get_all(
        anio=anio, activo=activo,
        page=page, page_size=pageSize,
    )
    return PlenosListResponse(
        data=[PlenoOut.from_orm_pleno(p) for p in plenos],
        total=total, page=page, pageSize=pageSize,
    )


@router.get("/anios", response_model=list[int])
async def get_anios(svc: PlenosService = Depends(get_service)):
    return await svc.get_anios()


@router.get("/{pleno_id}", response_model=PlenoOut)
async def get_pleno(
    pleno_id: int,
    svc: PlenosService = Depends(get_service),
):
    pleno = await svc.get_by_id(pleno_id)
    if not pleno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pleno no encontrado")
    return PlenoOut.from_orm_pleno(pleno)


@router.post("", response_model=PlenoOut, status_code=status.HTTP_201_CREATED)
async def crear_pleno(
    data: PlenoCreate,
    svc: PlenosService  = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),
):
    pleno = await svc.crear(data)
    return PlenoOut.from_orm_pleno(pleno)


@router.put("/{pleno_id}", response_model=PlenoOut)
async def actualizar_pleno(
    pleno_id: int,
    data: PlenoUpdate,
    svc: PlenosService  = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),
):
    pleno = await svc.actualizar(pleno_id, data)
    if not pleno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pleno no encontrado")
    return PlenoOut.from_orm_pleno(pleno)


@router.delete("/{pleno_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_pleno(
    pleno_id: int,
    svc: PlenosService  = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),
):
    eliminado = await svc.eliminar(pleno_id)
    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pleno no encontrado")