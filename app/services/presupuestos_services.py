from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app.models.presupuestos import Presupuesto
from app.schemas.schemas import PresupuestoCreate, PresupuestoUpdate


class PresupuestosService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(
        self,
        activo:    bool | None = None,
        page:      int = 1,
        page_size: int = 50,
    ) -> tuple[list[Presupuesto], int]:

        query = select(Presupuesto).order_by(Presupuesto.anio.desc())

        if activo is not None:
            query = query.where(Presupuesto.activo == activo)

        count_q      = select(func.count()).select_from(query.subquery())
        total        = (await self.db.execute(count_q)).scalar_one()
        result       = await self.db.execute(query.offset((page - 1) * page_size).limit(page_size))
        presupuestos = result.scalars().all()

        return presupuestos, total

    async def get_ultimo(self) -> Presupuesto | None:
        result = await self.db.execute(
            select(Presupuesto)
            .where(Presupuesto.activo == True)
            .order_by(Presupuesto.anio.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, presupuesto_id: int) -> Presupuesto | None:
        result = await self.db.execute(
            select(Presupuesto).where(Presupuesto.id == presupuesto_id)
        )
        return result.scalar_one_or_none()

    async def crear(self, data: PresupuestoCreate) -> Presupuesto:
        presupuesto = Presupuesto(
            titulo=data.titulo,
            descripcion=data.descripcion,
            anio=data.anio,
            url_pdf=data.url_pdf,
            activo=data.activo,
        )
        self.db.add(presupuesto)
        await self.db.commit()
        await self.db.refresh(presupuesto)
        return presupuesto

    async def actualizar(self, presupuesto_id: int, data: PresupuestoUpdate) -> Presupuesto | None:
        presupuesto = await self.get_by_id(presupuesto_id)
        if not presupuesto:
            return None

        campos = data.model_dump(exclude_unset=True)
        for campo, valor in campos.items():
            setattr(presupuesto, campo, valor)

        await self.db.commit()
        await self.db.refresh(presupuesto)
        return presupuesto

    async def eliminar(self, presupuesto_id: int) -> bool:
        presupuesto = await self.get_by_id(presupuesto_id)
        if not presupuesto:
            return False

        await self.db.delete(presupuesto)
        await self.db.commit()
        return True