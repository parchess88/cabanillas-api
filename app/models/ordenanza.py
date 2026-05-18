from datetime import datetime, date
from sqlalchemy import BigInteger, Boolean, DateTime, Date, String, Text, func , Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Ordenanza(Base):
    __tablename__ = "ordenanzas"

    id:                Mapped[int]       = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    titulo:            Mapped[str]       = mapped_column(String(500), nullable=False)
    descripcion:       Mapped[str|None]  = mapped_column(Text)
    categoria:         Mapped[str]       = mapped_column(String(100), nullable=False, default="general")
    url_pdf:           Mapped[str]       = mapped_column(Text, nullable=False)
    fecha_publicacion: Mapped[date]      = mapped_column(Date, nullable=False, server_default=func.now())
    activa:            Mapped[bool]      = mapped_column(Boolean, nullable=False, default=True)
    created_at:        Mapped[datetime]  = mapped_column(DateTime(timezone=True), server_default=func.now())
    orden_categoria: Mapped[int] = mapped_column(Integer, nullable=False, default=0)