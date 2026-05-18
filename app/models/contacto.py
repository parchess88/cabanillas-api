from datetime import datetime
from sqlalchemy import BigInteger, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Contacto(Base):
    __tablename__ = "contacto"

    id:         Mapped[int]      = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    clave:      Mapped[str]      = mapped_column(String(100), nullable=False, unique=True)
    valor:      Mapped[str]      = mapped_column(Text, nullable=False)
    etiqueta:   Mapped[str]      = mapped_column(String(200), nullable=False)
    icono:      Mapped[str]      = mapped_column(String(10), default='')
    orden:      Mapped[int]      = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())