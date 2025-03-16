# Introducción Rápida a SQLite


---

## ¿Qué es SQLite?

- Sistema de gestión de bases de datos relacional
- Contenido en una pequeña biblioteca de C (aproximadamente 600KB)
- No requiere servidor - funciona integrado en la aplicación
- Autocontenido, sin configuración externa
- Base de datos completa en un único archivo

---

## Ventajas de SQLite

- **Simplicidad**: fácil de instalar, usar y mantener
- **Portabilidad**: funciona en múltiples plataformas (Windows, Linux, macOS, Android, iOS)
- **Rendimiento**: rápido para la mayoría de operaciones
- **Confiabilidad**: cumple con ACID (Atomicidad, Consistencia, Aislamiento, Durabilidad)
- **Cero configuración**: no necesita puerto, usuario ni contraseña
- **Código abierto**: licencia de dominio público

---

## Casos de uso ideales

- Aplicaciones embebidas
- Aplicaciones móviles
- Prototipos y desarrollo
- Sitios web con tráfico moderado
- Análisis de datos y educación
- Formatos de archivo y almacenamiento local

---

## Instalación de SQLite

### Windows
1. Descargar el paquete de [sqlite.org/download.html](https://sqlite.org/download.html)
2. Extraer el archivo ZIP
3. Abrir una consola y navegar a la carpeta extraída
4. Ejecutar `sqlite3` para iniciar

### Linux
```bash
sudo apt-get install sqlite3   # Ubuntu/Debian
sudo yum install sqlite        # Fedora/CentOS
```

### macOS
```bash
brew install sqlite            # Con Homebrew
```

---

## Crear y conectar a una base de datos

```bash
# Crear/conectar a una base de datos
sqlite3 mibasededatos.db

# Ver bases de datos actuales
.databases

# Ver versión de SQLite
.version

# Salir de SQLite
.exit
```

---

## Comandos básicos de SQLite

```sql
-- Crear una tabla
CREATE TABLE estudiantes (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    edad INTEGER,
    promedio REAL
);

-- Insertar datos
INSERT INTO estudiantes VALUES (1, 'Ana', 'García', 20, 8.5);
INSERT INTO estudiantes VALUES (2, 'Juan', 'Pérez', 22, 7.8);

-- Consultar datos
SELECT * FROM estudiantes;
SELECT nombre, apellido FROM estudiantes WHERE edad > 21;

-- Actualizar datos
UPDATE estudiantes SET promedio = 9.0 WHERE id = 1;

-- Eliminar datos
DELETE FROM estudiantes WHERE id = 2;
```

---

## Comandos útiles del shell de SQLite

```
.help              -- Muestra ayuda con todos los comandos
.tables            -- Lista todas las tablas
.schema            -- Muestra el esquema completo
.mode column       -- Formatea la salida en columnas
.headers on        -- Muestra los encabezados
.output archivo.txt -- Redirige la salida a un archivo
.import csv datos.csv tabla -- Importar datos desde CSV
.dump              -- Muestra el script SQL para recrear la BD
```

---

## SQLite en distintos lenguajes de programación

### Python
```python
import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('ejemplo.db')
cursor = conn.cursor()

# Crear tabla
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                (id INTEGER PRIMARY KEY, nombre TEXT, email TEXT)''')

# Insertar dato
cursor.execute("INSERT INTO usuarios VALUES (1, 'María', 'maria@ejemplo.com')")

# Guardar cambios
conn.commit()
conn.close()
```

---

### Java
```java
import java.sql.*;

public class SQLiteEjemplo {
    public static void main(String[] args) {
        try {
            Class.forName("org.sqlite.JDBC");
            Connection conn = DriverManager.getConnection("jdbc:sqlite:ejemplo.db");
            
            Statement stmt = conn.createStatement();
            stmt.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nombre TEXT)");
            
            conn.close();
        } catch (Exception e) {
            System.err.println(e.getClass().getName() + ": " + e.getMessage());
        }
    }
}
```

---

### PHP
```php
<?php
    $db = new SQLite3('ejemplo.db');
    
    $db->exec('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nombre TEXT)');
    
    $db->exec("INSERT INTO usuarios (nombre) VALUES ('Carlos')");
    
    $resultados = $db->query('SELECT * FROM usuarios');
    while ($fila = $resultados->fetchArray()) {
        echo $fila['nombre'] . "\n";
    }
?>
```

---

## Limitaciones de SQLite

- No es adecuado para aplicaciones con:
  - Alto nivel de concurrencia (muchas escrituras simultáneas)
  - Grandes volúmenes de datos (>1TB)
  - Estrictos requisitos de seguridad multinivel
  - Aplicaciones cliente-servidor complejas

---

## Tipos de datos en SQLite

SQLite utiliza **tipado dinámico** con 5 clases de almacenamiento:

1. **NULL**: valor nulo
2. **INTEGER**: enteros de hasta 64 bits
3. **REAL**: números de punto flotante
4. **TEXT**: cadenas de texto (UTF-8, UTF-16BE o UTF-16LE)
5. **BLOB**: datos binarios tal como se introdujeron

---

## Herramientas visuales para SQLite

- **DB Browser for SQLite** (multiplataforma)
- **SQLite Studio** (multiplataforma)
- **SQLiteManager** (Firefox add-on)
- **DBeaver** (multiplataforma)
- **Navicat** (comercial)

---

## Casos prácticos para clase

1. **Sistema de gestión de biblioteca**:
   - Tablas: Libros, Usuarios, Préstamos
   - Consultas: disponibilidad, vencimientos

2. **Catálogo de productos**:
   - Tablas: Productos, Categorías, Inventario
   - Consultas: productos por categoría, stock

3. **Registro de calificaciones**:
   - Tablas: Estudiantes, Cursos, Calificaciones
   - Consultas: promedio por estudiante/curso

---

## Ejercicios propuestos

1. Crear una base de datos para un blog (usuarios, entradas, comentarios)
2. Implementar consultas con JOIN entre tablas relacionadas
3. Realizar transacciones con COMMIT y ROLLBACK
4. Crear índices y analizar mejoras de rendimiento
5. Implementar disparadores (triggers) para validación de datos

---

## Recursos adicionales

- Documentación oficial: [sqlite.org/docs.html](https://sqlite.org/docs.html)
- Tutorial: [sqlitetutorial.net](https://www.sqlitetutorial.net/)
- Libro: "Using SQLite" de Jay A. Kreibich
- Repositorio de ejemplos: [github.com/mapbox/node-sqlite3/wiki/API](https://github.com/mapbox/node-sqlite3/wiki/API)
- Comunidad: [sqlite.org/forum](https://sqlite.org/forum/forum)

---

## Contacto y preguntas

¡Gracias por su atención!

[Tu información de contacto]
