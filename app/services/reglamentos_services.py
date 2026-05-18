from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app.models.reglamento import Reglamento
from app.schemas.schemas import ReglamentoCreate, ReglamentoUpdate


class ReglamentosService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(
        self,
        categoria: str | None = None,
        activa:    bool | None = None,
        search:    str | None = None,
        page:      int = 1,
        page_size: int = 50,
    ) -> tuple[list[Reglamento], int]:

        query = select(Reglamento).order_by(Reglamento.fecha_publicacion.desc())

        if categoria:          query = query.where(Reglamento.categoria == categoria)
        if activa is not None: query = query.where(Reglamento.activa == activa)
        if search:
            query = query.where(
                Reglamento.titulo.ilike(f"%{search}%") |
                Reglamento.descripcion.ilike(f"%{search}%")
            )

        count_q     = select(func.count()).select_from(query.subquery())
        total       = (await self.db.execute(count_q)).scalar_one()
        result      = await self.db.execute(query.offset((page - 1) * page_size).limit(page_size))
        reglamentos = result.scalars().all()

        return reglamentos, total

    async def get_by_id(self, reglamento_id: int) -> Reglamento | None:
        result = await self.db.execute(
            select(Reglamento).where(Reglamento.id == reglamento_id)
        )
        return result.scalar_one_or_none()

    async def crear(self, data: ReglamentoCreate) -> Reglamento:
        reglamento = Reglamento(
            titulo=data.titulo,
            descripcion=data.descripcion,
            categoria=data.categoria,
            url_pdf=data.url_pdf,
            fecha_publicacion=data.fechaPublicacion,
            activa=data.activa,
        )
        self.db.add(reglamento)
        await self.db.commit()
        await self.db.refresh(reglamento)
        return reglamento

    async def actualizar(self, reglamento_id: int, data: ReglamentoUpdate) -> Reglamento | None:
        reglamento = await self.get_by_id(reglamento_id)
        if not reglamento:
            return None

        campos = data.model_dump(exclude_unset=True)
        for campo, valor in campos.items():
            setattr(reglamento, campo, valor)

        await self.db.commit()
        await self.db.refresh(reglamento)
        return reglamento

    async def eliminar(self, reglamento_id: int) -> bool:
        reglamento = await self.get_by_id(reglamento_id)
        if not reglamento:
            return False

        await self.db.delete(reglamento)
        await self.db.commit()
        return True