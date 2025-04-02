# Guía de Procedimientos Almacenados en MariaDB

## Introducción

Los procedimientos almacenados son colecciones de instrucciones SQL que se almacenan en el servidor de base de datos. En MariaDB, estos procedimientos ofrecen numerosas ventajas:

- Mejora del rendimiento
- Reducción del tráfico de red
- Reutilización de código
- Mayor seguridad
- Mantenimiento simplificado

Esta guía te mostrará cómo crear, utilizar y administrar procedimientos almacenados en MariaDB.

## Requisitos Previos

- MariaDB instalado (versión 10.0 o superior)
- Acceso a una terminal o a una herramienta como phpMyAdmin, MySQL Workbench, etc.
- Permisos adecuados para crear y ejecutar procedimientos almacenados

## Sintaxis Básica

### Crear un Procedimiento Almacenado

```sql
DELIMITER //
CREATE PROCEDURE nombre_procedimiento(parámetros)
BEGIN
    -- Instrucciones SQL
END //
DELIMITER ;
```

El uso de `DELIMITER //` cambia el delimitador predeterminado (;) para que las instrucciones dentro del procedimiento no sean interpretadas como el final del comando.

### Parámetros

Los procedimientos pueden tener tres tipos de parámetros:

- `IN`: Parámetro de entrada (predeterminado)
- `OUT`: Parámetro de salida
- `INOUT`: Parámetro que funciona como entrada y salida

Ejemplo:

```sql
CREATE PROCEDURE calcular_suma(IN num1 INT, IN num2 INT, OUT resultado INT)
BEGIN
    SET resultado = num1 + num2;
END
```

## Ejemplos Prácticos

### Procedimiento Básico sin Parámetros

```sql
DELIMITER //
CREATE PROCEDURE listar_clientes()
BEGIN
    SELECT * FROM clientes ORDER BY nombre;
END //
DELIMITER ;

-- Llamar al procedimiento
CALL listar_clientes();
```

### Procedimiento con Parámetros de Entrada

```sql
DELIMITER //
CREATE PROCEDURE obtener_cliente_por_id(IN cliente_id INT)
BEGIN
    SELECT * FROM clientes WHERE id = cliente_id;
END //
DELIMITER ;

-- Llamar al procedimiento
CALL obtener_cliente_por_id(5);
```

### Procedimiento con Parámetros de Salida

```sql
DELIMITER //
CREATE PROCEDURE contar_productos(OUT total INT)
BEGIN
    SELECT COUNT(*) INTO total FROM productos;
END //
DELIMITER ;

-- Llamar al procedimiento
CALL contar_productos(@total);
SELECT @total AS total_productos;
```

### Procedimiento con Parámetros INOUT

```sql
DELIMITER //
CREATE PROCEDURE incrementar_valor(INOUT valor INT, IN incremento INT)
BEGIN
    SET valor = valor + incremento;
END //
DELIMITER ;

-- Llamar al procedimiento
SET @numero = 10;
CALL incrementar_valor(@numero, 5);
SELECT @numero AS resultado;
```

## Control de Flujo

### Condicionales IF-ELSE

```sql
DELIMITER //
CREATE PROCEDURE verificar_edad(IN edad INT, OUT mensaje VARCHAR(100))
BEGIN
    IF edad < 18 THEN
        SET mensaje = 'Menor de edad';
    ELSEIF edad <= 65 THEN
        SET mensaje = 'Adulto';
    ELSE
        SET mensaje = 'Adulto mayor';
    END IF;
END //
DELIMITER ;
```

### CASE

```sql
DELIMITER //
CREATE PROCEDURE calificar_nota(IN nota INT, OUT resultado VARCHAR(20))
BEGIN
    CASE
        WHEN nota < 60 THEN SET resultado = 'Reprobado';
        WHEN nota < 70 THEN SET resultado = 'Suficiente';
        WHEN nota < 80 THEN SET resultado = 'Bueno';
        WHEN nota < 90 THEN SET resultado = 'Muy bueno';
        ELSE SET resultado = 'Excelente';
    END CASE;
END //
DELIMITER ;
```

### Bucles

#### WHILE

```sql
DELIMITER //
CREATE PROCEDURE generar_fibonacci(IN n INT)
BEGIN
    DECLARE i INT DEFAULT 2;
    DECLARE fib1 INT DEFAULT 0;
    DECLARE fib2 INT DEFAULT 1;
    DECLARE fib INT;
    
    IF n >= 1 THEN
        SELECT 0;
    END IF;
    
    IF n >= 2 THEN
        SELECT 1;
    END IF;
    
    WHILE i < n DO
        SET fib = fib1 + fib2;
        SELECT fib;
        SET fib1 = fib2;
        SET fib2 = fib;
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;
```

#### REPEAT

