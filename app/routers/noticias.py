from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, update

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.noticia import Noticia, NoticiaEtiqueta
from app.models.usuario import Usuario
from app.schemas.schemas import (
    NoticiaCreate, NoticiaOut, NoticiaUpdate, NoticiasListResponse
)

router = APIRouter(prefix="/noticias", tags=["Noticias"])


# ── GET /noticias ────────────────────────────────────────────
@router.get("", response_model=NoticiasListResponse)
async def get_noticias(
    estado:    str | None = Query(None),
    categoria: str | None = Query(None),
    search:    str | None = Query(None),
    page:      int        = Query(1, ge=1),
    pageSize:  int        = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Lista de noticias con filtros y paginación"""

    query = select(Noticia).order_by(Noticia.fecha_publicacion.desc())

    if estado:    query = query.where(Noticia.estado == estado)
    if categoria: query = query.where(Noticia.categoria == categoria)
    if search:
        query = query.where(
            Noticia.titulo.ilike(f"%{search}%") |
            Noticia.resumen.ilike(f"%{search}%")
        )

    # Total para paginación
    count_q  = select(func.count()).select_from(query.subquery())
    total    = (await db.execute(count_q)).scalar_one()

    # Página actual
    result   = await db.execute(query.offset((page - 1) * pageSize).limit(pageSize))
    noticias = result.scalars().all()

    # Cargar etiquetas
    for n in noticias:
        await db.refresh(n, ["etiquetas"])

    return NoticiasListResponse(
        data=[NoticiaOut.from_orm_noticia(n) for n in noticias],
        total=total,
        page=page,
        pageSize=pageSize,
    )


# ── GET /noticias/destacada ──────────────────────────────────
@router.get("/destacada", response_model=NoticiaOut)
async def get_destacada(db: AsyncSession = Depends(get_db)):
    """Noticia marcada como destacada para la portada"""

    result  = await db.execute(
        select(Noticia)
        .where(Noticia.destacada == True, Noticia.estado == "publicada")
        .order_by(Noticia.fecha_publicacion.desc())
        .limit(1)
    )
    noticia = result.scalar_one_or_none()

    if not noticia:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay noticia destacada")

    await db.refresh(noticia, ["etiquetas"])
    return NoticiaOut.from_orm_noticia(noticia)


# ── GET /noticias/ultimas ────────────────────────────────────
@router.get("/ultimas", response_model=list[NoticiaOut])
async def get_ultimas(
    limit: int = Query(3, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    """Últimas noticias publicadas para la portada"""

    result   = await db.execute(
        select(Noticia)
        .where(Noticia.estado == "publicada")
        .order_by(Noticia.fecha_publicacion.desc())
        .limit(limit)
    )
    noticias = result.scalars().all()

    for n in noticias:
        await db.refresh(n, ["etiquetas"])

    return [NoticiaOut.from_orm_noticia(n) for n in noticias]


# ── GET /noticias/{id} ───────────────────────────────────────
@router.get("/{noticia_id}", response_model=NoticiaOut)
async def get_noticia(noticia_id: int, db: AsyncSession = Depends(get_db)):
    """Detalle de una noticia por ID"""

    result  = await db.execute(select(Noticia).where(Noticia.id == noticia_id))
    noticia = result.scalar_one_or_none()

    if not noticia:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Noticia no encontrada")

    await db.refresh(noticia, ["etiquetas"])
    return NoticiaOut.from_orm_noticia(noticia)


# ── POST /noticias ───────────────────────────────────────────
@router.post("", response_model=NoticiaOut, status_code=status.HTTP_201_CREATED)
async def crear_noticia(
    data: NoticiaCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Crear nueva noticia — requiere autenticación"""

    noticia = Noticia(
        titulo=data.titulo,
        resumen=data.resumen,
        contenido=data.contenido,
        categoria=data.categoria,
        estado=data.estado,
        imagen=data.imagen,
        autor=data.autor or f"{current_user.nombre} {current_user.apellidos}",
        fecha_publicacion=data.fechaPublicacion or datetime.now(timezone.utc),
        destacada=data.destacada,
        usuario_id=current_user.id,
    )
    db.add(noticia)
    await db.flush()  # Para obtener el ID antes del commit

    # Guardar etiquetas
    for tag in data.etiquetas:
        db.add(NoticiaEtiqueta(noticia_id=noticia.id, etiqueta=tag))

    await db.commit()
    await db.refresh(noticia, ["etiquetas"])
    return NoticiaOut.from_orm_noticia(noticia)


# ── PUT /noticias/{id} ───────────────────────────────────────
@router.put("/{noticia_id}", response_model=NoticiaOut)
async def actualizar_noticia(
    noticia_id: int,
    data: NoticiaUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Actualizar noticia — requiere autenticación"""

    result  = await db.execute(select(Noticia).where(Noticia.id == noticia_id))
    noticia = result.scalar_one_or_none()

    if not noticia:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Noticia no encontrada")

    # Actualizar solo los campos enviados
    campos = data.model_dump(exclude_unset=True, exclude={"etiquetas"})
    for campo, valor in campos.items():
        setattr(noticia, campo, valor)

    # Actualizar etiquetas si se enviaron
    if data.etiquetas is not None:
        await db.execute(
            NoticiaEtiqueta.__table__.delete().where(NoticiaEtiqueta.noticia_id == noticia_id)
        )
        for tag in data.etiquetas:
            db.add(NoticiaEtiqueta(noticia_id=noticia_id, etiqueta=tag))

    await db.commit()
    await db.refresh(noticia, ["etiquetas"])
    return NoticiaOut.from_orm_noticia(noticia)


# ── PATCH /noticias/{id}/publicar ───────────────────────────
@router.patch("/{noticia_id}/publicar", response_model=NoticiaOut)
async def publicar_noticia(
    noticia_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Publicar una noticia directamente"""

    result  = await db.execute(select(Noticia).where(Noticia.id == noticia_id))
    noticia = result.scalar_one_or_none()

    if not noticia:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Noticia no encontrada")

    noticia.estado            = "publicada"
    noticia.fecha_publicacion = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(noticia, ["etiquetas"])
    return NoticiaOut.from_orm_noticia(noticia)


# ── DELETE /noticias/{id} ────────────────────────────────────
@router.delete("/{noticia_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_noticia(
    noticia_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Eliminar noticia — requiere autenticación"""

    result  = await db.execute(select(Noticia).where(Noticia.id == noticia_id))
    noticia = result.scalar_one_or_none()

    if not noticia:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Noticia no encontrada")

    await db.delete(noticia)
    await db.commit()
