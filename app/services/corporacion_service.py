from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.models.corporacion import Partido, MiembroCorporacion
from app.schemas.schemas import PartidoCreate, PartidoUpdate, MiembroCreate, MiembroUpdate


class CorporacionService:

    def __init__(self, db: AsyncSession):
        self.db = db

    # ── Partidos ──────────────────────────────────────────────

    async def get_partidos(self, activo: bool | None = None) -> list[Partido]:
        query = (
            select(Partido)
            .options(selectinload(Partido.miembros))
            .order_by(Partido.orden)
        )
        if activo is not None:
            query = query.where(Partido.activo == activo)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_partido(self, partido_id: int) -> Partido | None:
        result = await self.db.execute(
            select(Partido)
            .options(selectinload(Partido.miembros))
            .where(Partido.id == partido_id)
        )
        return result.scalar_one_or_none()

    async def crear_partido(self, data: PartidoCreate) -> Partido:
        partido = Partido(
            nombre=data.nombre,
            logo_url=data.logo_url,
            color=data.color,
            orden=data.orden,
            activo=data.activo,
        )
        self.db.add(partido)
        await self.db.commit()
        await self.db.refresh(partido)
        return await self.get_partido(partido.id)

    async def actualizar_partido(self, partido_id: int, data: PartidoUpdate) -> Partido | None:
        partido = await self.get_partido(partido_id)
        if not partido:
            return None
        campos = data.model_dump(exclude_unset=True)
        for campo, valor in campos.items():
            setattr(partido, campo, valor)
        await self.db.commit()
        return await self.get_partido(partido_id)

    async def eliminar_partido(self, partido_id: int) -> bool:
        partido = await self.get_partido(partido_id)
        if not partido:
            return False
        await self.db.delete(partido)
        await self.db.commit()
        return True

    # ── Miembros ──────────────────────────────────────────────

    async def get_miembro(self, miembro_id: int) -> MiembroCorporacion | None:
        result = await self.db.execute(
            select(MiembroCorporacion).where(MiembroCorporacion.id == miembro_id)
        )
        return result.scalar_one_or_none()

    async def crear_miembro(self, data: MiembroCreate) -> MiembroCorporacion:
        miembro = MiembroCorporacion(
            partido_id=data.partido_id,
            nombre=data.nombre,
            cargo=data.cargo,
            foto_url=data.foto_url,
            descripcion=data.descripcion,
            orden=data.orden,
            activo=data.activo,
        )
        self.db.add(miembro)
        await self.db.commit()
        await self.db.refresh(miembro)
        return miembro

    async def actualizar_miembro(self, miembro_id: int, data: MiembroUpdate) -> MiembroCorporacion | None:
        miembro = await self.get_miembro(miembro_id)
        if not miembro:
            return None
        campos = data.model_dump(exclude_unset=True)
        for campo, valor in campos.items():
            setattr(miembro, campo, valor)
        await self.db.commit()
        await self.db.refresh(miembro)
        return miembro

    async def eliminar_miembro(self, miembro_id: int) -> bool:
        miembro = await self.get_miembro(miembro_id)
        if not miembro:
            return False
        await self.db.delete(miembro)
        await self.db.commit()
        return True