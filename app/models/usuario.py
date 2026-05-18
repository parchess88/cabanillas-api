from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id:            Mapped[int]      = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    nombre:        Mapped[str]      = mapped_column(String(100), nullable=False)
    apellidos:     Mapped[str]      = mapped_column(String(200), nullable=False)
    email:         Mapped[str]      = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str]      = mapped_column(Text, nullable=False)
    rol:           Mapped[str]      = mapped_column(String(20), nullable=False, default="editor")
    departamento:  Mapped[str|None] = mapped_column(String(100))
    activo:        Mapped[bool]     = mapped_column(Boolean, nullable=False, default=True)
    ultimo_acceso: Mapped[datetime|None] = mapped_column(DateTime(timezone=True))
    created_at:    Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:    Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    noticias: Mapped[list["Noticia"]] = relationship(back_populates="usuario")
    eventos:  Mapped[list["Evento"]]  = relationship(back_populates="usuario")
    imagenes: Mapped[list["Imagen"]]  = relationship(back_populates="usuario")
