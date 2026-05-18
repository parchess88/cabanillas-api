from sqlalchemy import Column, Integer, String, Boolean, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class LayoutTipo(str, enum.Enum):
    TARJETA = "TARJETA"
    LISTA = "LISTA"


class ServicioMunicipal(Base):
    __tablename__ = "servicios_municipales"

    id          = Column(Integer, primary_key=True, index=True)
    nombre      = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    direccion   = Column(String(300), nullable=True)
    maps_url    = Column(String(500), nullable=True)
    maps_embed  = Column(String(500), nullable=True)
    foto_url    = Column(String(500), nullable=True)
    layout = Column(
        Enum(LayoutTipo, name="layout_tipo"),
        default=LayoutTipo.TARJETA,
        nullable=False
    )
    activo      = Column(Boolean, default=True)
    orden       = Column(Integer, default=0)

    items = relationship(
        "ServicioItem",
        back_populates="servicio",
        cascade="all, delete-orphan",
        order_by="ServicioItem.orden"
    )


class ServicioItem(Base):
    __tablename__ = "servicios_items"

    id          = Column(Integer, primary_key=True, index=True)
    servicio_id = Column(Integer, ForeignKey("servicios_municipales.id", ondelete="CASCADE"), nullable=False)  # ← esto faltaba
    titulo      = Column(String(200), nullable=False)
    contenido   = Column(Text, nullable=True)
    orden       = Column(Integer, default=0)

    servicio = relationship("ServicioMunicipal", back_populates="items")