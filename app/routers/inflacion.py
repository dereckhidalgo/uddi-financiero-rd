from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import IndiceInflacion
from app.services.logger import registrar_uso
import re

router = APIRouter()


@router.get(
    "/inflacion",
    summary="Consultar índice de inflación por período",
    description="""
Retorna el índice de inflación mensual de República Dominicana para un período dado.

**Formato del período:** `yyyymm`

| Ejemplo | Descripción |
|---|---|
| `202603` | Marzo 2026 |

**Períodos disponibles:** desde `201501` hasta `202603`.

**Fuente de datos:** Banco Central de la República Dominicana (BCRD).
""",
)
def consultar_inflacion(
    periodo: str,
    request: Request,
    db: Session = Depends(get_db)
):
    # Validar formato yyyymm
    if not re.match(r"^\d{4}(0[1-9]|1[0-2])$", periodo):
        raise HTTPException(
            status_code=400,
            detail="Formato de período inválido. Use yyyymm (ej: 202401)"
        )

    registrar_uso(db, "inflacion", parametros=f"periodo={periodo}", ip_cliente=request.client.host)

    registro = db.query(IndiceInflacion).filter(IndiceInflacion.periodo == periodo).first()

    if not registro:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró índice de inflación para el período {periodo}"
        )

    anio = periodo[:4]
    mes  = periodo[4:]

    return {
        "periodo": periodo,
        "anio": anio,
        "mes": mes,
        "indice_inflacion": float(registro.indice),
        "unidad": "%",
        "fuente": "Base de Datos UDDI"
    }