```sql
DELIMITER //
CREATE PROCEDURE contar_descendente(IN inicio INT)
BEGIN
    DECLARE contador INT DEFAULT inicio;
    
    REPEAT
        SELECT contador;
        SET contador = contador - 1;
    UNTIL contador <= 0 END REPEAT;
END //
DELIMITER ;
```

#### LOOP

```sql
DELIMITER //
CREATE PROCEDURE generar_numeros(IN limite INT)
BEGIN
    DECLARE contador INT DEFAULT 1;
    
    etiqueta: LOOP
        SELECT contador;
        SET contador = contador + 1;
        IF contador > limite THEN
            LEAVE etiqueta;
        END IF;
    END LOOP etiqueta;
END //
DELIMITER ;
```

## Gestión de Errores

### Declaración DECLARE HANDLER

```sql
DELIMITER //
CREATE PROCEDURE insertar_usuario_seguro(
    IN p_nombre VARCHAR(50),
    IN p_email VARCHAR(100),
    OUT p_resultado VARCHAR(100)
)
BEGIN
    -- Declarar handler para errores
    DECLARE exit handler FOR SQLEXCEPTION
    BEGIN
        SET p_resultado = 'Error al insertar el usuario';
        ROLLBACK;
    END;
    
    -- Iniciar transacción
    START TRANSACTION;
    
    INSERT INTO usuarios(nombre, email) VALUES (p_nombre, p_email);
    
    SET p_resultado = 'Usuario insertado correctamente';
    
    COMMIT;
END //
DELIMITER ;
```

## Variables y Cursores

### Variables Locales

```sql
DELIMITER //
CREATE PROCEDURE calcular_estadisticas(OUT promedio DECIMAL(10,2), OUT total INT)
BEGIN
    DECLARE suma DECIMAL(10,2) DEFAULT 0;
    DECLARE contador INT DEFAULT 0;
    
    SELECT SUM(precio) INTO suma FROM productos;
    SELECT COUNT(*) INTO contador FROM productos;
    
    SET promedio = suma / contador;
    SET total = contador;
END //
DELIMITER ;
```

### Cursores

```sql
DELIMITER //
CREATE PROCEDURE procesar_clientes()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE cliente_id INT;
    DECLARE cliente_nombre VARCHAR(100);
    
    -- Declarar cursor
    DECLARE cliente_cursor CURSOR FOR 
        SELECT id, nombre FROM clientes;
    
    -- Declarar handler
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    -- Abrir cursor
    OPEN cliente_cursor;
    
    cliente_loop: LOOP
        FETCH cliente_cursor INTO cliente_id, cliente_nombre;
        
        IF done THEN
            LEAVE cliente_loop;
        END IF;
        
        -- Procesar cada registro
        SELECT CONCAT('Procesando cliente: ', cliente_nombre);
        
        -- Aquí iría la lógica para cada cliente
        
    END LOOP;
    
    -- Cerrar cursor
    CLOSE cliente_cursor;
END //
DELIMITER ;
```

## Administración de Procedimientos

### Listar Procedimientos

```sql
SHOW PROCEDURE STATUS WHERE Db = 'nombre_base_datos';
```

### Ver Definición de un Procedimiento

```sql
SHOW CREATE PROCEDURE nombre_procedimiento;
```

### Eliminar un Procedimiento

```sql
DROP PROCEDURE IF EXISTS nombre_procedimiento;
```

### Modificar un Procedimiento

En MariaDB no existe un comando ALTER PROCEDURE. Para modificar un procedimiento:

1. Obtén la definición actual
2. Elimina el procedimiento existente
3. Crea un nuevo procedimiento con los cambios

## Buenas Prácticas

1. **Nomenclatura consistente**: Usa prefijos como `sp_` para identificar procedimientos.
2. **Documentación**: Incluye comentarios explicando la funcionalidad.
3. **Parámetros claros**: Usa nombres descriptivos precedidos por `p_`.
4. **Manejo de errores**: Implementa handlers para gestionar excepciones.
5. **Transacciones**: Usa transacciones para mantener la integridad de los datos.
6. **Permisos**: Asigna permisos específicos para ejecutar procedimientos.
7. **Modularidad**: Divide la lógica compleja en múltiples procedimientos.

## Ventajas y Limitaciones

### Ventajas
- Mejora el rendimiento al reducir la cantidad de consultas
- Centraliza la lógica de negocio en la base de datos
- Mejora la seguridad al limitar el acceso directo a las tablas
- Reduce el tráfico de red

### Limitaciones
- Mayor complejidad en el mantenimiento
- Dependencia de la plataforma
- Dificultad para depurar procedimientos complejos

## Ejemplo Completo: Sistema de Gestión de Inventario

