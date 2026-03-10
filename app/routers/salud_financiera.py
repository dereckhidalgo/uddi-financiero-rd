from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import SaludFinanciera
from app.services.logger import registrar_uso
from app.services.validaciones import valida_cedula_o_rnc

router = APIRouter()


@router.get(
    "/salud-financiera",
    summary="Consultar salud financiera de un cliente",
    description="""
Retorna el estado de salud financiera de un cliente identificado por su **Cédula** o **RNC**.

> Usa `/api/v1/clientes` para ver la lista completa de las cedulas y RNC disponibles.
""",
)
def consultar_salud_financiera(
    cedula_rnc: str,
    request: Request,
    db: Session = Depends(get_db)
):
    cedula_rnc = cedula_rnc.strip()

    if not cedula_rnc:
        raise HTTPException(status_code=400, detail="Cédula o RNC requerido")

    es_valido, tipo = valida_cedula_o_rnc(cedula_rnc)
    if not es_valido:
        raise HTTPException(
            status_code=400,
            detail="Cédula o RNC inválido. Verifique el número ingresado. "
                   "Cédula: 11 dígitos. RNC: 9 dígitos comenzando en 1, 4 o 5."
        )

    registrar_uso(
        db,
        "salud-financiera",
        parametros=f"cedula_rnc={cedula_rnc}&tipo={tipo}",
        ip_cliente=request.client.host
    )

    registro = db.query(SaludFinanciera).filter(SaludFinanciera.cedula_rnc == cedula_rnc).first()

    if not registro:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró información financiera para la cédula/RNC: {cedula_rnc}"
        )

    return {
        "cedula_rnc": cedula_rnc,
        "tipo": tipo,
        "indicador": registro.indicador,
        "estado": "Saludable" if registro.indicador == "S" else "No Saludable",
        "comentario": registro.comentario,
        "monto_total_adeudado": float(registro.monto_adeudado)
    }
