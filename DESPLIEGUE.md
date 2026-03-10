# UDDI Servicios Web Financieros RD
## Guía de Despliegue Completa

---

## Arquitectura

```
Internet → Render.com (FastAPI) → Supabase (PostgreSQL)
                   ↓
           BCRD API (tasas en tiempo real)
```

---

## PASO 1: Configurar Supabase (Base de Datos)

1. Ir a **https://supabase.com** → Sign Up (gratis)
2. Crear nuevo proyecto:
   - **Name:** uddi-financiero-rd
   - **Database Password:** (guardar bien esta contraseña)
   - **Region:** East US (más cercano a RD)
3. Esperar que el proyecto inicie (~2 minutos)
4. Ir a **SQL Editor** (menú izquierdo)
5. Pegar TODO el contenido del archivo `scripts/supabase_setup.sql`
6. Click en **Run** → debe decir "Success"
7. Ir a **Project Settings → Database → Connection String → URI**
8. Copiar la URI (se ve así):
   ```
   postgresql://postgres:[PASSWORD]@db.xxxxxxxxxxxx.supabase.co:5432/postgres
   ```
   ⚠️ Reemplazar `[PASSWORD]` con la contraseña que pusiste al crear el proyecto

---

## PASO 2: Subir código a GitHub

1. Crear cuenta en **https://github.com** (si no tienes)
2. Crear nuevo repositorio:
   - **Name:** uddi-financiero-rd
   - **Visibility:** Public
3. Subir todos los archivos del proyecto:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - UDDI Servicios Web RD"
   git remote add origin https://github.com/TU-USUARIO/uddi-financiero-rd.git
   git push -u origin main
   ```
   ⚠️ Asegúrate de que el archivo `.env` NO esté en GitHub (está en .gitignore)

---

## PASO 3: Desplegar en Render

1. Ir a **https://render.com** → Sign Up con GitHub (gratis)
2. Click en **New → Web Service**
3. Conectar tu repositorio `uddi-financiero-rd`
4. Configurar:
   - **Name:** uddi-financiero-rd
   - **Environment:** Docker
   - **Branch:** main
   - **Plan:** Free
5. En **Environment Variables**, agregar:
   - **Key:** `DATABASE_URL`
   - **Value:** la URI de Supabase del Paso 1
6. Click **Create Web Service**
7. Esperar el despliegue (~5 minutos)
8. Render te dará una URL como:
   ```
   https://uddi-financiero-rd.onrender.com
   ```

---

## PASO 4: Verificar que funciona

Una vez desplegado, probar en el navegador:

### Documentación interactiva (Swagger UI)
```
https://uddi-financiero-rd.onrender.com/docs
```

### Probar endpoints:

| Endpoint | URL de prueba |
|---|---|
| Root | `/` |
| Clientes disponibles | `/api/v1/clientes` |
| Tasa DOL | `/api/v1/tasa-cambiaria?codigo_moneda=DOL` |
| Tasa EUR | `/api/v1/tasa-cambiaria?codigo_moneda=EUR` |
| Inflación | `/api/v1/inflacion?periodo=202401` |
| Salud Financiera | `/api/v1/salud-financiera?cedula_rnc=00100123456` |
| Historial Crediticio | `/api/v1/historial-crediticio?cedula_rnc=00200234567` |
| Uso de Servicios | `/api/v1/uso-servicios` |
| Uso filtrado por WS | `/api/v1/uso-servicios?nombre_ws=tasa-cambiaria` |
| Uso por rango fecha | `/api/v1/uso-servicios?fecha_inicio=2024-01-01&fecha_fin=2024-12-31` |

---

## Clientes de prueba disponibles

### Cédulas (personas físicas)
| Cédula | Nombre | Salud |
|---|---|---|
| 00100123456 | Juan Carlos Pérez Marte | ✅ Saludable |
| 00200234567 | María Elena Rodríguez Sánchez | ❌ No Saludable |
| 00300345678 | Pedro Antonio Gómez Reyes | ✅ Saludable |
| 00400456789 | Carmen Altagracia Díaz López | ❌ No Saludable |
| 00500567890 | Luis Manuel Jiménez Castillo | ✅ Saludable |
| 00600678901 | Rosa Isabel Ferreira Núñez | ❌ No Saludable |
| 00700789012 | Francisco Antonio Torres Mejía | ✅ Saludable |
| 00800890123 | Ana Beatriz Vargas Polanco | ✅ Saludable |

### RNC (empresas)
| RNC | Empresa | Salud |
|---|---|---|
| 131000124 | Empresa Nacional S.R.L. | ✅ Saludable |
| 132000258 | Comercial del Este S.A. | ❌ No Saludable |
| 133000369 | Distribuidora Norte C. por A. | ✅ Saludable |
| 134000478 | Importadora del Caribe S.R.L. | ❌ No Saludable |

### Monedas disponibles
`DOL`, `EUR`, `PES`, `GBP`, `CAD`, `CHF`, `JPY`

### Períodos de inflación disponibles
`202301` hasta `202503`

---

## Stack tecnológico

| Componente | Tecnología | Tipo |
|---|---|---|
| Lenguaje | Python 3.11 | Open-source |
| Framework API | FastAPI | Open-source |
| Base de Datos | Supabase (PostgreSQL) | Propietario |
| Despliegue | Render.com | Propietario |
| ORM | SQLAlchemy | Open-source |
| HTTP Client | HTTPX | Open-source |

---

## Estructura del proyecto

```
uddi-financiero/
├── app/
│   ├── main.py                    # Punto de entrada FastAPI
│   ├── database.py                # Conexión Supabase
│   ├── models.py                  # Tablas SQLAlchemy
│   ├── routers/
│   │   ├── clientes.py            # GET /clientes
│   │   ├── tasa_cambiaria.py      # GET /tasa-cambiaria
│   │   ├── inflacion.py           # GET /inflacion
│   │   ├── salud_financiera.py    # GET /salud-financiera
│   │   ├── historial_crediticio.py # GET /historial-crediticio
│   │   └── uso_servicios.py       # GET /uso-servicios
│   └── services/
│       └── logger.py              # Registro automático de invocaciones
├── scripts/
│   └── supabase_setup.sql         # Tablas + seed data
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
└── DESPLIEGUE.md
```
