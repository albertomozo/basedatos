-- Crear tabla principal
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    edad INTEGER
);

-- Crear tabla de logs
CREATE TABLE IF NOT EXISTS log_usuarios (
    id_log INTEGER PRIMARY KEY AUTOINCREMENT,
    operacion TEXT NOT NULL,
    id_usuario INTEGER,
    nombre TEXT,
    edad INTEGER,
    usuario_sistema TEXT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla temporal para usuario de sesión
CREATE TEMP TABLE IF NOT EXISTS session_info (
    usuario_sistema TEXT
);

-- Insertar aquí el nombre de usuario de la sesión actual
-- (puedes cambiar 'usuario_actual' por tu nombre de usuario real)
INSERT INTO session_info VALUES ('usuario_actual');

-- Trigger para INSERT
CREATE TRIGGER IF NOT EXISTS log_insert
AFTER INSERT ON usuarios
BEGIN
    INSERT INTO log_usuarios (operacion, id_usuario, nombre, edad, usuario_sistema)
    VALUES ('INSERT', NEW.id, NEW.nombre, NEW.edad, (SELECT usuario_sistema FROM session_info));
END;

-- Trigger para UPDATE
CREATE TRIGGER IF NOT EXISTS log_update
AFTER UPDATE ON usuarios
BEGIN
    INSERT INTO log_usuarios (operacion, id_usuario, nombre, edad, usuario_sistema)
    VALUES ('UPDATE', NEW.id, NEW.nombre, NEW.edad, (SELECT usuario_sistema FROM session_info));
END;

-- Trigger para DELETE
CREATE TRIGGER IF NOT EXISTS log_delete
AFTER DELETE ON usuarios
BEGIN
    INSERT INTO log_usuarios (operacion, id_usuario, nombre, edad, usuario_sistema)
    VALUES ('DELETE', OLD.id, OLD.nombre, OLD.edad, (SELECT usuario_sistema FROM session_info));
END;

-- Mensaje de confirmación
SELECT 'Tablas, triggers y sesión creados correctamente.' AS resultado;
