from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Partido(Base):
    __tablename__ = "partidos"

    id:         Mapped[int]      = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    nombre:     Mapped[str]      = mapped_column(String(200), nullable=False)
    logo_url:   Mapped[str|None] = mapped_column(Text)
    color:      Mapped[str]      = mapped_column(String(20), nullable=False, default='#163969')
    orden:      Mapped[int]      = mapped_column(Integer, nullable=False, default=0)
    activo:     Mapped[bool]     = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    miembros: Mapped[list["MiembroCorporacion"]] = relationship("MiembroCorporacion", back_populates="partido", cascade="all, delete")


class MiembroCorporacion(Base):
    __tablename__ = "miembros_corporacion"

    id:          Mapped[int]      = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    partido_id:  Mapped[int]      = mapped_column(BigInteger, ForeignKey("partidos.id", ondelete="CASCADE"), nullable=False)
    nombre:      Mapped[str]      = mapped_column(String(200), nullable=False)
    cargo:       Mapped[str]      = mapped_column(String(100), nullable=False, default='Concejal')
    foto_url:    Mapped[str|None] = mapped_column(Text)
    descripcion: Mapped[str|None] = mapped_column(Text)
    orden:       Mapped[int]      = mapped_column(Integer, nullable=False, default=0)
    activo:      Mapped[bool]     = mapped_column(Boolean, nullable=False, default=True)
    created_at:  Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    partido: Mapped["Partido"] = relationship("Partido", back_populates="miembros")