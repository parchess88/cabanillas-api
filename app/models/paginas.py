from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Pagina(Base):
    __tablename__ = "paginas"

    id:          Mapped[int]      = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    titulo:      Mapped[str]      = mapped_column(String(300), nullable=False)
    slug:        Mapped[str]      = mapped_column(String(300), nullable=False, unique=True)
    contenido:   Mapped[str|None] = mapped_column(Text)
    descripcion: Mapped[str|None] = mapped_column(Text)
    activa:      Mapped[bool]     = mapped_column(Boolean, nullable=False, default=True)
    created_at:  Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:  Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())