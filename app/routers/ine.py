import json
import httpx
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/ine", tags=["INE"])

# Serie directa de Cabanillas de la Sierra - Total habitantes
# Obtenida consultando SERIES_TABLA/29005 - COD: DPOP13009
SERIE_CABANILLAS = "DPOP13009"
INE_SERIE_URL = f"https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/{SERIE_CABANILLAS}"


@router.get("/poblacion")
async def get_poblacion_cabanillas():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                INE_SERIE_URL,
                params={"nult": 1},
                timeout=10.0
            )
            response.raise_for_status()
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Timeout al conectar con el INE")
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail="Error en la API del INE"
            )

    try:
        data = json.loads(response.content.decode("latin-1"))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error decodificando respuesta del INE: {str(e)}"
        )

    if not data or not data.get("Data"):
        raise HTTPException(
            status_code=404,
            detail="No se encontraron datos de población"
        )

    dato = data["Data"][0]

    return {
        "municipio": "Cabanillas de la Sierra",
        "codigo_ine": "28029",
        "total": round(dato["Valor"]),
        "año": dato["Anyo"]
    }