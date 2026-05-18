from datetime import datetime, date
from enum import Enum
from typing import Literal, Optional, List
from pydantic import BaseModel, EmailStr, Field


# ── Auth ────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: EmailStr
    password: str





# ── Usuario ─────────────────────────────────────────────────

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    apellidos: str
    email: str
    rol: Literal["admin", "editor"]
    departamento: str | None
    activo: bool
    ultimo_acceso: datetime | None

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioOut

class UsuarioCreate(BaseModel):
    nombre: str
    apellidos: str
    email: EmailStr
    password: str
    rol: Literal["admin", "editor"] = "editor"
    departamento: str | None = None


class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    apellidos: str | None = None
    rol: Literal["admin", "editor"] | None = None
    departamento: str | None = None
    activo: bool | None = None


# ── Noticia ─────────────────────────────────────────────────

CategoriaNoticia = Literal[
    "urbanismo",
    "cultura",
    "economia",
    "servicios",
    "medioambiente",
    "igualdad",
    "juventud",
    "salud",
    "tablon",
]
EstadoNoticia    = Literal["borrador", "revision", "publicada"]


class NoticiaOut(BaseModel):
    id: int
    titulo: str
    resumen: str | None
    contenido: str
    categoria: CategoriaNoticia
    estado: EstadoNoticia
    imagen: str | None
    autor: str
    fechaPublicacion: datetime
    destacada: bool
    etiquetas: list[str] = []

    model_config = {"from_attributes": True, "populate_by_name": True}

    @classmethod
    def from_orm_noticia(cls, obj):
        return cls(
            id=obj.id,
            titulo=obj.titulo,
            resumen=obj.resumen,
            contenido=obj.contenido,
            categoria=obj.categoria,
            estado=obj.estado,
            imagen=obj.imagen,
            autor=obj.autor,
            fechaPublicacion=obj.fecha_publicacion,
            destacada=obj.destacada,
            etiquetas=[e.etiqueta for e in obj.etiquetas],
        )


class NoticiaCreate(BaseModel):
    titulo: str
    resumen: str | None = None
    contenido: str
    categoria: CategoriaNoticia
    estado: EstadoNoticia = "borrador"
    imagen: str | None = None
    autor: Optional[str] = None
    fechaPublicacion: datetime | None = None
    destacada: bool = False
    etiquetas: list[str] = []


class NoticiaUpdate(BaseModel):
    titulo: str | None = None
    resumen: str | None = None
    contenido: str | None = None
    categoria: CategoriaNoticia | None = None
    estado: EstadoNoticia | None = None
    imagen: str | None = None
    autor: str | None = None
    destacada: bool | None = None
    etiquetas: list[str] | None = None


class NoticiasListResponse(BaseModel):
    data: list[NoticiaOut]
    total: int
    page: int
    pageSize: int


# ── Evento ──────────────────────────────────────────────────

CategoriaEvento = Literal["plenos", "mercados", "medioambiente", "cultura"]


