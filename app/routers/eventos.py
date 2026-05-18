from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, extract

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.evento_imagen import Evento
from app.models.usuario import Usuario
from app.schemas.schemas import EventoCreate, EventoOut, EventoUpdate
from app.services.parse import parse_time
router = APIRouter(prefix="/eventos", tags=["Eventos"])


# ── GET /eventos/proximos ────────────────────────────────────
@router.get("/proximos", response_model=list[EventoOut])
async def get_proximos(
    limit: int = Query(6, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """Próximos eventos desde hoy"""

    result  = await db.execute(
        select(Evento)
        .where(Evento.fecha_inicio >= date.today())
        .order_by(Evento.fecha_inicio.asc())
        .limit(limit)
    )
    eventos = result.scalars().all()
    return [EventoOut.from_orm_evento(e) for e in eventos]


# ── GET /eventos ─────────────────────────────────────────────
@router.get("", response_model=list[EventoOut])
async def get_eventos(
    year:      int | None = Query(None),
    month:     int | None = Query(None),
    categoria: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Lista de eventos con filtros opcionales por mes y categoría"""

    query = select(Evento).order_by(Evento.fecha_inicio.asc())

    if year:      query = query.where(extract("year",  Evento.fecha_inicio) == year)
    if month:     query = query.where(extract("month", Evento.fecha_inicio) == month)
    if categoria: query = query.where(Evento.categoria == categoria)

    result  = await db.execute(query)
    eventos = result.scalars().all()
    return [EventoOut.from_orm_evento(e) for e in eventos]


# ── GET /eventos/{id} ────────────────────────────────────────
@router.get("/{evento_id}", response_model=EventoOut)
async def get_evento(evento_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Evento).where(Evento.id == evento_id))
    evento = result.scalar_one_or_none()
    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado")
    return EventoOut.from_orm_evento(evento)


# ── POST /eventos ────────────────────────────────────────────
@router.post("", response_model=EventoOut, status_code=status.HTTP_201_CREATED)
async def crear_evento(
    data: EventoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    # Usamos la función parse_time para normalizar horas
    hora_inicio = parse_time(data.horaInicio)
    hora_fin = parse_time(data.horaFin)

    evento = Evento(
        nombre=data.nombre,
        descripcion=data.descripcion,
        fecha_inicio=date.fromisoformat(data.fechaInicio),
        fecha_fin=date.fromisoformat(data.fechaFin) if data.fechaFin else None,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        ubicacion=data.ubicacion,
        categoria=data.categoria,
        aforo=data.aforo,
        imagen=data.imagen,
        usuario_id=current_user.id,
    )
    db.add(evento)
    await db.commit()
    await db.refresh(evento)
    return EventoOut.from_orm_evento(evento)


# ── PUT /eventos/{id} ────────────────────────────────────────
@router.put("/{evento_id}", response_model=EventoOut)
async def actualizar_evento(
    evento_id: int,
    data: EventoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    result = await db.execute(select(Evento).where(Evento.id == evento_id))
    evento = result.scalar_one_or_none()
    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado")

    campos = data.model_dump(exclude_unset=True)
    # Convertir fechas string a objetos date
    if "fechaInicio" in campos:
        evento.fecha_inicio = date.fromisoformat(campos.pop("fechaInicio"))
    if "fechaFin" in campos:
        evento.fecha_fin = date.fromisoformat(campos.pop("fechaFin")) if campos["fechaFin"] else None
        campos.pop("fechaFin", None)

    for campo, valor in campos.items():
        setattr(evento, campo, valor)

    await db.commit()
    await db.refresh(evento)
    return EventoOut.from_orm_evento(evento)


# ── DELETE /eventos/{id} ─────────────────────────────────────
@router.delete("/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_evento(
    evento_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    result = await db.execute(select(Evento).where(Evento.id == evento_id))
    evento = result.scalar_one_or_none()
    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado")
    await db.delete(evento)
    await db.commit()
