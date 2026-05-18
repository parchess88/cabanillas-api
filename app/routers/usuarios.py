from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user, get_current_admin
from app.models.usuario import Usuario
from app.schemas.schemas import UsuarioOut, UsuarioCreate, UsuarioUpdate
from app.services.usuarios_service import UsuariosService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


class PasswordChange(BaseModel):
    password: str


def get_service(db: AsyncSession = Depends(get_db)) -> UsuariosService:
    return UsuariosService(db)


@router.get("", response_model=list[UsuarioOut])
async def get_usuarios(
    svc: UsuariosService = Depends(get_service),
    _admin: Usuario = Depends(get_current_admin),
):
    usuarios = await svc.get_all()
    return [UsuarioOut.model_validate(u) for u in usuarios]


@router.get("/me", response_model=UsuarioOut)
async def get_me(current_user: Usuario = Depends(get_current_user)):
    return UsuarioOut.model_validate(current_user)


@router.post("", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
async def crear_usuario(
    data: UsuarioCreate,
    svc: UsuariosService  = Depends(get_service),
    _admin: Usuario       = Depends(get_current_admin),
):
    existente = await svc.get_by_email(data.email)
    if existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya está registrado")
    usuario = await svc.crear(data)
    return UsuarioOut.model_validate(usuario)


@router.put("/{usuario_id}", response_model=UsuarioOut)
async def actualizar_usuario(
    usuario_id: int,
    data: UsuarioUpdate,
    svc: UsuariosService = Depends(get_service),
    _admin: Usuario      = Depends(get_current_admin),
):
    usuario = await svc.actualizar(usuario_id, data)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return UsuarioOut.model_validate(usuario)


@router.patch("/{usuario_id}/password", status_code=status.HTTP_204_NO_CONTENT)
async def cambiar_password(
    usuario_id: int,
    data: PasswordChange,
    svc: UsuariosService = Depends(get_service),
    _admin: Usuario      = Depends(get_current_admin),
):
    if not data.password or len(data.password) < 6:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 6 caracteres")
    ok = await svc.cambiar_password(usuario_id, data.password)
    if not ok:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(
    usuario_id: int,
    svc: UsuariosService   = Depends(get_service),
    current_admin: Usuario = Depends(get_current_admin),
):
    if usuario_id == current_admin.id:
        raise HTTPException(status_code=400, detail="No puedes eliminar tu propia cuenta")
    ok = await svc.eliminar(usuario_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")