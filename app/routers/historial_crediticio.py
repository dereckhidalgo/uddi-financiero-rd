from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import HistorialCrediticio
from app.services.logger import registrar_uso
from app.services.validaciones import valida_cedula_o_rnc

router = APIRouter()


@router.get(
    "/historial-crediticio",
    summary="Consultar historial crediticio de un cliente",
    description="""
Retorna el historial de deudas registradas de un cliente identificado por su **Cédula** o **RNC**.

**Validaciones aplicadas:**
- Cédula: 11 dígitos, algoritmo de verificación oficial RD
- RNC: 9 dígitos, primer dígito debe ser 1, 4 o 5, algoritmo de verificación oficial RD
- Acepta formato con o sin guiones

Cada registro incluye:
- `rnc_empresa`: RNC de la empresa acreedora
- `concepto_deuda`: descripción de la deuda
- `fecha`: fecha del registro
- `monto_adeudado`: monto en DOP

**Cédulas de prueba disponibles:**
`00100123456`, `00200234567`, `00300345678`, `00400456789`,
`00500567890`, `00600678901`, `00700789012`, `00800890123`

**RNC de prueba disponibles:**
`131000124`, `132000258`, `133000369`, `134000478`

> Usa `/api/v1/clientes` para ver la lista completa.
""",
)
def consultar_historial_crediticio(
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
        "historial-crediticio",
        parametros=f"cedula_rnc={cedula_rnc}&tipo={tipo}",
        ip_cliente=request.client.host
    )

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
        "tipo": tipo,
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
