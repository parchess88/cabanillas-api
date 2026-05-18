from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Directorio(Base):
    __tablename__ = "directorio"

    id:         Mapped[int]      = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    icono:      Mapped[str]      = mapped_column(String(10), nullable=False, default='🏛️')
    nombre:     Mapped[str]      = mapped_column(String(200), nullable=False)
    direccion:  Mapped[str]      = mapped_column(String(300), nullable=False)
    telefono:   Mapped[str|None] = mapped_column(String(50))
    extra:      Mapped[str|None] = mapped_column(Text)
    orden:      Mapped[int]      = mapped_column(Integer, nullable=False, default=0)
    activo:     Mapped[bool]     = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())