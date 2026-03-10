from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tasa_cambiaria, inflacion, salud_financiera, historial_crediticio, uso_servicios, clientes
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

description = """
## UDDI — Servicios Web Financieros República Dominicana

Sistema de consulta de información financiera de RD expuesto como API REST.

---

### Servicios disponibles

| Servicio | Descripción |
|---|---|
| **Clientes** | Lista de cédulas y RNC disponibles para consulta |
| **Tasa Cambiaria** | Tasa de cambio en DOP según código ISO 4217 |
| **Índice de Inflación** | Porcentaje de inflación mensual por período |
| **Salud Financiera** | Estado financiero de un cliente por cédula o RNC |
| **Historial Crediticio** | Deudas registradas de un cliente por cédula o RNC |
| **Uso de Servicios** | Log de invocaciones con filtros por nombre y fecha |

---

### ⚠️ Notas
- Todos los endpoints registran automáticamente su uso, consultable en `/api/v1/uso-servicios`.
- La moneda base siempre es **DOP (Peso Dominicano)**.
"""

app = FastAPI(
    title="UDDI - Servicios Web Financieros RD",
    description=description,
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes.router,             prefix="/api/v1", tags=["Clientes"])
app.include_router(tasa_cambiaria.router,       prefix="/api/v1", tags=["Tasa Cambiaria"])
app.include_router(inflacion.router,            prefix="/api/v1", tags=["Inflación"])
app.include_router(salud_financiera.router,     prefix="/api/v1", tags=["Salud Financiera"])
app.include_router(historial_crediticio.router, prefix="/api/v1", tags=["Historial Crediticio"])
app.include_router(uso_servicios.router,        prefix="/api/v1", tags=["Uso de Servicios"])

@app.get("/", tags=["Root"])
def root():
    return {
        "mensaje": "UDDI Servicios Web Financieros RD",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": [
            "/api/v1/clientes",
            "/api/v1/tasa-cambiaria",
            "/api/v1/inflacion",
            "/api/v1/salud-financiera",
            "/api/v1/historial-crediticio",
            "/api/v1/uso-servicios",
        ]
    }
