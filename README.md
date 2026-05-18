# Cabanillas de la Sierra — API Backend

API REST con **FastAPI 0.131** + **Python 3.13** conectada a **Supabase (PostgreSQL)**.

---

## Estructura del proyecto

```
cabanillas-api/
├── main.py                  ← Punto de entrada
├── requirements.txt         ← Dependencias
├── .env.example             ← Variables de entorno (copia a .env)
└── app/
    ├── core/
    │   ├── config.py        ← Configuración (lee el .env)
    │   ├── database.py      ← Conexión SQLAlchemy async
    │   └── security.py      ← JWT + bcrypt
    ├── models/
    │   ├── usuario.py       ← Tabla usuarios
    │   ├── noticia.py       ← Tablas noticias + etiquetas
    │   └── evento_imagen.py ← Tablas eventos + imágenes
    ├── schemas/
    │   └── schemas.py       ← Modelos Pydantic (request/response)
    └── routers/
        ├── auth.py          ← POST /api/auth/login
        ├── noticias.py      ← CRUD /api/noticias
        ├── eventos.py       ← CRUD /api/eventos
        └── imagenes_usuarios.py ← CRUD /api/imagenes + /api/usuarios
```

---

## Instalación

### 1. Requisitos previos
- Python 3.13 instalado
- Proyecto en Supabase creado con el SQL de `cabanillas-supabase.sql`

### 2. Clonar y preparar entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Mac/Linux)
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env
```

Edita el `.env` con tus datos de Supabase:

```env
# Lo encuentras en: Supabase → Settings → Database → Connection string → URI
# Cambia [YOUR-PASSWORD] por tu contraseña
DATABASE_URL=postgresql+asyncpg://postgres:[YOUR-PASSWORD]@db.[TU-REF].supabase.co:5432/postgres

# Genera una clave segura con: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=tu_clave_secreta_muy_larga

ALLOWED_ORIGINS=http://localhost:4200
```

### 5. Arrancar el servidor

```bash
uvicorn main:app --reload --port 8000
```

La API estará disponible en:
- **API:** http://localhost:4200 → proxy → http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Endpoints disponibles

### Autenticación
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/login` | Iniciar sesión | No |
| POST | `/api/auth/registro` | Crear usuario | Admin |

### Noticias
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/noticias` | Lista con filtros y paginación | No |
| GET | `/api/noticias/destacada` | Noticia destacada portada | No |
| GET | `/api/noticias/ultimas` | Últimas publicadas | No |
| GET | `/api/noticias/{id}` | Detalle | No |
| POST | `/api/noticias` | Crear noticia | Sí |
| PUT | `/api/noticias/{id}` | Actualizar | Sí |
| PATCH | `/api/noticias/{id}/publicar` | Publicar | Sí |
| DELETE | `/api/noticias/{id}` | Eliminar | Sí |

### Eventos
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/eventos` | Lista con filtros | No |
| GET | `/api/eventos/proximos` | Próximos eventos | No |
| GET | `/api/eventos/{id}` | Detalle | No |
| POST | `/api/eventos` | Crear | Sí |
| PUT | `/api/eventos/{id}` | Actualizar | Sí |
| DELETE | `/api/eventos/{id}` | Eliminar | Sí |

### Imágenes
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/imagenes` | Lista por álbum | No |
| GET | `/api/imagenes/albumes` | Lista de álbumes | No |
| POST | `/api/imagenes` | Registrar imagen | Sí |
| DELETE | `/api/imagenes/{id}` | Eliminar | Sí |

### Usuarios
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/usuarios` | Lista | Admin |
| GET | `/api/usuarios/me` | Mi perfil | Sí |
| PUT | `/api/usuarios/{id}` | Actualizar | Admin |
| DELETE | `/api/usuarios/{id}` | Eliminar | Admin |

---

## Conectar con Angular

En `src/environments/environment.ts` de tu proyecto Angular:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};
```

---

## Credenciales de prueba

El SQL de Supabase crea un usuario admin de ejemplo.  
Para crear el hash correcto desde Python:

```python
from passlib.context import CryptContext
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(pwd.hash("TuContraseña123!"))
```

Luego actualiza el `password_hash` en Supabase:
```sql
UPDATE usuarios
SET password_hash = '$2b$12$...'  -- el hash generado
WHERE email = 'admin@cabanillas.es';
```
