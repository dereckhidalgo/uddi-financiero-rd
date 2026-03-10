from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database import get_db
from app.models import UsoServicio
from app.services.logger import registrar_uso
from typing import Optional
from datetime import datetime

router = APIRouter()


@router.get("/uso-servicios", summary="Consulta de uso de Web Services")
def consultar_uso_servicios(
    request: Request,
    nombre_ws: Optional[str] = None,
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    db: Session = Depends(get_db)
):
    registrar_uso(db, "uso-servicios", ip_cliente=request.client.host)

    query = db.query(UsoServicio)
    filtros = []

    if nombre_ws:
        filtros.append(UsoServicio.nombre_ws.ilike(f"%{nombre_ws}%"))

    if fecha_inicio:
        try:
            fi = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            filtros.append(UsoServicio.fecha_invocacion >= fi)
        except ValueError:
            pass

    if fecha_fin:
        try:
            ff = datetime.strptime(fecha_fin, "%Y-%m-%d")
            ff = ff.replace(hour=23, minute=59, second=59)
            filtros.append(UsoServicio.fecha_invocacion <= ff)
        except ValueError:
            pass

    if filtros:
        query = query.filter(and_(*filtros))

    registros = query.order_by(UsoServicio.fecha_invocacion.desc()).limit(100).all()

    return {
        "total": len(registros),
        "filtros_aplicados": {
            "nombre_ws": nombre_ws,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin
        },
        "registros": [
            {
                "id": r.id,
                "nombre_ws": r.nombre_ws,
                "parametros": r.parametros,
                "ip_cliente": r.ip_cliente,
                "fecha_invocacion": str(r.fecha_invocacion)
            }
            for r in registros
        ]
    }
