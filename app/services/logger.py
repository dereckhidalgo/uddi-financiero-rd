from sqlalchemy.orm import Session
from app.models import UsoServicio


def registrar_uso(db: Session, nombre_ws: str, parametros: str = None, ip_cliente: str = None):
    registro = UsoServicio(
        nombre_ws=nombre_ws,
        parametros=parametros,
        ip_cliente=ip_cliente,
    )
    db.add(registro)
    db.commit()
