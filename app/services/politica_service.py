from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.models.politica_privacidad import PoliticaPrivacidad
from app.schemas.schemas import PoliticaPrivacidadCreate, PoliticaPrivacidadUpdate


class PoliticaService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, activo: bool | None = None) -> tuple[list[PoliticaPrivacidad], int]:
        query = select(PoliticaPrivacidad).order_by(PoliticaPrivacidad.orden)
        if activo is not None:
            query = query.where(PoliticaPrivacidad.activo == activo)
        count_q = select(func.count()).select_from(query.subquery())
        total   = (await self.db.execute(count_q)).scalar_one()
        result  = await self.db.execute(query)
        return result.scalars().all(), total

    async def get_by_id(self, item_id: int) -> PoliticaPrivacidad | None:
        result = await self.db.execute(
            select(PoliticaPrivacidad).where(PoliticaPrivacidad.id == item_id)
        )
        return result.scalar_one_or_none()

    async def crear(self, data: PoliticaPrivacidadCreate) -> PoliticaPrivacidad:
        item = PoliticaPrivacidad(
            titulo=data.titulo, descripcion=data.descripcion,
            url_pdf=data.url_pdf, orden=data.orden, activo=data.activo,
        )
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def actualizar(self, item_id: int, data: PoliticaPrivacidadUpdate) -> PoliticaPrivacidad | None:
        item = await self.get_by_id(item_id)
        if not item:
            return None
        for campo, valor in data.model_dump(exclude_unset=True).items():
            setattr(item, campo, valor)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def eliminar(self, item_id: int) -> bool:
        item = await self.get_by_id(item_id)
        if not item:
            return False
        await self.db.delete(item)
        await self.db.commit()
        return True