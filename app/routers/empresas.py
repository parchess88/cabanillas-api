from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.schemas import EmpresaCreate, EmpresaOut, EmpresaUpdate, EmpresasListResponse
from app.services.empresas_service import EmpresasService

router = APIRouter(prefix="/empresas", tags=["Directorio Empresas"])


def get_service(db: AsyncSession = Depends(get_db)) -> EmpresasService:
    return EmpresasService(db)


@router.get("", response_model=EmpresasListResponse)
async def get_empresas(
    categoria: str | None  = Query(None),
    activo: bool | None    = Query(None),
    svc: EmpresasService   = Depends(get_service),
):
    items, total = await svc.get_all(categoria=categoria, activo=activo)
    return EmpresasListResponse(data=[EmpresaOut.from_orm_empresa(i) for i in items], total=total)


@router.get("/categorias", response_model=list[str])
async def get_categorias(svc: EmpresasService = Depends(get_service)):
    return await svc.get_categorias()


@router.get("/{empresa_id}", response_model=EmpresaOut)
async def get_empresa(
    empresa_id: int,
    svc: EmpresasService = Depends(get_service),
):
    empresa = await svc.get_by_id(empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return EmpresaOut.from_orm_empresa(empresa)


@router.post("", response_model=EmpresaOut, status_code=status.HTTP_201_CREATED)
async def crear_empresa(
    data: EmpresaCreate,
    svc: EmpresasService  = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),
):
    empresa = await svc.crear(data)
    return EmpresaOut.from_orm_empresa(empresa)


@router.put("/{empresa_id}", response_model=EmpresaOut)
async def actualizar_empresa(
    empresa_id: int,
    data: EmpresaUpdate,
    svc: EmpresasService  = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),
):
    empresa = await svc.actualizar(empresa_id, data)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return EmpresaOut.from_orm_empresa(empresa)


@router.delete("/{empresa_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_empresa(
    empresa_id: int,
    svc: EmpresasService  = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),
):
    if not await svc.eliminar(empresa_id):
        raise HTTPException(status_code=404, detail="Empresa no encontrada")