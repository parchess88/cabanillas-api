from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import verify_password, hash_password, create_access_token, pwd_context
from app.models.usuario import Usuario
from app.schemas.schemas import LoginRequest, TokenResponse, UsuarioOut, UsuarioCreate

router = APIRouter(prefix="/auth", tags=["Autenticación"])


async def _do_login(email: str, password: str, db: AsyncSession):
    result = await db.execute(select(Usuario).where(Usuario.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
        )

    if pwd_context.needs_update(user.password_hash):
        user.password_hash = hash_password(password)
        await db.commit()

    if not user.activo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo")

    user.ultimo_acceso = datetime.now(timezone.utc)
    await db.commit()

    token = create_access_token({"sub": str(user.id), "rol": user.rol})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        usuario=UsuarioOut.model_validate(user)
    )


# ── Login JSON (Angular) ──────────────────────────────────────
@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await _do_login(credentials.email, credentials.password, db)


# ── Login Form (Swagger) ──────────────────────────────────────
@router.post("/token", response_model=TokenResponse)
async def login_swagger(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    return await _do_login(form.username, form.password, db)


# ── Registro ──────────────────────────────────────────────────
@router.post("/registro", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
async def registro(data: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).where(Usuario.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya está registrado")

    user = Usuario(
        nombre=data.nombre,
        apellidos=data.apellidos,
        email=data.email,
        password_hash=hash_password(data.password),
        rol=data.rol,
        departamento=data.departamento,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return UsuarioOut.model_validate(user)