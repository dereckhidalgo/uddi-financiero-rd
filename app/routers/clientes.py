from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Cliente
from app.services.logger import registrar_uso

router = APIRouter()


@router.get(
    "/clientes",
    summary="Lista de clientes disponibles",
    description="""
Retorna todos los clientes (personas físicas y empresas) registrados en el sistema.

Úsalo para conocer qué **cédulas** y **RNC** puedes consultar en los endpoints
de Salud Financiera e Historial Crediticio.

**Tipo de identificación:**
- `CEDULA` → persona física (11 dígitos)
- `RNC` → empresa (9 dígitos)
""",
)
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
