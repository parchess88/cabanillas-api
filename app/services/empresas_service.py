from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, distinct
from app.models.empresas import Empresa
from app.schemas.schemas import EmpresaCreate, EmpresaUpdate


class EmpresasService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, categoria: str | None = None, activo: bool | None = None) -> tuple[list[Empresa], int]:
        query = select(Empresa).order_by(Empresa.orden, Empresa.nombre)
        if categoria:
            query = query.where(Empresa.categoria == categoria)
        if activo is not None:
            query = query.where(Empresa.activo == activo)
        count_q = select(func.count()).select_from(query.subquery())
        total   = (await self.db.execute(count_q)).scalar_one()
        result  = await self.db.execute(query)
        return result.scalars().all(), total

    async def get_categorias(self) -> list[str]:
        result = await self.db.execute(
            select(distinct(Empresa.categoria)).order_by(Empresa.categoria)
        )
        return result.scalars().all()

    async def get_by_id(self, empresa_id: int) -> Empresa | None:
        result = await self.db.execute(select(Empresa).where(Empresa.id == empresa_id))
        return result.scalar_one_or_none()

    async def crear(self, data: EmpresaCreate) -> Empresa:
        empresa = Empresa(
            nombre=data.nombre, categoria=data.categoria,
            descripcion=data.descripcion, telefono=data.telefono,
            email=data.email, web=data.web, direccion=data.direccion,
            logo_url=data.logo_url, orden=data.orden, activo=data.activo,
        )
        self.db.add(empresa)
        await self.db.commit()
        await self.db.refresh(empresa)
        return empresa

    async def actualizar(self, empresa_id: int, data: EmpresaUpdate) -> Empresa | None:
        empresa = await self.get_by_id(empresa_id)
        if not empresa:
            return None
        for campo, valor in data.model_dump(exclude_unset=True).items():
            setattr(empresa, campo, valor)
        await self.db.commit()
        await self.db.refresh(empresa)
        return empresa

    async def eliminar(self, empresa_id: int) -> bool:
        empresa = await self.get_by_id(empresa_id)
        if not empresa:
            return False
        await self.db.delete(empresa)
        await self.db.commit()
        return True