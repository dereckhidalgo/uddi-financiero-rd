from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import SaludFinanciera
from app.services.logger import registrar_uso

router = APIRouter()


@router.get("/salud-financiera", summary="Consultar salud financiera de un cliente")
def consultar_salud_financiera(
    cedula_rnc: str,
    request: Request,
    db: Session = Depends(get_db)
):
    cedula_rnc = cedula_rnc.strip()

    if not cedula_rnc:
        raise HTTPException(status_code=400, detail="Cédula o RNC requerido")

    registrar_uso(db, "salud-financiera", parametros=f"cedula_rnc={cedula_rnc}", ip_cliente=request.client.host)

    registro = db.query(SaludFinanciera).filter(SaludFinanciera.cedula_rnc == cedula_rnc).first()

    if not registro:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró información financiera para la cédula/RNC: {cedula_rnc}"
        )

    return {
        "cedula_rnc": cedula_rnc,
        "indicador": registro.indicador,
        "estado": "Saludable" if registro.indicador == "S" else "No Saludable",
        "comentario": registro.comentario,
        "monto_total_adeudado": float(registro.monto_adeudado)
    }
