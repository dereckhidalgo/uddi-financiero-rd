from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.models import TasaCambiaria
from app.services.logger import registrar_uso
import httpx
from datetime import date

router = APIRouter()

# Códigos ISO 4217 soportados con metadata
MONEDAS_ISO_4217 = {
    "USD": {"nombre": "Dólar Estadounidense",     "simbolo": "$",  "fallback": 59.50},
    "EUR": {"nombre": "Euro",                      "simbolo": "€",  "fallback": 64.20},
    "GBP": {"nombre": "Libra Esterlina",           "simbolo": "£",  "fallback": 75.10},
    "CAD": {"nombre": "Dólar Canadiense",          "simbolo": "$",  "fallback": 43.80},
    "CHF": {"nombre": "Franco Suizo",              "simbolo": "Fr", "fallback": 66.30},
    "JPY": {"nombre": "Yen Japonés",               "simbolo": "¥",  "fallback":  0.40},
    "MXN": {"nombre": "Peso Mexicano",             "simbolo": "$",  "fallback":  3.20},
    "COP": {"nombre": "Peso Colombiano",           "simbolo": "$",  "fallback":  0.015},
    "BRL": {"nombre": "Real Brasileño",            "simbolo": "R$", "fallback": 11.80},
    "DKK": {"nombre": "Corona Danesa",             "simbolo": "kr", "fallback":  8.60},
    "SEK": {"nombre": "Corona Sueca",              "simbolo": "kr", "fallback":  5.50},
    "NOK": {"nombre": "Corona Noruega",            "simbolo": "kr", "fallback":  5.40},
    "CNY": {"nombre": "Yuan Chino",                "simbolo": "¥",  "fallback":  8.20},
    "HTG": {"nombre": "Gourde Haitiano",           "simbolo": "G",  "fallback":  0.44},
    "DOP": {"nombre": "Peso Dominicano",           "simbolo": "RD$","fallback":  1.00},
}


async def obtener_tasa_bcrd(codigo_iso: str) -> float | None:
    """
    Intenta obtener la tasa desde el Banco Central RD.
    Si falla, retorna None y se usa la BD como fallback.
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                "https://api.bcrd.gov.do/tasas",
                headers={"Accept": "application/json"}
            )
            if resp.status_code == 200:
                data = resp.json()
                for item in data:
                    if item.get("codigo") == codigo_iso:
                        return float(item.get("tasa", 0))
    except Exception:
        pass

    # Fallback con tasas aproximadas
    moneda = MONEDAS_ISO_4217.get(codigo_iso)
    return moneda["fallback"] if moneda else None


@router.get("/tasa-cambiaria", summary="Consultar tasa de cambio según código ISO 4217")
async def consultar_tasa_cambiaria(
    codigo_moneda: str,
    request: Request,
    db: Session = Depends(get_db)
):
    codigo_moneda = codigo_moneda.upper().strip()

    if len(codigo_moneda) != 3:
        raise HTTPException(
            status_code=400,
            detail="El código de moneda debe tener exactamente 3 caracteres según ISO 4217 (ej: USD, EUR, GBP)"
        )

    if codigo_moneda not in MONEDAS_ISO_4217:
        codigos = ", ".join(sorted(MONEDAS_ISO_4217.keys()))
        raise HTTPException(
            status_code=400,
            detail=f"Código ISO 4217 no soportado: '{codigo_moneda}'. Códigos disponibles: {codigos}"
        )

    if codigo_moneda == "DOP":
        raise HTTPException(
            status_code=400,
            detail="DOP es la moneda base. No se puede consultar su propia tasa."
        )

    registrar_uso(
        db,
        "tasa-cambiaria",
        parametros=f"codigo_iso={codigo_moneda}",
        ip_cliente=request.client.host
    )

    meta = MONEDAS_ISO_4217[codigo_moneda]

    # 1. Intentar obtener del BCRD
    tasa_valor = await obtener_tasa_bcrd(codigo_moneda)

    if tasa_valor:
        registro = TasaCambiaria(
            codigo_moneda=codigo_moneda,
            tasa=tasa_valor,
            fecha=date.today()
        )
        db.add(registro)
        db.commit()
        fuente = "Banco Central RD"
    else:
        # Fallback: último registro en BD
        registro = (
            db.query(TasaCambiaria)
            .filter(TasaCambiaria.codigo_moneda == codigo_moneda)
            .order_by(desc(TasaCambiaria.fecha))
            .first()
        )
        if not registro:
            raise HTTPException(status_code=404, detail=f"No se encontró tasa para {codigo_moneda}")
        tasa_valor = float(registro.tasa)
        fuente = "Base de Datos (caché)"

    return {
        "codigo_iso_4217": codigo_moneda,
        "nombre_moneda":   meta["nombre"],
        "simbolo":         meta["simbolo"],
        "tasa_cambiaria":  tasa_valor,
        "moneda_base":     "DOP",
        "descripcion":     f"1 {codigo_moneda} = {tasa_valor} DOP",
        "fecha":           str(date.today()),
        "fuente":          fuente
    }


@router.get("/tasa-cambiaria/monedas", summary="Lista de monedas disponibles (ISO 4217)")
def listar_monedas(request: Request, db: Session = Depends(get_db)):
    registrar_uso(db, "tasa-cambiaria/monedas", ip_cliente=request.client.host)
    return {
        "total": len(MONEDAS_ISO_4217) - 1,  # excluye DOP
        "moneda_base": "DOP",
        "monedas": [
            {
                "codigo_iso_4217": codigo,
                "nombre":          meta["nombre"],
                "simbolo":         meta["simbolo"],
            }
            for codigo, meta in MONEDAS_ISO_4217.items()
            if codigo != "DOP"
        ]
    }
