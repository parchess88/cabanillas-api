from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Empresa(Base):
    __tablename__ = "directorio_empresas"

    id:          Mapped[int]      = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    nombre:      Mapped[str]      = mapped_column(Text, nullable=False)
    categoria:   Mapped[str]      = mapped_column(String(100), nullable=False, default='general')
    descripcion: Mapped[str|None] = mapped_column(Text)
    telefono:    Mapped[str|None] = mapped_column(String(50))
    email:       Mapped[str|None] = mapped_column(String(200))
    web:         Mapped[str|None] = mapped_column(Text)
    direccion:   Mapped[str|None] = mapped_column(Text)
    logo_url:    Mapped[str|None] = mapped_column(Text)
    orden:       Mapped[int]      = mapped_column(Integer, nullable=False, default=0)
    activo:      Mapped[bool]     = mapped_column(Boolean, nullable=False, default=True)
    created_at:  Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())