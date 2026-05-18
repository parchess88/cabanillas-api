from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.schemas import (
    ReglamentoCreate, ReglamentoOut, ReglamentoUpdate, ReglamentosListResponse
)
from app.services.reglamentos_services import ReglamentosService

router = APIRouter(prefix="/reglamentos", tags=["Reglamentos"])


def get_service(db: AsyncSession = Depends(get_db)) -> ReglamentosService:
    return ReglamentosService(db)


@router.get("", response_model=ReglamentosListResponse)
async def get_reglamentos(
    categoria: str | None  = Query(None),
    activa:    bool | None = Query(None),
    search:    str | None  = Query(None),
    page:      int         = Query(1, ge=1),
    pageSize:  int         = Query(50, ge=1, le=100),
    svc: ReglamentosService = Depends(get_service),
):
    reglamentos, total = await svc.get_all(
        categoria=categoria, activa=activa,
        search=search, page=page, page_size=pageSize,
    )
    return ReglamentosListResponse(
        data=[ReglamentoOut.from_orm_reglamento(r) for r in reglamentos],
        total=total, page=page, pageSize=pageSize,
    )


@router.get("/{reglamento_id}", response_model=ReglamentoOut)
async def get_reglamento(
    reglamento_id: int,
    svc: ReglamentosService = Depends(get_service),
):
    reglamento = await svc.get_by_id(reglamento_id)
    if not reglamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reglamento no encontrado")
    return ReglamentoOut.from_orm_reglamento(reglamento)


@router.post("", response_model=ReglamentoOut, status_code=status.HTTP_201_CREATED)
async def crear_reglamento(
    data: ReglamentoCreate,
    svc: ReglamentosService = Depends(get_service),
    current_user: Usuario   = Depends(get_current_user),
):
    reglamento = await svc.crear(data)
    return ReglamentoOut.from_orm_reglamento(reglamento)


@router.put("/{reglamento_id}", response_model=ReglamentoOut)
async def actualizar_reglamento(
    reglamento_id: int,
    data: ReglamentoUpdate,
    svc: ReglamentosService = Depends(get_service),
    current_user: Usuario   = Depends(get_current_user),
):
    reglamento = await svc.actualizar(reglamento_id, data)
    if not reglamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reglamento no encontrado")
    return ReglamentoOut.from_orm_reglamento(reglamento)


@router.delete("/{reglamento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_reglamento(
    reglamento_id: int,
    svc: ReglamentosService = Depends(get_service),
    current_user: Usuario   = Depends(get_current_user),
):
    eliminado = await svc.eliminar(reglamento_id)
    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reglamento no encontrado")



@router.get("/total", tags=["Reglamentos"])
async def get_total(svc: ReglamentosService = Depends(get_service)):
    _, total = await svc.get_all(page=1, page_size=1)
    return {"total": total}