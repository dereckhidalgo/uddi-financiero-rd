from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import tasa_cambiaria, inflacion, salud_financiera, historial_crediticio, uso_servicios, clientes
from app.database import engine
from app import models
import os

models.Base.metadata.create_all(bind=engine)

description = """
## UDDI — Servicios Web Financieros República Dominicana

Sistema de consulta de información financiera de RD expuesto como API REST.

---

### 📋 Servicios disponibles

| Servicio | Descripción |
|---|---|
| **Clientes** | Lista de cédulas y RNC disponibles para consulta |
| **Tasa Cambiaria** | Tasa de cambio en DOP según código ISO 4217 |
| **Índice de Inflación** | Porcentaje de inflación mensual por período |
| **Salud Financiera** | Estado financiero de un cliente por cédula o RNC |
| **Historial Crediticio** | Deudas registradas de un cliente por cédula o RNC |
| **Uso de Servicios** | Log de invocaciones con filtros por nombre y fecha |

---

### Dashboard
Visualiza el uso de los servicios en: `/dashboard`

"""

app = FastAPI(
    title="UDDI - Servicios Web Financieros RD",
    description=description,
    version="1.0.0",
    contact={
        "name": "UDDI Financiero RD",
        "url": "https://github.com/dereckhidalgo/uddi-financiero-rd",
    },
    license_info={
        "name": "MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(clientes.router,             prefix="/api/v1", tags=["Clientes"])
app.include_router(tasa_cambiaria.router,       prefix="/api/v1", tags=["Tasa Cambiaria"])
app.include_router(inflacion.router,            prefix="/api/v1", tags=["Inflación"])
app.include_router(salud_financiera.router,     prefix="/api/v1", tags=["Salud Financiera"])
app.include_router(historial_crediticio.router, prefix="/api/v1", tags=["Historial Crediticio"])
app.include_router(uso_servicios.router,        prefix="/api/v1", tags=["Uso de Servicios"])

@app.get("/dashboard", include_in_schema=False)
def dashboard():
    return FileResponse(os.path.join(static_dir, "dashboard.html"))

@app.get("/", tags=["Root"])
def root():
    return {
        "mensaje": "UDDI Servicios Web Financieros RD",
        "version": "1.0.0",
        "docs": "/docs",
        "dashboard": "/dashboard",
        "endpoints": [
            "/api/v1/clientes",
            "/api/v1/tasa-cambiaria",
            "/api/v1/inflacion",
            "/api/v1/salud-financiera",
            "/api/v1/historial-crediticio",
            "/api/v1/uso-servicios",
        ]
    }
