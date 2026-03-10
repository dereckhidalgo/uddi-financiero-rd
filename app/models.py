from sqlalchemy import Column, String, Numeric, DateTime, Text, Integer, Date
from sqlalchemy.sql import func
from app.database import Base


class TasaCambiaria(Base):
    __tablename__ = "tasa_cambiaria"

    id            = Column(Integer, primary_key=True, index=True)
    codigo_moneda = Column(String(10), nullable=False)
    tasa          = Column(Numeric(10, 2), nullable=False)
    fecha         = Column(Date, nullable=False)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())


class IndiceInflacion(Base):
    __tablename__ = "indice_inflacion"

    id         = Column(Integer, primary_key=True, index=True)
    periodo    = Column(String(6), nullable=False, unique=True)  # yyyymm
    indice     = Column(Numeric(6, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Cliente(Base):
    __tablename__ = "clientes"

    id         = Column(Integer, primary_key=True, index=True)
    cedula_rnc = Column(String(20), nullable=False, unique=True)
    nombre     = Column(String(100), nullable=False)
    tipo       = Column(String(10), nullable=False)  # CEDULA / RNC
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SaludFinanciera(Base):
    __tablename__ = "salud_financiera"

    id             = Column(Integer, primary_key=True, index=True)
    cedula_rnc     = Column(String(20), nullable=False, unique=True)
    indicador      = Column(String(1), nullable=False)   # S / N
    comentario     = Column(Text, nullable=False)
    monto_adeudado = Column(Numeric(12, 2), nullable=False)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())


class HistorialCrediticio(Base):
    __tablename__ = "historial_crediticio"

    id             = Column(Integer, primary_key=True, index=True)
    cedula_rnc     = Column(String(20), nullable=False)
    rnc_empresa    = Column(String(20), nullable=False)
    concepto_deuda = Column(Text, nullable=False)
    fecha          = Column(Date, nullable=False)
    monto_adeudado = Column(Numeric(12, 2), nullable=False)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())


class UsoServicio(Base):
    __tablename__ = "uso_servicios"

    id           = Column(Integer, primary_key=True, index=True)
    nombre_ws    = Column(String(100), nullable=False)
    parametros   = Column(Text, nullable=True)
    ip_cliente   = Column(String(50), nullable=True)
    fecha_invocacion = Column(DateTime(timezone=True), server_default=func.now())
