from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Noticia(Base):
    __tablename__ = "noticias"

    id:                Mapped[int]      = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    titulo:            Mapped[str]      = mapped_column(String(500), nullable=False)
    resumen:           Mapped[str|None] = mapped_column(Text)
    contenido:         Mapped[str]      = mapped_column(Text, nullable=False)
    categoria:         Mapped[str]      = mapped_column(String(50), nullable=False)
    estado:            Mapped[str]      = mapped_column(String(20), nullable=False, default="borrador")
    imagen:            Mapped[str|None] = mapped_column(Text)
    autor:             Mapped[str]      = mapped_column(String(200), nullable=False)
    fecha_publicacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    destacada:         Mapped[bool]     = mapped_column(Boolean, nullable=False, default=False)
    usuario_id:        Mapped[int|None] = mapped_column(BigInteger, ForeignKey("usuarios.id", ondelete="SET NULL"))
    created_at:        Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:        Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    usuario:   Mapped["Usuario"]          = relationship(back_populates="noticias")
    etiquetas: Mapped[list["NoticiaEtiqueta"]] = relationship(back_populates="noticia", cascade="all, delete-orphan")


class NoticiaEtiqueta(Base):
    __tablename__ = "noticia_etiquetas"

    id:         Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    noticia_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("noticias.id", ondelete="CASCADE"), nullable=False)
    etiqueta:   Mapped[str] = mapped_column(String(100), nullable=False)

    noticia: Mapped["Noticia"] = relationship(back_populates="etiquetas")
