from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.models.servicio_municipal import ServicioMunicipal, ServicioItem
from app.schemas.schemas import ServicioMunicipalCreate, ServicioMunicipalUpdate


class ServicioMunicipalService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, solo_activos: bool = True) -> List[ServicioMunicipal]:
        query = (
            select(ServicioMunicipal)
            .options(selectinload(ServicioMunicipal.items))
            .order_by(ServicioMunicipal.orden)
        )

        if solo_activos:
            query = query.where(ServicioMunicipal.activo == True)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, servicio_id: int) -> Optional[ServicioMunicipal]:
        result = await self.db.execute(
            select(ServicioMunicipal)
            .options(selectinload(ServicioMunicipal.items))
            .where(ServicioMunicipal.id == servicio_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data: ServicioMunicipalCreate) -> ServicioMunicipal:
        servicio = ServicioMunicipal(
            nombre=data.nombre,
            descripcion=data.descripcion,
            direccion=data.direccion,
            maps_url=data.maps_url,
            maps_embed=data.maps_embed,
            foto_url=data.foto_url,
            layout=data.layout,
            activo=data.activo,
            orden=data.orden
        )

        self.db.add(servicio)
        await self.db.flush()

        for item_data in data.items:
            self.db.add(ServicioItem(
                servicio_id=servicio.id,
                titulo=item_data.titulo,
                contenido=item_data.contenido,
                orden=item_data.orden
            ))

        await self.db.commit()

        # ← recargar con selectinload en lugar de refresh
        return await self.get_by_id(servicio.id)
    async def update(self, servicio_id: int, data: ServicioMunicipalUpdate) -> Optional[ServicioMunicipal]:
        servicio = await self.get_by_id(servicio_id)
        if not servicio:
            return None

        for field, value in data.model_dump(exclude={"items"}, exclude_none=True).items():
            setattr(servicio, field, value)

        if data.items is not None:
            await self.db.execute(
                delete(ServicioItem).where(ServicioItem.servicio_id == servicio_id)
            )

            for item_data in data.items:
                self.db.add(ServicioItem(
                    servicio_id=servicio_id,
                    titulo=item_data.titulo,
                    contenido=item_data.contenido,
                    orden=item_data.orden
                ))

        await self.db.commit()
        await self.db.refresh(servicio)
        return await self.get_by_id(servicio_id)  # ← cambia esto

    async def delete(self, servicio_id: int) -> bool:
        servicio = await self.get_by_id(servicio_id)
        if not servicio:
            return False

        await self.db.delete(servicio)
        await self.db.commit()
        return True

    async def toggle_activo(self, servicio_id: int) -> Optional[ServicioMunicipal]:
        servicio = await self.get_by_id(servicio_id)
        if not servicio:
            return None

        servicio.activo = not servicio.activo
        await self.db.commit()
        await self.db.refresh(servicio)
        return await self.get_by_id(servicio_id)  # ← cambia esto