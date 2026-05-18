from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, extract

from app.models.plenos import Pleno
from app.schemas.schemas import PlenoCreate, PlenoUpdate


class PlenosService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(
        self,
        anio:      int | None = None,
        activo:    bool | None = None,
        page:      int = 1,
        page_size: int = 50,
    ) -> tuple[list[Pleno], int]:

        query = select(Pleno).order_by(Pleno.fecha.desc())

        if anio is not None:
            query = query.where(extract('year', Pleno.fecha) == anio)
        if activo is not None:
            query = query.where(Pleno.activo == activo)

        count_q = select(func.count()).select_from(query.subquery())
        total   = (await self.db.execute(count_q)).scalar_one()
        result  = await self.db.execute(query.offset((page - 1) * page_size).limit(page_size))
        plenos  = result.scalars().all()

        return plenos, total

    async def get_anios(self) -> list[int]:
        result = await self.db.execute(
            select(extract('year', Pleno.fecha).label('anio'))
            .where(Pleno.activo == True)
            .distinct()
            .order_by(extract('year', Pleno.fecha).desc())
        )
        return [int(row.anio) for row in result.fetchall()]

    async def get_by_id(self, pleno_id: int) -> Pleno | None:
        result = await self.db.execute(
            select(Pleno).where(Pleno.id == pleno_id)
        )
        return result.scalar_one_or_none()

    async def crear(self, data: PlenoCreate) -> Pleno:
        pleno = Pleno(
            titulo=data.titulo,
            descripcion=data.descripcion,
            fecha=data.fecha,
            url_pdf=data.url_pdf,
            url_youtube=data.url_youtube,
            activo=data.activo,
        )
        self.db.add(pleno)
        await self.db.commit()
        await self.db.refresh(pleno)
        return pleno

    async def actualizar(self, pleno_id: int, data: PlenoUpdate) -> Pleno | None:
        pleno = await self.get_by_id(pleno_id)
        if not pleno:
            return None

        campos = data.model_dump(exclude_unset=True)
        for campo, valor in campos.items():
            setattr(pleno, campo, valor)

        await self.db.commit()
        await self.db.refresh(pleno)
        return pleno

    async def eliminar(self, pleno_id: int) -> bool:
        pleno = await self.get_by_id(pleno_id)
        if not pleno:
            return False

        await self.db.delete(pleno)
        await self.db.commit()
        return True