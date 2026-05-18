from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.schemas import ContactoOut, ContactoUpdate, ContactoListResponse
from app.services.contacto_service import ContactoService

router = APIRouter(prefix="/contacto", tags=["Contacto"])


def get_service(db: AsyncSession = Depends(get_db)) -> ContactoService:
    return ContactoService(db)


@router.get("", response_model=ContactoListResponse)
async def get_contacto(svc: ContactoService = Depends(get_service)):
    items = await svc.get_all()
    return ContactoListResponse(data=[ContactoOut.from_orm_contacto(i) for i in items], total=len(items))


@router.put("/{clave}", response_model=ContactoOut)
async def actualizar_contacto(
    clave: str,
    data: ContactoUpdate,
    svc: ContactoService  = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),
):
    item = await svc.actualizar(clave, data)
    if not item:
        raise HTTPException(status_code=404, detail="Campo no encontrado")
    return ContactoOut.from_orm_contacto(item)