```sql
DELIMITER //

-- Procedimiento para agregar un producto al inventario
CREATE PROCEDURE sp_agregar_producto(
    IN p_nombre VARCHAR(100),
    IN p_descripcion TEXT,
    IN p_precio DECIMAL(10,2),
    IN p_cantidad INT,
    OUT p_id_producto INT,
    OUT p_mensaje VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SET p_mensaje = 'Error al agregar el producto';
        ROLLBACK;
    END;
    
    START TRANSACTION;
    
    INSERT INTO productos(nombre, descripcion, precio, cantidad)
    VALUES (p_nombre, p_descripcion, p_precio, p_cantidad);
    
    SET p_id_producto = LAST_INSERT_ID();
    SET p_mensaje = CONCAT('Producto agregado con ID: ', p_id_producto);
    
    -- Registrar la entrada en el historial
    INSERT INTO historial_inventario(producto_id, tipo_movimiento, cantidad, fecha)
    VALUES (p_id_producto, 'ENTRADA', p_cantidad, NOW());
    
    COMMIT;
END //

-- Procedimiento para actualizar stock
CREATE PROCEDURE sp_actualizar_stock(
    IN p_producto_id INT,
    IN p_cantidad INT,
    IN p_tipo_movimiento ENUM('ENTRADA', 'SALIDA'),
    OUT p_nuevo_stock INT,
    OUT p_mensaje VARCHAR(100)
)
BEGIN
    DECLARE stock_actual INT;
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SET p_mensaje = 'Error al actualizar el stock';
        ROLLBACK;
    END;
    
    START TRANSACTION;
    
    -- Obtener stock actual
    SELECT cantidad INTO stock_actual FROM productos 
    WHERE id = p_producto_id FOR UPDATE;
    
    IF stock_actual IS NULL THEN
        SET p_mensaje = 'Producto no encontrado';
        SET p_nuevo_stock = NULL;
        ROLLBACK;
    ELSE
        IF p_tipo_movimiento = 'ENTRADA' THEN
            SET p_nuevo_stock = stock_actual + p_cantidad;
            UPDATE productos SET cantidad = p_nuevo_stock 
            WHERE id = p_producto_id;
            
            SET p_mensaje = CONCAT('Stock incrementado. Nuevo stock: ', p_nuevo_stock);
        ELSEIF p_tipo_movimiento = 'SALIDA' THEN
            IF stock_actual >= p_cantidad THEN
                SET p_nuevo_stock = stock_actual - p_cantidad;
                UPDATE productos SET cantidad = p_nuevo_stock 
                WHERE id = p_producto_id;
                
                SET p_mensaje = CONCAT('Stock reducido. Nuevo stock: ', p_nuevo_stock);
            ELSE
                SET p_mensaje = 'Stock insuficiente para la operación';
                SET p_nuevo_stock = stock_actual;
                ROLLBACK;
            END IF;
        END IF;
        
        IF p_nuevo_stock <> stock_actual THEN
            -- Registrar en el historial
            INSERT INTO historial_inventario(producto_id, tipo_movimiento, cantidad, fecha)
            VALUES (p_producto_id, p_tipo_movimiento, p_cantidad, NOW());
            
            COMMIT;
        END IF;
    END IF;
END //

-- Procedimiento para generar informe de inventario
CREATE PROCEDURE sp_informe_inventario(IN p_nivel_critico INT)
BEGIN
    SELECT 
        p.id,
        p.nombre,
        p.descripcion,
        p.precio,
        p.cantidad,
        CASE
            WHEN p.cantidad <= p_nivel_critico THEN 'CRÍTICO'
            WHEN p.cantidad <= (p_nivel_critico * 2) THEN 'BAJO'
            WHEN p.cantidad <= (p_nivel_critico * 5) THEN 'NORMAL'
            ELSE 'ALTO'
        END AS nivel_stock,
        (SELECT COUNT(*) FROM historial_inventario 
         WHERE producto_id = p.id AND tipo_movimiento = 'SALIDA') AS total_salidas,
        (SELECT MAX(fecha) FROM historial_inventario 
         WHERE producto_id = p.id) AS ultimo_movimiento
    FROM 
        productos p
    ORDER BY 
        CASE
            WHEN p.cantidad <= p_nivel_critico THEN 1
            WHEN p.cantidad <= (p_nivel_critico * 2) THEN 2
            WHEN p.cantidad <= (p_nivel_critico * 5) THEN 3
            ELSE 4
        END,
        p.nombre;
END //

DELIMITER ;
```

## Conclusión

Los procedimientos almacenados son una herramienta poderosa en MariaDB que te permite encapsular lógica compleja directamente en el servidor de base de datos. Al dominar su creación y uso, puedes mejorar significativamente el rendimiento y la seguridad de tus aplicaciones de base de datos.

Recuerda que el diseño adecuado de los procedimientos almacenados puede simplificar enormemente el desarrollo y mantenimiento de aplicaciones que interactúan con bases de datos MariaDB.
