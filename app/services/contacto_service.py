from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.contacto import Contacto
from app.schemas.schemas import ContactoUpdate


class ContactoService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Contacto]:
        result = await self.db.execute(
            select(Contacto).order_by(Contacto.orden)
        )
        return result.scalars().all()

    async def get_by_clave(self, clave: str) -> Contacto | None:
        result = await self.db.execute(
            select(Contacto).where(Contacto.clave == clave)
        )
        return result.scalar_one_or_none()

    async def actualizar(self, clave: str, data: ContactoUpdate) -> Contacto | None:
        item = await self.get_by_clave(clave)
        if not item:
            return None
        for campo, valor in data.model_dump(exclude_unset=True).items():
            setattr(item, campo, valor)
        await self.db.commit()
        await self.db.refresh(item)
        return item