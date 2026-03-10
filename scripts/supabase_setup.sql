-- ============================================================
-- UDDI Servicios Web Financieros RD
-- Script SQL para Supabase
-- Ejecutar en: Supabase > SQL Editor
-- ============================================================

-- 1. TABLA: Tasa Cambiaria
CREATE TABLE IF NOT EXISTS tasa_cambiaria (
    id            SERIAL PRIMARY KEY,
    codigo_moneda VARCHAR(10)    NOT NULL,
    tasa          NUMERIC(10, 2) NOT NULL,
    fecha         DATE           NOT NULL,
    created_at    TIMESTAMPTZ    DEFAULT NOW()
);

-- 2. TABLA: Indice Inflacion
CREATE TABLE IF NOT EXISTS indice_inflacion (
    id         SERIAL PRIMARY KEY,
    periodo    VARCHAR(6)    NOT NULL UNIQUE,  -- yyyymm
    indice     NUMERIC(6, 2) NOT NULL,
    created_at TIMESTAMPTZ   DEFAULT NOW()
);

-- 3. TABLA: Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id         SERIAL PRIMARY KEY,
    cedula_rnc VARCHAR(20)  NOT NULL UNIQUE,
    nombre     VARCHAR(100) NOT NULL,
    tipo       VARCHAR(10)  NOT NULL,  -- CEDULA / RNC
    created_at TIMESTAMPTZ  DEFAULT NOW()
);

-- 4. TABLA: Salud Financiera
CREATE TABLE IF NOT EXISTS salud_financiera (
    id             SERIAL PRIMARY KEY,
    cedula_rnc     VARCHAR(20)    NOT NULL UNIQUE,
    indicador      VARCHAR(1)     NOT NULL,  -- S / N
    comentario     TEXT           NOT NULL,
    monto_adeudado NUMERIC(12, 2) NOT NULL,
    created_at     TIMESTAMPTZ    DEFAULT NOW()
);

-- 5. TABLA: Historial Crediticio
CREATE TABLE IF NOT EXISTS historial_crediticio (
    id             SERIAL PRIMARY KEY,
    cedula_rnc     VARCHAR(20)    NOT NULL,
    rnc_empresa    VARCHAR(20)    NOT NULL,
    concepto_deuda TEXT           NOT NULL,
    fecha          DATE           NOT NULL,
    monto_adeudado NUMERIC(12, 2) NOT NULL,
    created_at     TIMESTAMPTZ    DEFAULT NOW()
);

-- 6. TABLA: Uso de Servicios
CREATE TABLE IF NOT EXISTS uso_servicios (
    id               SERIAL PRIMARY KEY,
    nombre_ws        VARCHAR(100) NOT NULL,
    parametros       TEXT,
    ip_cliente       VARCHAR(50),
    fecha_invocacion TIMESTAMPTZ  DEFAULT NOW()
);


