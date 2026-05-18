import httpx
import json
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from app.core.config import get_settings

router = APIRouter(prefix="/tiempo", tags=["Tiempo"])

AEMET_BASE = "https://opendata.aemet.es/opendata/api"

# Caché en memoria
_cache: dict = {
    "data": None,
    "expires": datetime.min
}

@router.get("")
async def get_tiempo():
    # Si hay caché válida la devolvemos directamente
    if _cache["data"] and datetime.now() < _cache["expires"]:
        return _cache["data"]

    settings  = get_settings()
    headers   = {"api_key": settings.AEMET_API_KEY}
    municipio = settings.AEMET_MUNICIPIO

    async with httpx.AsyncClient(verify=False) as client:
        r1 = await client.get(
            f"{AEMET_BASE}/prediccion/especifica/municipio/diaria/{municipio}",
            headers=headers, timeout=10
        )
        if r1.status_code != 200:
            raise HTTPException(status_code=502, detail=f"AEMET error {r1.status_code}")

        data_url = r1.json().get("datos")
        if not data_url:
            raise HTTPException(status_code=502, detail="AEMET no devolvió URL de datos")

        r2 = await client.get(data_url, timeout=10)
        if r2.status_code != 200:
            raise HTTPException(status_code=502, detail="Error obteniendo datos AEMET")

        texto = r2.content.decode('latin-1')
        data  = json.loads(texto)

        # Guardar en caché 30 minutos
        _cache["data"]    = data
        _cache["expires"] = datetime.now() + timedelta(minutes=30)

        return data