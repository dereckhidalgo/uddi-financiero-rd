from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import HistorialCrediticio
from app.services.logger import registrar_uso

router = APIRouter()


@router.get("/historial-crediticio", summary="Consultar historial crediticio de un cliente")
def consultar_historial_crediticio(
    cedula_rnc: str,
    request: Request,
    db: Session = Depends(get_db)
):
    cedula_rnc = cedula_rnc.strip()

    if not cedula_rnc:
        raise HTTPException(status_code=400, detail="Cédula o RNC requerido")

    registrar_uso(db, "historial-crediticio", parametros=f"cedula_rnc={cedula_rnc}", ip_cliente=request.client.host)

    registros = (
        db.query(HistorialCrediticio)
        .filter(HistorialCrediticio.cedula_rnc == cedula_rnc)
        .order_by(HistorialCrediticio.fecha.desc())
        .all()
    )

    if not registros:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró historial crediticio para la cédula/RNC: {cedula_rnc}"
        )

    total_adeudado = sum(float(r.monto_adeudado) for r in registros)

    return {
        "cedula_rnc": cedula_rnc,
        "total_deudas": len(registros),
        "total_adeudado": total_adeudado,
        "historial": [
            {
                "rnc_empresa": r.rnc_empresa,
                "concepto_deuda": r.concepto_deuda,
                "fecha": str(r.fecha),
                "monto_adeudado": float(r.monto_adeudado)
            }
            for r in registros
        ]
    }
