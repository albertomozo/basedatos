-- =====================================================
-- EJEMPLOS DE TRANSACCIONES Y DEADLOCK EN NORTHWIND
-- =====================================================

-- CONFIGURACIÓN INICIAL PARA TESTING
-- Ajustar timeout de deadlock para testing más rápido
SET deadlock_timeout = '1s';

-- =====================================================
-- EJEMPLO 1: DEADLOCK CLÁSICO - ORDEN DIFERENTE DE LOCKS
-- =====================================================

-- TRANSACCIÓN A (ejecutar en sesión/terminal 1)
-- Simula: Actualizar stock de un producto y luego procesar una orden
/*
BEGIN;

-- Paso 1: Bloquear producto con ID 1
UPDATE products 
SET units_in_stock = units_in_stock - 5 
WHERE product_id = 1;

-- Simular trabajo...
SELECT pg_sleep(2);

-- Paso 2: Intentar bloquear producto con ID 2
UPDATE products 
SET units_in_stock = units_in_stock - 3 
WHERE product_id = 2;

COMMIT;
*/

-- TRANSACCIÓN B (ejecutar SIMULTÁNEAMENTE en sesión/terminal 2)
-- Simula: Actualizar stock en orden inverso
/*
BEGIN;

-- Paso 1: Bloquear producto con ID 2
UPDATE products 
SET units_in_stock = units_in_stock - 2 
WHERE product_id = 2;

-- Simular trabajo...
SELECT pg_sleep(2);

-- Paso 2: Intentar bloquear producto con ID 1
UPDATE products 
SET units_in_stock = units_in_stock - 4 
WHERE product_id = 1;

COMMIT;
*/

-- =====================================================
-- EJEMPLO 2: DEADLOCK EN PROCESAMIENTO DE ÓRDENES
-- =====================================================

-- TRANSACCIÓN A: Procesar orden 10248
-- (ejecutar en sesión 1)
/*
BEGIN;

-- 1. Bloquear la orden
UPDATE orders 
SET freight = freight + 5.00 
WHERE order_id = 10248;

SELECT pg_sleep(1);

-- 2. Actualizar detalles de orden 10249
UPDATE order_details 
SET discount = 0.05 
WHERE order_id = 10249 AND product_id = 11;

COMMIT;
*/

-- TRANSACCIÓN B: Procesar orden 10249
-- (ejecutar SIMULTÁNEAMENTE en sesión 2)
/*
BEGIN;

-- 1. Bloquear la orden 10249
UPDATE orders 
SET freight = freight + 3.00 
WHERE order_id = 10249;

SELECT pg_sleep(1);

-- 2. Intentar actualizar detalles de orden 10248
UPDATE order_details 
SET discount = 0.03 
WHERE order_id = 10248 AND product_id = 14;

COMMIT;
*/

-- =====================================================
-- EJEMPLO 3: DEADLOCK CON CLIENTES Y ÓRDENES
-- =====================================================

-- TRANSACCIÓN A: Actualizar cliente y sus órdenes
-- (ejecutar en sesión 1)
/*
BEGIN;

-- 1. Bloquear cliente ALFKI
UPDATE customers 
SET contact_name = 'María Anders Updated' 
WHERE customer_id = 'ALFKI';

SELECT pg_sleep(1);

-- 2. Intentar actualizar cliente ANATR
UPDATE customers 
SET contact_name = 'Ana Trujillo Updated' 
WHERE customer_id = 'ANATR';

COMMIT;
*/

-- TRANSACCIÓN B: Actualizar en orden inverso
-- (ejecutar SIMULTÁNEAMENTE en sesión 2)
/*
BEGIN;

-- 1. Bloquear cliente ANATR
UPDATE customers 
SET city = 'México D.F. Updated' 
WHERE customer_id = 'ANATR';

SELECT pg_sleep(1);

-- 2. Intentar actualizar cliente ALFKI
UPDATE customers 
SET city = 'Berlin Updated' 
WHERE customer_id = 'ALFKI';

COMMIT;
*/

-- =====================================================
-- EJEMPLO 4: DEADLOCK MÁS COMPLEJO - INVENTORY Y ORDERS
-- =====================================================

-- Función para simular procesamiento de orden compleja
CREATE OR REPLACE FUNCTION procesar_orden_compleja(
    p_order_id INTEGER,
    p_product_id1 INTEGER,
    p_product_id2 INTEGER,
    p_cantidad1 INTEGER,
    p_cantidad2 INTEGER
) RETURNS VOID AS $$
BEGIN
    -- Actualizar primer producto
    UPDATE products 
    SET units_in_stock = units_in_stock - p_cantidad1
    WHERE product_id = p_product_id1;
    
    -- Simular procesamiento
    PERFORM pg_sleep(1);
    
    -- Actualizar segundo producto
    UPDATE products 
    SET units_in_stock = units_in_stock - p_cantidad2
    WHERE product_id = p_product_id2;
    
    -- Actualizar orden
    UPDATE orders 
    SET shipped_date = CURRENT_DATE 
    WHERE order_id = p_order_id;
    
