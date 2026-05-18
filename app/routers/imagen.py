from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.schemas import ImagenOut
from app.services.imagen_service import ImagenesService

router = APIRouter(prefix="/imagenes", tags=["Imágenes"])


def get_service(db: AsyncSession = Depends(get_db)) -> ImagenesService:
    return ImagenesService(db)


@router.get("", response_model=list[ImagenOut])
async def get_imagenes(
    album: str | None     = Query(None),
    svc: ImagenesService  = Depends(get_service),
):
    imagenes = await svc.get_all(album=album)
    return [ImagenOut.from_orm_imagen(i) for i in imagenes]


@router.get("/albumes", response_model=list[str])
async def get_albumes(svc: ImagenesService = Depends(get_service)):
    return await svc.get_albumes()


@router.post("", response_model=ImagenOut, status_code=status.HTTP_201_CREATED)
async def crear_imagen(
    titulo: str,
    url: str,
    album: str            = "general",
    svc: ImagenesService  = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),
):
    imagen = await svc.crear(
        titulo=titulo, url=url, album=album,
        autor=f"{current_user.nombre} {current_user.apellidos}",
        usuario_id=current_user.id
    )
    return ImagenOut.from_orm_imagen(imagen)


@router.delete("/{imagen_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_imagen(
    imagen_id: int,
    svc: ImagenesService  = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),
):
    if not await svc.eliminar(imagen_id):
        raise HTTPException(status_code=404, detail="Imagen no encontrada")