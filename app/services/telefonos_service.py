from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.models.telefonos_interes import TelefonoInteres
from app.schemas.schemas import TelefonoInteresCreate, TelefonoInteresUpdate


class TelefonosService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, activo: bool | None = None) -> tuple[list[TelefonoInteres], int]:
        query = select(TelefonoInteres).order_by(TelefonoInteres.orden)
        if activo is not None:
            query = query.where(TelefonoInteres.activo == activo)
        count_q = select(func.count()).select_from(query.subquery())
        total   = (await self.db.execute(count_q)).scalar_one()
        result  = await self.db.execute(query)
        return result.scalars().all(), total

    async def get_by_id(self, item_id: int) -> TelefonoInteres | None:
        result = await self.db.execute(
            select(TelefonoInteres).where(TelefonoInteres.id == item_id)
        )
        return result.scalar_one_or_none()

    async def crear(self, data: TelefonoInteresCreate) -> TelefonoInteres:
        item = TelefonoInteres(
            nombre=data.nombre, localidad=data.localidad,
            telefono=data.telefono, movil=data.movil, fax=data.fax,
            orden=data.orden, activo=data.activo,
        )
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def actualizar(self, item_id: int, data: TelefonoInteresUpdate) -> TelefonoInteres | None:
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