from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Presupuesto(Base):
    __tablename__ = "presupuestos"

    id:          Mapped[int]      = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    titulo:      Mapped[str]      = mapped_column(String(500), nullable=False)
    descripcion: Mapped[str|None] = mapped_column(Text)
    anio:        Mapped[int]      = mapped_column(Integer, nullable=False)
    url_pdf:     Mapped[str]      = mapped_column(Text, nullable=False)
    activo:      Mapped[bool]     = mapped_column(Boolean, nullable=False, default=True)
    created_at:  Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())