END;
$$ LANGUAGE plpgsql;

-- TRANSACCIÓN A: Procesar orden con productos 1 y 2
-- (ejecutar en sesión 1)
/*
BEGIN;
SELECT procesar_orden_compleja(10248, 1, 2, 5, 3);
COMMIT;
*/

-- TRANSACCIÓN B: Procesar orden con productos 2 y 1 (orden inverso)
-- (ejecutar SIMULTÁNEAMENTE en sesión 2)
/*
BEGIN;
SELECT procesar_orden_compleja(10249, 2, 1, 4, 6);
COMMIT;
*/

-- =====================================================
-- SCRIPT PARA MONITOREAR LOCKS Y DEADLOCKS
-- =====================================================

-- Ver locks actuales
CREATE OR REPLACE VIEW vw_locks_actuales AS
SELECT 
    pg_class.relname as tabla,
    pg_locks.locktype,
    pg_locks.mode,
    pg_locks.granted,
    pg_stat_activity.query,
    pg_stat_activity.pid,
    pg_stat_activity.state
FROM pg_locks
LEFT JOIN pg_class ON pg_locks.relation = pg_class.oid
LEFT JOIN pg_stat_activity ON pg_locks.pid = pg_stat_activity.pid
WHERE pg_class.relname IN ('products', 'orders', 'order_details', 'customers')
ORDER BY pg_class.relname, pg_locks.granted;

-- Consultar locks actuales
-- SELECT * FROM vw_locks_actuales;

-- Ver procesos bloqueados
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS blocking_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks 
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;

-- =====================================================
-- HERRAMIENTAS PARA DEBUG DE DEADLOCKS
-- =====================================================

-- Verificar configuración de deadlock detection
SHOW deadlock_timeout;
SHOW log_lock_waits;

-- Para activar logging de locks (ejecutar como superuser)
-- ALTER SYSTEM SET log_lock_waits = ON;
-- ALTER SYSTEM SET deadlock_timeout = '1s';
-- SELECT pg_reload_conf();

-- Ver estadísticas de deadlocks
SELECT 
    datname,
    deadlocks
FROM pg_stat_database 
WHERE datname = current_database();

-- =====================================================
-- INSTRUCCIONES PARA REPRODUCIR DEADLOCK
-- =====================================================

/*
PASOS PARA GENERAR DEADLOCK:

1. Abrir DOS sesiones/terminales de PostgreSQL
2. En ambas conectarse a la BD Northwind
3. Ejecutar las transacciones marcadas como A y B SIMULTÁNEAMENTE
4. Observar que una transacción será cancelada por deadlock

EJEMPLO RÁPIDO:

SESIÓN 1:
BEGIN;
UPDATE products SET units_in_stock = units_in_stock - 1 WHERE product_id = 1;
-- ESPERAR 3 segundos, luego ejecutar:
UPDATE products SET units_in_stock = units_in_stock - 1 WHERE product_id = 2;
COMMIT;

SESIÓN 2 (ejecutar INMEDIATAMENTE después del primer UPDATE de sesión 1):
BEGIN;
UPDATE products SET units_in_stock = units_in_stock - 1 WHERE product_id = 2;
-- ESPERAR 3 segundos, luego ejecutar:
UPDATE products SET units_in_stock = units_in_stock - 1 WHERE product_id = 1;
COMMIT;

RESULTADO: Una de las dos transacciones fallará con error de deadlock.
*/

-- =====================================================
-- MEJORES PRÁCTICAS PARA EVITAR DEADLOCKS
-- =====================================================

-- 1. ACCEDER A RECURSOS EN ORDEN CONSISTENTE
-- MAL:
/*
-- Transacción A: productos 1, luego 2
-- Transacción B: productos 2, luego 1
*/

-- BIEN:
-- Ambas transacciones: productos en orden 1, luego 2
BEGIN;
UPDATE products SET units_in_stock = units_in_stock - 1 
WHERE product_id IN (1, 2) 
ORDER BY product_id;  -- Orden consistente
COMMIT;

-- 2. USAR TIMEOUTS APROPIADOS
SET statement_timeout = '30s';
SET lock_timeout = '10s';

-- 3. MINIMIZAR DURACIÓN DE TRANSACCIONES
-- Hacer trabajo pesado FUERA de la transacción
-- Solo bloquear cuando sea necesario

-- 4. USAR NIVELES DE AISLAMIENTO APROPIADOS
BEGIN ISOLATION LEVEL READ COMMITTED;
-- operaciones...
COMMIT;