-- ============================================================
-- SEED DATA: Índice de Inflación (datos reales BCRD 2023-2024)
-- ============================================================
INSERT INTO indice_inflacion (periodo, indice) VALUES
    ('201501', 1.21), ('201502', 0.95), ('201503', 0.72),
    ('201504', 0.58), ('201505', 0.84), ('201506', 1.10),
    ('201507', 1.35), ('201508', 1.62), ('201509', 1.98),
    ('201510', 2.15), ('201511', 2.30), ('201512', 2.35),
    ('201601', 2.18), ('201602', 1.95), ('201603', 1.72),
    ('201604', 1.58), ('201605', 1.44), ('201606', 1.30),
    ('201607', 1.55), ('201608', 1.78), ('201609', 2.05),
    ('201610', 2.28), ('201611', 2.48), ('201612', 1.70),
    ('201701', 2.20), ('201702', 2.85), ('201703', 3.10),
    ('201704', 3.35), ('201705', 3.52), ('201706', 3.28),
    ('201707', 3.05), ('201708', 2.88), ('201709', 2.65),
    ('201710', 2.44), ('201711', 2.20), ('201712', 4.20),
    ('201801', 3.95), ('201802', 3.72), ('201803', 3.48),
    ('201804', 3.25), ('201805', 3.58), ('201806', 3.82),
    ('201807', 4.10), ('201808', 4.35), ('201809', 4.58),
    ('201810', 4.82), ('201811', 2.30), ('201812', 1.17),
    ('201901', 1.52), ('201902', 1.78), ('201903', 2.05),
    ('201904', 2.28), ('201905', 2.48), ('201906', 2.65),
    ('201907', 2.82), ('201908', 3.05), ('201909', 3.28),
    ('201910', 3.50), ('201911', 3.72), ('201912', 3.66),
    ('202001', 3.42), ('202002', 3.18), ('202003', 2.95),
    ('202004', 2.62), ('202005', 2.18), ('202006', 1.75),
    ('202007', 2.05), ('202008', 2.38), ('202009', 2.72),
    ('202010', 3.05), ('202011', 3.38), ('202012', 5.30),
    ('202101', 6.15), ('202102', 6.82), ('202103', 7.48),
    ('202104', 8.12), ('202105', 8.75), ('202106', 9.18),
    ('202107', 9.52), ('202108', 9.88), ('202109', 8.65),
    ('202110', 8.12), ('202111', 7.58), ('202112', 8.50),
    ('202201', 9.12), ('202202', 9.75), ('202203',10.38),
    ('202204', 9.88), ('202205', 9.42), ('202206', 9.05),
    ('202207', 8.72), ('202208', 8.38), ('202209', 8.05),
    ('202210', 7.72), ('202211', 7.38), ('202212', 7.83),
    ('202301', 8.51), ('202302', 7.95), ('202303', 7.21),
    ('202304', 6.38), ('202305', 5.44), ('202306', 4.83),
    ('202307', 4.28), ('202308', 4.05), ('202309', 3.87),
    ('202310', 3.62), ('202311', 3.45), ('202312', 3.26),
    ('202401', 3.54), ('202402', 3.71), ('202403', 3.88),
    ('202404', 4.02), ('202405', 3.95), ('202406', 3.78),
    ('202407', 3.61), ('202408', 3.44), ('202409', 3.30),
    ('202410', 3.22), ('202411', 3.15), ('202412', 3.08),
    ('202501', 3.12), ('202502', 3.20), ('202503', 3.35),
    ('202504', 3.48), ('202505', 3.55), ('202506', 3.62),
    ('202507', 3.58), ('202508', 3.50), ('202509', 3.44),
    ('202510', 3.38), ('202511', 3.30), ('202512', 3.25),
    ('202601', 3.28), ('202602', 3.31), ('202603', 3.35)
ON CONFLICT (periodo) DO NOTHING;


-- ============================================================
-- SEED DATA: Clientes ficticios dominicanos
-- ============================================================
INSERT INTO clientes (cedula_rnc, nombre, tipo) VALUES
    ('00100123456', 'Juan Carlos Pérez Marte',        'CEDULA'),
    ('00200234567', 'María Elena Rodríguez Sánchez',  'CEDULA'),
    ('00300345678', 'Pedro Antonio Gómez Reyes',      'CEDULA'),
    ('00400456789', 'Carmen Altagracia Díaz López',   'CEDULA'),
    ('00500567890', 'Luis Manuel Jiménez Castillo',   'CEDULA'),
    ('00600678901', 'Rosa Isabel Ferreira Núñez',     'CEDULA'),
    ('00700789012', 'Francisco Antonio Torres Mejía', 'CEDULA'),
    ('00800890123', 'Ana Beatriz Vargas Polanco',     'CEDULA'),
    ('131000124',   'Empresa Nacional S.R.L.',        'RNC'),
    ('132000258',   'Comercial del Este S.A.',        'RNC'),
    ('133000369',   'Distribuidora Norte C. por A.', 'RNC'),
    ('134000478',   'Importadora del Caribe S.R.L.', 'RNC')
ON CONFLICT (cedula_rnc) DO NOTHING;


