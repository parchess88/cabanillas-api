from datetime import date, datetime, time
from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, Integer, String, Text, Time, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Evento(Base):
    __tablename__ = "eventos"

    id:          Mapped[int]      = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    nombre:      Mapped[str]      = mapped_column(String(300), nullable=False)
    descripcion: Mapped[str|None] = mapped_column(Text)
    fecha_inicio: Mapped[date]    = mapped_column(Date, nullable=False)
    fecha_fin:   Mapped[date|None] = mapped_column(Date)
    hora_inicio: Mapped[time|None] = mapped_column(Time)
    hora_fin:    Mapped[time|None] = mapped_column(Time)
    ubicacion:   Mapped[str|None] = mapped_column(String(300))
    categoria:   Mapped[str]      = mapped_column(String(50), nullable=False)
    aforo:       Mapped[int|None] = mapped_column(Integer)
    imagen:      Mapped[str|None] = mapped_column(Text)
    usuario_id:  Mapped[int|None] = mapped_column(BigInteger, ForeignKey("usuarios.id", ondelete="SET NULL"))
    created_at:  Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:  Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    usuario: Mapped["Usuario"] = relationship(back_populates="eventos")


class Imagen(Base):
    __tablename__ = "imagenes"

    id:           Mapped[int]      = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    titulo:       Mapped[str]      = mapped_column(String(300), nullable=False)
    url:          Mapped[str]      = mapped_column(Text, nullable=False)
    album:        Mapped[str]      = mapped_column(String(100), nullable=False, default="general")
    fecha_subida: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    autor:        Mapped[str|None] = mapped_column(String(200))
    usuario_id:   Mapped[int|None] = mapped_column(BigInteger, ForeignKey("usuarios.id", ondelete="SET NULL"))
    created_at:   Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    usuario: Mapped["Usuario"] = relationship(back_populates="imagenes")
