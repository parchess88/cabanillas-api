from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.models.paginas import Pagina
from app.schemas.schemas import PaginaCreate, PaginaUpdate
import re


def slugify(texto: str) -> str:
    texto = texto.lower().strip()
    texto = re.sub(r'[áàäâ]', 'a', texto)
    texto = re.sub(r'[éèëê]', 'e', texto)
    texto = re.sub(r'[íìïî]', 'i', texto)
    texto = re.sub(r'[óòöô]', 'o', texto)
    texto = re.sub(r'[úùüû]', 'u', texto)
    texto = re.sub(r'[ñ]', 'n', texto)
    texto = re.sub(r'[^a-z0-9\s-]', '', texto)
    texto = re.sub(r'[\s-]+', '-', texto)
    return texto.strip('-')


class PaginasService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, activa: bool | None = None) -> tuple[list[Pagina], int]:
        query = select(Pagina).order_by(Pagina.created_at.desc())
        if activa is not None:
            query = query.where(Pagina.activa == activa)
        count_q = select(func.count()).select_from(query.subquery())
        total   = (await self.db.execute(count_q)).scalar_one()
        result  = await self.db.execute(query)
        return result.scalars().all(), total

    async def get_by_slug(self, slug: str) -> Pagina | None:
        result = await self.db.execute(select(Pagina).where(Pagina.slug == slug))
        return result.scalar_one_or_none()

    async def get_by_id(self, pagina_id: int) -> Pagina | None:
        result = await self.db.execute(select(Pagina).where(Pagina.id == pagina_id))
        return result.scalar_one_or_none()

    async def crear(self, data: PaginaCreate) -> Pagina:
        slug = data.slug or slugify(data.titulo)
        pagina = Pagina(
            titulo=data.titulo, slug=slug,
            contenido=data.contenido, descripcion=data.descripcion,
            activa=data.activa,
        )
        self.db.add(pagina)
        await self.db.commit()
        await self.db.refresh(pagina)
        return pagina

    async def actualizar(self, pagina_id: int, data: PaginaUpdate) -> Pagina | None:
        pagina = await self.get_by_id(pagina_id)
        if not pagina:
            return None
        campos = data.model_dump(exclude_unset=True)
        for campo, valor in campos.items():
            setattr(pagina, campo, valor)
        await self.db.commit()
        await self.db.refresh(pagina)
        return pagina

    async def eliminar(self, pagina_id: int) -> bool:
        pagina = await self.get_by_id(pagina_id)
        if not pagina:
            return False
        await self.db.delete(pagina)
        await self.db.commit()
        return True