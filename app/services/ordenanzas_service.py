from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app.models.ordenanza import Ordenanza
from app.schemas.schemas import OrdenanzaCreate, OrdenanzaUpdate


class OrdenanzasService:

    def __init__(self, db: AsyncSession):
        self.db = db

    # ── Listar ───────────────────────────────────────────────
    async def get_all(
        self,
        categoria: str | None = None,
        activa:    bool | None = None,
        search:    str | None = None,
        page:      int = 1,
        page_size: int = 50,
    ) -> tuple[list[Ordenanza], int]:

        query = select(Ordenanza).order_by(Ordenanza.fecha_publicacion.desc())

        if categoria:       query = query.where(Ordenanza.categoria == categoria)
        if activa is not None: query = query.where(Ordenanza.activa == activa)
        if search:
            query = query.where(
                Ordenanza.titulo.ilike(f"%{search}%") |
                Ordenanza.descripcion.ilike(f"%{search}%")
            )

        count_q    = select(func.count()).select_from(query.subquery())
        total      = (await self.db.execute(count_q)).scalar_one()
        result     = await self.db.execute(query.offset((page - 1) * page_size).limit(page_size))
        ordenanzas = result.scalars().all()

        return ordenanzas, total

    # ── Obtener por ID ───────────────────────────────────────
    async def get_by_id(self, ordenanza_id: int) -> Ordenanza | None:
        result = await self.db.execute(
            select(Ordenanza).where(Ordenanza.id == ordenanza_id)
        )
        return result.scalar_one_or_none()

    # ── Crear ────────────────────────────────────────────────
    async def crear(self, data: OrdenanzaCreate) -> Ordenanza:
        ordenanza = Ordenanza(
            titulo=data.titulo,
            descripcion=data.descripcion,
            categoria=data.categoria,
            url_pdf=data.url_pdf,
            fecha_publicacion=data.fechaPublicacion,
            activa=data.activa,
            orden_categoria=data.orden_categoria,

        )
        self.db.add(ordenanza)
        await self.db.commit()
        await self.db.refresh(ordenanza)
        return ordenanza

    # ── Actualizar ───────────────────────────────────────────
    async def actualizar(self, ordenanza_id: int, data: OrdenanzaUpdate) -> Ordenanza | None:
        ordenanza = await self.get_by_id(ordenanza_id)
        if not ordenanza:
            return None

        campos = data.model_dump(exclude_unset=True)
        for campo, valor in campos.items():
            setattr(ordenanza, campo, valor)

        await self.db.commit()
        await self.db.refresh(ordenanza)
        return ordenanza

    # ── Eliminar ─────────────────────────────────────────────
    async def eliminar(self, ordenanza_id: int) -> bool:
        ordenanza = await self.get_by_id(ordenanza_id)
        if not ordenanza:
            return False

        await self.db.delete(ordenanza)
        await self.db.commit()
        return True