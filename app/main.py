from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tasa_cambiaria, inflacion, salud_financiera, historial_crediticio, uso_servicios, clientes
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="UDDI - Servicios Web Financieros RD",
    description="Sistema de servicios web financieros para República Dominicana",
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
