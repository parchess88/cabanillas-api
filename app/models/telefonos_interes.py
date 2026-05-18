from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class TelefonoInteres(Base):
    __tablename__ = "telefonos_interes"

    id:         Mapped[int]      = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    nombre:     Mapped[str]      = mapped_column(Text, nullable=False)
    localidad:  Mapped[str|None] = mapped_column(Text)
    telefono:   Mapped[str|None] = mapped_column(String(100))
    movil:      Mapped[str|None] = mapped_column(String(100))
    fax:        Mapped[str|None] = mapped_column(String(100))
    orden:      Mapped[int]      = mapped_column(Integer, nullable=False, default=0)
    activo:     Mapped[bool]     = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())