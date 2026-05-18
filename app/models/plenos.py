from datetime import datetime, date
from sqlalchemy import BigInteger, Boolean, DateTime, Date, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Pleno(Base):
    __tablename__ = "plenos"

    id:          Mapped[int]      = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    titulo:      Mapped[str]      = mapped_column(String(500), nullable=False)
    descripcion: Mapped[str|None] = mapped_column(Text)
    fecha:       Mapped[date]     = mapped_column(Date, nullable=False)
    url_pdf:     Mapped[str|None] = mapped_column(Text)
    url_youtube: Mapped[str|None] = mapped_column(Text)
    activo:      Mapped[bool]     = mapped_column(Boolean, nullable=False, default=True)
    created_at:  Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())