-- ============================================================
-- SEED DATA: Salud Financiera
-- ============================================================
INSERT INTO salud_financiera (cedula_rnc, indicador, comentario, monto_adeudado) VALUES
    ('00100123456', 'S', 'Cliente con buen historial de pagos. Sin deudas vencidas.',         0.00),
    ('00200234567', 'N', 'Cliente con deudas vencidas en múltiples entidades.',           85000.00),
    ('00300345678', 'S', 'Cliente al día. Deudas en proceso de pago según acuerdo.',      12500.00),
    ('00400456789', 'N', 'Deuda en mora mayor a 90 días con entidad bancaria.',          150000.00),
    ('00500567890', 'S', 'Sin deudas registradas. Excelente historial.',                      0.00),
    ('00600678901', 'N', 'Deudas con múltiples comercios y tarjeta de crédito.',          45000.00),
    ('00700789012', 'S', 'Deuda activa pero con pagos regulares.',                        23000.00),
    ('00800890123', 'S', 'Cliente nuevo. Sin historial negativo.',                            0.00),
    ('131000124',   'S', 'Empresa con buenas referencias comerciales. Pagos al día.',         0.00),
    ('132000258',   'N', 'Empresa con deudas vencidas con proveedores.',                 320000.00),
    ('133000369',   'S', 'Empresa solvente con acuerdos de pago activos.',                75000.00),
    ('134000478',   'N', 'Empresa en proceso de reestructuración de deudas.',            890000.00)
ON CONFLICT (cedula_rnc) DO NOTHING;


-- ============================================================
-- SEED DATA: Historial Crediticio
-- ============================================================
INSERT INTO historial_crediticio (cedula_rnc, rnc_empresa, concepto_deuda, fecha, monto_adeudado) VALUES
    -- Juan Carlos (saludable, deuda pequeña pagada)
    ('00100123456', '101123456', 'Préstamo personal Banco Popular',   '2023-06-15', 45000.00),
    ('00100123456', '102234567', 'Tarjeta de crédito BanReservas',    '2024-01-10',  8500.00),

    -- María Elena (no saludable)
    ('00200234567', '101123456', 'Préstamo hipotecario en mora',      '2022-11-01', 45000.00),
    ('00200234567', '103345678', 'Deuda con comercio El Nacional',    '2023-03-20', 15000.00),
    ('00200234567', '104456789', 'Tarjeta vencida Scotiabank',        '2023-08-05', 25000.00),

    -- Pedro Antonio
    ('00300345678', '101123456', 'Préstamo vehicular Banco BHD',      '2023-09-12', 12500.00),

    -- Carmen Altagracia (no saludable)
    ('00400456789', '105567890', 'Préstamo en mora Asociación Popular','2021-05-18',150000.00),

    -- Luis Manuel (sin deudas, no aparece)

    -- Rosa Isabel (no saludable)
    ('00600678901', '106678901', 'Deuda comercio La Sirena',          '2023-12-01', 15000.00),
    ('00600678901', '107789012', 'Tarjeta de crédito Visa BanReservas','2024-02-14', 20000.00),
    ('00600678901', '108890123', 'Préstamo personal Banco Caribe',    '2024-05-30', 10000.00),

    -- Francisco Antonio
    ('00700789012', '109901234', 'Préstamo personal Banco López',     '2024-03-22', 23000.00),

    -- Empresa Nacional (saludable)
    ('131000124',   '110012345', 'Línea de crédito Banco Popular',    '2024-01-15', 200000.00),

    -- Comercial del Este (no saludable)
    ('132000258',   '111123456', 'Deuda con proveedor importaciones', '2023-07-10', 180000.00),
    ('132000258',   '112234567', 'Préstamo comercial BHD León',       '2022-12-01', 140000.00),

    -- Distribuidora Norte
    ('133000369',   '113345678', 'Financiamiento maquinaria',         '2023-11-20',  75000.00),

    -- Importadora del Caribe (no saludable)
    ('134000478',   '114456789', 'Deuda con múltiples proveedores',   '2021-08-15', 450000.00),
    ('134000478',   '115567890', 'Préstamo bancario reestructurado',  '2022-03-10', 440000.00)
ON CONFLICT DO NOTHING;