class EventoOut(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    fechaInicio: str
    fechaFin: str | None
    horaInicio: str | None
    horaFin: str | None
    ubicacion: str | None
    categoria: CategoriaEvento
    aforo: int | None
    imagen: str | None

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_evento(cls, obj):
        return cls(
            id=obj.id,
            nombre=obj.nombre,
            descripcion=obj.descripcion,
            fechaInicio=str(obj.fecha_inicio),
            fechaFin=str(obj.fecha_fin) if obj.fecha_fin else None,
            horaInicio=str(obj.hora_inicio) if obj.hora_inicio else None,
            horaFin=str(obj.hora_fin) if obj.hora_fin else None,
            ubicacion=obj.ubicacion,
            categoria=obj.categoria,
            aforo=obj.aforo,
            imagen=obj.imagen,
        )


class EventoCreate(BaseModel):
    nombre: str
    descripcion: str | None = None
    fechaInicio: str
    fechaFin: str | None = None
    horaInicio: str | None = None
    horaFin: str | None = None
    ubicacion: str | None = None
    categoria: CategoriaEvento
    aforo: int | None = None
    imagen: str | None = None


class EventoUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    fechaInicio: str | None = None
    fechaFin: str | None = None
    horaInicio: str | None = None
    horaFin: str | None = None
    ubicacion: str | None = None
    categoria: CategoriaEvento | None = None
    aforo: int | None = None
    imagen: str | None = None


# ── Imagen ──────────────────────────────────────────────────

class ImagenOut(BaseModel):
    id: int
    titulo: str
    url: str
    album: str
    fechaSubida: datetime
    autor: str | None

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_imagen(cls, obj):
        return cls(
            id=obj.id,
            titulo=obj.titulo,
            url=obj.url,
            album=obj.album,
            fechaSubida=obj.fecha_subida,
            autor=obj.autor,
        )


# ── Ordenanza ────────────────────────────────────────────────

class OrdenanzaOut(BaseModel):
    id: int
    titulo: str
    descripcion: str | None
    categoria: str
    url_pdf: str
    fechaPublicacion: date
    activa: bool
    orden_categoria: int = 0

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_ordenanza(cls, obj):
        return cls(
            id=obj.id,
            titulo=obj.titulo,
            descripcion=obj.descripcion,
            categoria=obj.categoria,
            url_pdf=obj.url_pdf,
            fechaPublicacion=obj.fecha_publicacion,
            activa=obj.activa,
            orden_categoria=obj.orden_categoria,
        )


class OrdenanzaCreate(BaseModel):
    titulo: str
    descripcion: str | None = None
    categoria: str = 'general'
    url_pdf: str
    fechaPublicacion: date = Field(default_factory=date.today)
    activa: bool = True
    orden_categoria: int = 0


class OrdenanzaUpdate(BaseModel):
    titulo: str | None = None
    descripcion: str | None = None
    categoria: str | None = None
    url_pdf: str | None = None
    fechaPublicacion: date | None = None
    activa: bool | None = None
    orden_categoria: int | None = None

class OrdenanzasListResponse(BaseModel):
    data: list[OrdenanzaOut]
    total: int
    page: int
    pageSize: int


# ── Reglamento ───────────────────────────────────────────────

class ReglamentoOut(BaseModel):
    id: int
    titulo: str
    descripcion: str | None
    categoria: str
    url_pdf: str
    fechaPublicacion: date
    activa: bool

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_reglamento(cls, obj):
        return cls(
            id=obj.id,
            titulo=obj.titulo,
            descripcion=obj.descripcion,
            categoria=obj.categoria,
            url_pdf=obj.url_pdf,
            fechaPublicacion=obj.fecha_publicacion,
            activa=obj.activa,
        )


class ReglamentoCreate(BaseModel):
    titulo: str
    descripcion: str | None = None
    categoria: str = "general"
    url_pdf: str
    fechaPublicacion: date | None = None
    activa: bool = True


class ReglamentoUpdate(BaseModel):
    titulo: str | None = None
    descripcion: str | None = None
    categoria: str | None = None
    url_pdf: str | None = None
    fechaPublicacion: date | None = None
    activa: bool | None = None


class ReglamentosListResponse(BaseModel):
    data: list[ReglamentoOut]
    total: int
    page: int
    pageSize: int


# ── Presupuesto ──────────────────────────────────────────────

class PresupuestoOut(BaseModel):
    id: int
    titulo: str
    descripcion: str | None
    anio: int
    url_pdf: str
    activo: bool

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_presupuesto(cls, obj):
        return cls(
            id=obj.id,
            titulo=obj.titulo,
            descripcion=obj.descripcion,
            anio=obj.anio,
            url_pdf=obj.url_pdf,
            activo=obj.activo,
        )


class PresupuestoCreate(BaseModel):
    titulo: str
    descripcion: str | None = None
    anio: int
    url_pdf: str
    activo: bool = True


class PresupuestoUpdate(BaseModel):
    titulo: str | None = None
    descripcion: str | None = None
    anio: int | None = None
    url_pdf: str | None = None
    activo: bool | None = None


class PresupuestosListResponse(BaseModel):
    data: list[PresupuestoOut]
    total: int
    page: int
    pageSize: int



# ── Pleno ────────────────────────────────────────────────────

class PlenoOut(BaseModel):
    id: int
    titulo: str
    descripcion: str | None
    fecha: date
    url_pdf: str | None
    url_youtube: str | None
    activo: bool

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_pleno(cls, obj):
        return cls(
            id=obj.id,
            titulo=obj.titulo,
            descripcion=obj.descripcion,
            fecha=obj.fecha,
            url_pdf=obj.url_pdf,
            url_youtube=obj.url_youtube,
            activo=obj.activo,
        )


class PlenoCreate(BaseModel):
    titulo: str
    descripcion: str | None = None
    fecha: date
    url_pdf: str | None = None
    url_youtube: str | None = None
    activo: bool = True


class PlenoUpdate(BaseModel):
    titulo: str | None = None
    descripcion: str | None = None
    fecha: date | None = None
    url_pdf: str | None = None
    url_youtube: str | None = None
    activo: bool | None = None


class PlenosListResponse(BaseModel):
    data: list[PlenoOut]
    total: int
    page: int
    pageSize: int


# ── Corporación ──────────────────────────────────────────────

class MiembroOut(BaseModel):
    id: int
    partido_id: int
    nombre: str
    cargo: str
    foto_url: str | None
    descripcion: str | None
    orden: int
    activo: bool

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_miembro(cls, obj):
        return cls(
            id=obj.id,
            partido_id=obj.partido_id,
            nombre=obj.nombre,
            cargo=obj.cargo,
            foto_url=obj.foto_url,
            descripcion=obj.descripcion,
            orden=obj.orden,
            activo=obj.activo,
        )


class MiembroCreate(BaseModel):
    partido_id: int
    nombre: str
    cargo: str = 'Concejal'
    foto_url: str | None = None
    descripcion: str | None = None
    orden: int = 0
    activo: bool = True


class MiembroUpdate(BaseModel):
    nombre: str | None = None
    cargo: str | None = None
    foto_url: str | None = None
    descripcion: str | None = None
    orden: int | None = None
    activo: bool | None = None


class PartidoOut(BaseModel):
    id: int
    nombre: str
    logo_url: str | None
    color: str
    orden: int
    activo: bool
    miembros: list[MiembroOut] = []

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_partido(cls, obj):
        return cls(
            id=obj.id,
            nombre=obj.nombre,
            logo_url=obj.logo_url,
            color=obj.color,
            orden=obj.orden,
            activo=obj.activo,
            miembros=[MiembroOut.from_orm_miembro(m) for m in sorted(obj.miembros, key=lambda m: m.orden)],
        )


class PartidoCreate(BaseModel):
    nombre: str
    logo_url: str | None = None
    color: str = '#163969'
    orden: int = 0
    activo: bool = True


class PartidoUpdate(BaseModel):
    nombre: str | None = None
    logo_url: str | None = None
    color: str | None = None
    orden: int | None = None
    activo: bool | None = None


class PartidosListResponse(BaseModel):
    data: list[PartidoOut]
    total: int



# ── Directorio ───────────────────────────────────────────────

class DirectorioOut(BaseModel):
    id: int
    icono: str
    nombre: str
    direccion: str
    telefono: str | None
    extra: str | None
    orden: int
    activo: bool

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_directorio(cls, obj):
        return cls(
            id=obj.id, icono=obj.icono, nombre=obj.nombre,
            direccion=obj.direccion, telefono=obj.telefono,
            extra=obj.extra, orden=obj.orden, activo=obj.activo,
        )


class DirectorioCreate(BaseModel):
    icono: str = '🏛️'
    nombre: str
    direccion: str
    telefono: str | None = None
    extra: str | None = None
    orden: int = 0
    activo: bool = True


class DirectorioUpdate(BaseModel):
    icono: str | None = None
    nombre: str | None = None
    direccion: str | None = None
    telefono: str | None = None
    extra: str | None = None
    orden: int | None = None
    activo: bool | None = None


class DirectorioListResponse(BaseModel):
    data: list[DirectorioOut]
    total: int


# ── Contacto ─────────────────────────────────────────────────

class ContactoOut(BaseModel):
    id: int
    clave: str
    valor: str
    etiqueta: str
    icono: str
    orden: int

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_contacto(cls, obj):
        return cls(
            id=obj.id, clave=obj.clave, valor=obj.valor,
            etiqueta=obj.etiqueta, icono=obj.icono, orden=obj.orden,
        )


class ContactoUpdate(BaseModel):
    valor: str
    etiqueta: str | None = None
    icono: str | None = None
    orden: int | None = None


class ContactoListResponse(BaseModel):
    data: list[ContactoOut]
    total: int

# ── Páginas ──────────────────────────────────────────────────

class PaginaOut(BaseModel):
    id: int
    titulo: str
    slug: str
    contenido: str | None
    descripcion: str | None
    activa: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_pagina(cls, obj):
        return cls(
            id=obj.id, titulo=obj.titulo, slug=obj.slug,
            contenido=obj.contenido, descripcion=obj.descripcion,
            activa=obj.activa, created_at=obj.created_at, updated_at=obj.updated_at,
        )


class PaginaCreate(BaseModel):
    titulo: str
    slug: str
    contenido: str | None = None
    descripcion: str | None = None
    activa: bool = True


class PaginaUpdate(BaseModel):
    titulo: str | None = None
    slug: str | None = None
    contenido: str | None = None
    descripcion: str | None = None
    activa: bool | None = None


class PaginasListResponse(BaseModel):
    data: list[PaginaOut]
    total: int


class LayoutTipo(str, Enum):
    TARJETA = "tarjeta"
    LISTA = "lista"


# ── Servicio Municipal ───────────────────────────────────────

class LayoutTipo(str, Enum):
    TARJETA = "TARJETA"
    LISTA = "LISTA"


class ServicioItemOut(BaseModel):
    id: int
    servicio_id: int
    titulo: str
    contenido: str | None
    orden: int

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_item(cls, obj):
        return cls(
            id=obj.id,
            servicio_id=obj.servicio_id,
            titulo=obj.titulo,
            contenido=obj.contenido,
            orden=obj.orden,
        )


class ServicioItemCreate(BaseModel):
    titulo: str
    contenido: str | None = None
    orden: int = 0


class ServicioItemUpdate(BaseModel):
    titulo: str | None = None
    contenido: str | None = None
    orden: int | None = None


class ServicioMunicipalOut(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    direccion: str | None
    maps_url: str | None
    maps_embed: str | None
    foto_url: str | None
    layout: LayoutTipo
    activo: bool
    orden: int
    items: list[ServicioItemOut] = []

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_servicio(cls, obj):
        return cls(
            id=obj.id,
            nombre=obj.nombre,
            descripcion=obj.descripcion,
            direccion=obj.direccion,
            maps_url=obj.maps_url,
            maps_embed=obj.maps_embed,
            foto_url=obj.foto_url,
            layout=obj.layout,
            activo=obj.activo,
            orden=obj.orden,
            items=[ServicioItemOut.from_orm_item(i) for i in sorted(obj.items, key=lambda i: i.orden)],
        )


class ServicioMunicipalCreate(BaseModel):
    nombre: str
    descripcion: str | None = None
    direccion: str | None = None
    maps_url: str | None = None
    maps_embed: str | None = None
    foto_url: str | None = None
    layout: LayoutTipo = LayoutTipo.TARJETA
    activo: bool = True
    orden: int = 0
    items: list[ServicioItemCreate] = []


class ServicioMunicipalUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    direccion: str | None = None
    maps_url: str | None = None
    maps_embed: str | None = None
    foto_url: str | None = None
    layout: LayoutTipo | None = None
    activo: bool | None = None
    orden: int | None = None
    items: list[ServicioItemCreate] | None = None


class ServiciosListResponse(BaseModel):
    data: list[ServicioMunicipalOut]
    total: int




# ── Teléfonos de interés ─────────────────────────────────────

class TelefonoInteresOut(BaseModel):
    id: int
    nombre: str
    localidad: str | None
    telefono: str | None
    movil: str | None
    fax: str | None
    orden: int
    activo: bool

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_telefono(cls, obj):
        return cls(
            id=obj.id, nombre=obj.nombre, localidad=obj.localidad,
            telefono=obj.telefono, movil=obj.movil, fax=obj.fax,
            orden=obj.orden, activo=obj.activo,
        )


class TelefonoInteresCreate(BaseModel):
    nombre: str
    localidad: str | None = None
    telefono: str | None = None
    movil: str | None = None
    fax: str | None = None
    orden: int = 0
    activo: bool = True


class TelefonoInteresUpdate(BaseModel):
    nombre: str | None = None
    localidad: str | None = None
    telefono: str | None = None
    movil: str | None = None
    fax: str | None = None
    orden: int | None = None
    activo: bool | None = None


class TelefonosListResponse(BaseModel):
    data: list[TelefonoInteresOut]
    total: int



# ── Política de Privacidad ───────────────────────────────────

class PoliticaPrivacidadOut(BaseModel):
    id: int
    titulo: str
    descripcion: str | None
    url_pdf: str
    orden: int
    activo: bool

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_politica(cls, obj):
        return cls(
            id=obj.id, titulo=obj.titulo, descripcion=obj.descripcion,
            url_pdf=obj.url_pdf, orden=obj.orden, activo=obj.activo,
        )


class PoliticaPrivacidadCreate(BaseModel):
    titulo: str
    descripcion: str | None = None
    url_pdf: str
    orden: int = 0
    activo: bool = True


class PoliticaPrivacidadUpdate(BaseModel):
    titulo: str | None = None
    descripcion: str | None = None
    url_pdf: str | None = None
    orden: int | None = None
    activo: bool | None = None


class PoliticaListResponse(BaseModel):
    data: list[PoliticaPrivacidadOut]
    total: int


