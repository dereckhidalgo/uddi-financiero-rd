from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Cliente
from app.services.logger import registrar_uso

router = APIRouter()


@router.get("/clientes", summary="Lista de clientes disponibles para consulta")
def listar_clientes(request: Request, db: Session = Depends(get_db)):
    registrar_uso(db, "clientes", ip_cliente=request.client.host)

    clientes = db.query(Cliente).all()
    return {
        "total": len(clientes),
        "clientes": [
            {
                "cedula_rnc": c.cedula_rnc,
                "nombre": c.nombre,
                "tipo": c.tipo
            }
            for c in clientes
        ]
    }
