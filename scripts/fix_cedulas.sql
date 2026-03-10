-- ============================================================
-- Script: Corregir cédulas y RNC en la BD
-- Ejecutar en Supabase > SQL Editor
-- ============================================================

-- Limpiar tablas de clientes (preserva inflación y tasas)
DELETE FROM historial_crediticio;
DELETE FROM salud_financiera;
DELETE FROM clientes;

-- Reinsertar clientes con cédulas/RNC válidos
INSERT INTO clientes (cedula_rnc, nombre, tipo) VALUES
    ('00110000007', 'Juan Carlos Pérez Marte',        'CEDULA'),
    ('00110000015', 'María Elena Rodríguez Sánchez',  'CEDULA'),
    ('00110000023', 'Pedro Antonio Gómez Reyes',      'CEDULA'),
    ('00110000031', 'Carmen Altagracia Díaz López',   'CEDULA'),
    ('00110000049', 'Luis Manuel Jiménez Castillo',   'CEDULA'),
    ('00110000056', 'Rosa Isabel Ferreira Núñez',     'CEDULA'),
    ('00110000064', 'Francisco Antonio Torres Mejía', 'CEDULA'),
    ('00110000072', 'Ana Beatriz Vargas Polanco',     'CEDULA'),
    ('131000002',   'Empresa Nacional S.R.L.',        'RNC'),
    ('131000011',   'Comercial del Este S.A.',        'RNC'),
    ('131000029',   'Distribuidora Norte C. por A.', 'RNC'),
    ('131000037',   'Importadora del Caribe S.R.L.', 'RNC');

-- Reinsertar salud financiera
INSERT INTO salud_financiera (cedula_rnc, indicador, comentario, monto_adeudado) VALUES
    ('00110000007', 'S', 'Cliente con buen historial de pagos. Sin deudas vencidas.',         0.00),
    ('00110000015', 'N', 'Cliente con deudas vencidas en múltiples entidades.',           85000.00),
    ('00110000023', 'S', 'Cliente al día. Deudas en proceso de pago según acuerdo.',      12500.00),
    ('00110000031', 'N', 'Deuda en mora mayor a 90 días con entidad bancaria.',          150000.00),
    ('00110000049', 'S', 'Sin deudas registradas. Excelente historial.',                      0.00),
    ('00110000056', 'N', 'Deudas con múltiples comercios y tarjeta de crédito.',          45000.00),
    ('00110000064', 'S', 'Deuda activa pero con pagos regulares.',                        23000.00),
    ('00110000072', 'S', 'Cliente nuevo. Sin historial negativo.',                            0.00),
    ('131000002',   'S', 'Empresa con buenas referencias comerciales. Pagos al día.',         0.00),
    ('131000011',   'N', 'Empresa con deudas vencidas con proveedores.',                 320000.00),
    ('131000029',   'S', 'Empresa solvente con acuerdos de pago activos.',                75000.00),
    ('131000037',   'N', 'Empresa en proceso de reestructuración de deudas.',            890000.00);

-- Reinsertar historial crediticio
INSERT INTO historial_crediticio (cedula_rnc, rnc_empresa, concepto_deuda, fecha, monto_adeudado) VALUES
    ('00110000007', '101123456', 'Préstamo personal Banco Popular',    '2023-06-15', 45000.00),
    ('00110000007', '102234567', 'Tarjeta de crédito BanReservas',     '2024-01-10',  8500.00),
    ('00110000015', '101123456', 'Préstamo hipotecario en mora',       '2022-11-01', 45000.00),
    ('00110000015', '103345678', 'Deuda con comercio El Nacional',     '2023-03-20', 15000.00),
    ('00110000015', '104456789', 'Tarjeta vencida Scotiabank',         '2023-08-05', 25000.00),
    ('00110000023', '101123456', 'Préstamo vehicular Banco BHD',       '2023-09-12', 12500.00),
    ('00110000031', '105567890', 'Préstamo en mora Asociación Popular','2021-05-18',150000.00),
    ('00110000056', '106678901', 'Deuda comercio La Sirena',           '2023-12-01', 15000.00),
    ('00110000056', '107789012', 'Tarjeta de crédito Visa BanReservas','2024-02-14', 20000.00),
    ('00110000056', '108890123', 'Préstamo personal Banco Caribe',     '2024-05-30', 10000.00),
    ('00110000064', '109901234', 'Préstamo personal Banco López',      '2024-03-22', 23000.00),
    ('131000002',   '110012345', 'Línea de crédito Banco Popular',     '2024-01-15',200000.00),
    ('131000011',   '111123456', 'Deuda con proveedor importaciones',  '2023-07-10',180000.00),
    ('131000011',   '112234567', 'Préstamo comercial BHD León',        '2022-12-01',140000.00),
    ('131000029',   '113345678', 'Financiamiento maquinaria',          '2023-11-20', 75000.00),
    ('131000037',   '114456789', 'Deuda con múltiples proveedores',    '2021-08-15',450000.00),
    ('131000037',   '115567890', 'Préstamo bancario reestructurado',   '2022-03-10',440000.00);
