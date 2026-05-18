from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, distinct
from app.models.evento_imagen import Imagen


class ImagenesService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, album: str | None = None) -> list[Imagen]:
        query = select(Imagen).order_by(Imagen.fecha_subida.desc())
        if album:
            query = query.where(Imagen.album == album)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_albumes(self) -> list[str]:
        result = await self.db.execute(
            select(distinct(Imagen.album)).order_by(Imagen.album)
        )
        return result.scalars().all()

    async def get_total(self) -> int:
        result = await self.db.execute(select(Imagen))
        return len(result.scalars().all())

    async def crear(self, titulo: str, url: str, album: str, autor: str, usuario_id: int) -> Imagen:
        imagen = Imagen(
            titulo=titulo, url=url, album=album,
            autor=autor, usuario_id=usuario_id
        )
        self.db.add(imagen)
        await self.db.commit()
        await self.db.refresh(imagen)
        return imagen

    async def eliminar(self, imagen_id: int) -> bool:
        result = await self.db.execute(select(Imagen).where(Imagen.id == imagen_id))
        imagen = result.scalar_one_or_none()
        if not imagen:
            return False
        await self.db.delete(imagen)
        await self.db.commit()
        return True

