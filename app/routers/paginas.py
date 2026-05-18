from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.schemas import PaginaCreate, PaginaOut, PaginaUpdate, PaginasListResponse
from app.services.pagina_service import PaginasService

router = APIRouter(prefix="/paginas", tags=["Páginas"])


def get_service(db: AsyncSession = Depends(get_db)) -> PaginasService:
    return PaginasService(db)


@router.get("", response_model=PaginasListResponse)
async def get_paginas(
    activa: bool | None    = Query(None),
    svc: PaginasService    = Depends(get_service),
):
    paginas, total = await svc.get_all(activa=activa)
    return PaginasListResponse(data=[PaginaOut.from_orm_pagina(p) for p in paginas], total=total)


@router.get("/{slug}", response_model=PaginaOut)
async def get_pagina(
    slug: str,
    svc: PaginasService = Depends(get_service),
):
    pagina = await svc.get_by_slug(slug)
    if not pagina or not pagina.activa:
        raise HTTPException(status_code=404, detail="Página no encontrada")
    return PaginaOut.from_orm_pagina(pagina)


@router.post("", response_model=PaginaOut, status_code=status.HTTP_201_CREATED)
async def crear_pagina(
    data: PaginaCreate,
    svc: PaginasService   = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),
):
    pagina = await svc.crear(data)
    return PaginaOut.from_orm_pagina(pagina)


@router.put("/{pagina_id}", response_model=PaginaOut)
async def actualizar_pagina(
    pagina_id: int,
    data: PaginaUpdate,
    svc: PaginasService   = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),
):
    pagina = await svc.actualizar(pagina_id, data)
    if not pagina:
        raise HTTPException(status_code=404, detail="Página no encontrada")
    return PaginaOut.from_orm_pagina(pagina)


@router.delete("/{pagina_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_pagina(
    pagina_id: int,
    svc: PaginasService   = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),
):
    if not await svc.eliminar(pagina_id):
        raise HTTPException(status_code=404, detail="Página no encontrada")