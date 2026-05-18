from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.schemas import PoliticaPrivacidadCreate, PoliticaPrivacidadOut, PoliticaPrivacidadUpdate, PoliticaListResponse
from app.services.politica_service import PoliticaService

router = APIRouter(prefix="/politica-privacidad", tags=["Política de Privacidad"])


def get_service(db: AsyncSession = Depends(get_db)) -> PoliticaService:
    return PoliticaService(db)


@router.get("", response_model=PoliticaListResponse)
async def get_politica(
    activo: bool | None   = Query(None),
    svc: PoliticaService  = Depends(get_service),
):
    items, total = await svc.get_all(activo=activo)
    return PoliticaListResponse(data=[PoliticaPrivacidadOut.from_orm_politica(i) for i in items], total=total)


@router.post("", response_model=PoliticaPrivacidadOut, status_code=status.HTTP_201_CREATED)
async def crear(
    data: PoliticaPrivacidadCreate,
    svc: PoliticaService  = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),
):
    item = await svc.crear(data)
    return PoliticaPrivacidadOut.from_orm_politica(item)


@router.put("/{item_id}", response_model=PoliticaPrivacidadOut)
async def actualizar(
    item_id: int,
    data: PoliticaPrivacidadUpdate,
    svc: PoliticaService  = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),
):
    item = await svc.actualizar(item_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="No encontrado")
    return PoliticaPrivacidadOut.from_orm_politica(item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar(
    item_id: int,
    svc: PoliticaService  = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),
):
    if not await svc.eliminar(item_id):
        raise HTTPException(status_code=404, detail="No encontrado")