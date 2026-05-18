from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class PoliticaPrivacidad(Base):
    __tablename__ = "politica_privacidad"

    id:          Mapped[int]      = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    titulo:      Mapped[str]      = mapped_column(String(300), nullable=False)
    descripcion: Mapped[str|None] = mapped_column(Text)
    url_pdf:     Mapped[str]      = mapped_column(Text, nullable=False)
    orden:       Mapped[int]      = mapped_column(Integer, nullable=False, default=0)
    activo:      Mapped[bool]     = mapped_column(Boolean, nullable=False, default=True)
    created_at:  Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())