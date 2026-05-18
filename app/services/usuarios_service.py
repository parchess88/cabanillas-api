from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.usuario import Usuario
from app.schemas.schemas import UsuarioCreate, UsuarioUpdate
from app.core.security import hash_password


class UsuariosService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Usuario]:
        result = await self.db.execute(select(Usuario).order_by(Usuario.nombre))
        return result.scalars().all()

    async def get_by_id(self, usuario_id: int) -> Usuario | None:
        result = await self.db.execute(select(Usuario).where(Usuario.id == usuario_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Usuario | None:
        result = await self.db.execute(select(Usuario).where(Usuario.email == email))
        return result.scalar_one_or_none()

    async def crear(self, data: UsuarioCreate) -> Usuario:
        usuario = Usuario(
            nombre=data.nombre,
            apellidos=data.apellidos,
            email=data.email,
            password_hash=hash_password(data.password),
            rol=data.rol,
            departamento=data.departamento,
            activo=data.activo,
        )
        self.db.add(usuario)
        await self.db.commit()
        await self.db.refresh(usuario)
        return usuario

    async def actualizar(self, usuario_id: int, data: UsuarioUpdate) -> Usuario | None:
        usuario = await self.get_by_id(usuario_id)
        if not usuario:
            return None
        for campo, valor in data.model_dump(exclude_unset=True).items():
            setattr(usuario, campo, valor)
        await self.db.commit()
        await self.db.refresh(usuario)
        return usuario

    async def cambiar_password(self, usuario_id: int, nueva_password: str) -> bool:
        usuario = await self.get_by_id(usuario_id)
        if not usuario:
            return False
        usuario.password_hash = hash_password(nueva_password)
        await self.db.commit()
        return True

    async def eliminar(self, usuario_id: int) -> bool:
        usuario = await self.get_by_id(usuario_id)
        if not usuario:
            return False
        await self.db.delete(usuario)
        await self.db.commit()
        return True