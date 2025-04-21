### Ejercicio Práctico en MariaDB sobre Problemas de Concurrencia y Soluciones

**Entorno de Pruebas:**

Necesitarás tener acceso a un servidor MariaDB y al menos dos sesiones de cliente.

**1. Creación de la Tabla de Prueba:**

```sql
CREATE TABLE cuentas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    saldo DECIMAL(10, 2) NOT NULL
);

INSERT INTO cuentas (nombre, saldo) VALUES ('Ana', 100.00);
INSERT INTO cuentas (nombre, saldo) VALUES ('Juan', 50.00);

SELECT * FROM cuentas;
```
### 2. Simulación del Problema de la Actualización Perdida:

**Sesión 1:**

```sql
-- Inicia la transacción
START TRANSACTION;

-- Lee el saldo de Ana
SELECT saldo FROM cuentas WHERE nombre = 'Ana';
-- (Supongamos que el resultado es 100.00)

-- Espera un momento (NO EJECUTAR AÚN EL UPDATE)
-- Deja esta sesión en espera.
```

**Sesión 2:**

```sql
-- Inicia la transacción
START TRANSACTION;

-- Lee el saldo de Ana
SELECT saldo FROM cuentas WHERE nombre = 'Ana';
-- (El resultado también será 100.00)

-- Decrementa el saldo de Ana
UPDATE cuentas SET saldo = saldo - 20.00 WHERE nombre = 'Ana';

-- Lee el saldo de Juan
SELECT saldo FROM cuentas WHERE nombre = 'Juan';
-- (Supongamos que el resultado es 50.00)

-- Incrementa el saldo de Juan
UPDATE cuentas SET saldo = saldo + 20.00 WHERE nombre = 'Juan';

-- Confirma la transacción
COMMIT;

-- Verifica los saldos
SELECT * FROM cuentas;
-- (Ana tendrá 80.00, Juan tendrá 70.00)
```

** Vuelve a la Sesión 1 y ejecuta:**

```sql
-- Decrementa el saldo de Ana (basándose en la lectura inicial de 100.00)
UPDATE cuentas SET saldo = saldo - 20.00 WHERE nombre = 'Ana';

-- Lee el saldo de Juan
SELECT saldo FROM cuentas WHERE nombre = 'Juan';
-- (El resultado será 70.00, el saldo actualizado por la Sesión 2)

-- Incrementa el saldo de Juan (basándose en la lectura inicial de 50.00)
UPDATE cuentas SET saldo = saldo + 20.00 WHERE nombre = 'Juan';

-- Confirma la transacción
COMMIT;

-- Verifica los saldos
SELECT * FROM cuentas;
-- (¡Ana tendrá 80.00, Juan tendrá 90.00! La actualización de la Sesión 2 sobre el saldo de Juan se ha perdido parcialmente desde la perspectiva de la Sesión 1)
```

** Explicación:** La Sesión 1 leyó el saldo de Ana antes de que la Sesión 2 lo modificara. Luego, la Sesión 1 intentó actualizar los saldos basándose en su lectura inicial, sobrescribiendo efectivamente la actualización realizada por la Sesión 2 sobre el saldo de Juan.

