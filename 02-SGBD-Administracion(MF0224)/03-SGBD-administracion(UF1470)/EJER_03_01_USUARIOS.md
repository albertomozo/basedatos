# Script SQL Básico para Gestión de Usuarios en MariaDB (sin procedimientos almacenados)

Aquí tienes un script SQL sencillo que tus alumnos pueden entender fácilmente, sin usar procedimientos almacenados:

```sql
-- Script para crear usuario y base de datos en MariaDB (alojamiento compartido)

-- 1. Primero definimos las variables con los datos del nuevo usuario
SET @nombre_usuario = 'usuario_prueba';
SET @contrasena = 'PasswordSeguro123!';
SET @nombre_bd = CONCAT('db_', @nombre_usuario);

-- 2. Verificamos si la base de datos ya existe
SELECT IF(COUNT(*) > 0, CONCAT('Error: La base de datos ', @nombre_bd, ' ya existe'), 'OK') AS verifica_bd
FROM information_schema.SCHEMATA 
WHERE SCHEMA_NAME = @nombre_bd;

-- 3. Verificamos si el usuario ya existe
SELECT IF(COUNT(*) > 0, CONCAT('Error: El usuario ', @nombre_usuario, ' ya existe'), 'OK') AS verifica_usuario
FROM mysql.user 
WHERE User = @nombre_usuario;

-- 4. Si todo está OK, procedemos a crear (ejecutar estas líneas solo si las verificaciones anteriores son OK)
-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS `@nombre_bd` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear el usuario (accesible desde cualquier host)
CREATE USER IF NOT EXISTS `@nombre_usuario`@`%` IDENTIFIED BY '@contrasena';

-- Otorgar todos los privilegios sobre la base de datos al usuario
GRANT ALL PRIVILEGES ON `@nombre_bd`.* TO `@nombre_usuario`@`%`;

-- Actualizar privilegios
FLUSH PRIVILEGES;

-- 5. Mostrar resultado final
SELECT CONCAT('Usuario "', @nombre_usuario, '" creado con acceso a la base de datos "', @nombre_bd, '"') AS resultado;

-- Opcional: Crear tabla para registrar usuarios (ejecutar solo una vez)
CREATE TABLE IF NOT EXISTS registro_usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL,
    base_datos VARCHAR(50) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Registrar el nuevo usuario
INSERT INTO registro_usuarios (usuario, base_datos)
VALUES (@nombre_usuario, @nombre_bd);
```

## Versión para ejecución paso a paso (recomendada para alumnos):

```sql
-- PASO 1: Definir variables
SET @nombre_usuario = 'nombre_alumno';  -- Cambiar por el nombre deseado
SET @contrasena = 'MiPassword123!';     -- Cambiar por una contraseña segura
SET @nombre_bd = CONCAT('db_', @nombre_usuario);

-- PASO 2: Verificar si la BD existe (debe mostrar "OK")
SELECT IF(COUNT(*) > 0, CONCAT('ERROR: ', @nombre_bd, ' ya existe'), 'OK') AS estado_bd
FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = @nombre_bd;

-- PASO 3: Verificar si el usuario existe (debe mostrar "OK")
SELECT IF(COUNT(*) > 0, CONCAT('ERROR: ', @nombre_usuario, ' ya existe'), 'OK') AS estado_usuario
FROM mysql.user WHERE User = @nombre_usuario;

-- PASO 4: Crear la base de datos (solo si los pasos 2 y 3 dieron "OK")
CREATE DATABASE `@nombre_bd` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- PASO 5: Crear el usuario
CREATE USER `@nombre_usuario`@`%` IDENTIFIED BY '@contrasena';

-- PASO 6: Asignar privilegios
GRANT ALL PRIVILEGES ON `@nombre_bd`.* TO `@nombre_usuario`@`%`;

-- PASO 7: Actualizar privilegios
FLUSH PRIVILEGES;

-- PASO 8: Verificar creación
SHOW DATABASES LIKE @nombre_bd;
SELECT User, Host FROM mysql.user WHERE User = @nombre_usuario;
SHOW GRANTS FOR `@nombre_usuario`@`%`;
```

## Explicación didáctica:

1. **Variables**: Usamos `@variables` para almacenar los valores y hacer el script más legible.

2. **Verificaciones**: Comprobamos si el usuario/BD existen antes de crear.

3. **Creación**:
   - `CREATE DATABASE` con juego de caracteres UTF8 (recomendado)
   - `CREATE USER` con `@%` para permitir conexión desde cualquier host
   - `GRANT ALL PRIVILEGES` para dar control total sobre la BD

4. **Seguridad**:
   - `FLUSH PRIVILEGES` actualiza los permisos
   - Las contraseñas se almacenan cifradas

5. **Registro**: Tabla opcional para llevar control de usuarios creados.

Este script es perfecto para alumnos que están comenzando, ya que:
- No requiere conocimientos avanzados
- Se puede ejecutar línea por línea
- Muestra verificaciones antes de cada acción
- Es fácil de modificar y entender