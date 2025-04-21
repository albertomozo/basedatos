const sqlite3 = require('sqlite3').verbose();

// Conexión a la base de datos (crea el archivo si no existe)
const db = new sqlite3.Database('estudiantes.db');

// Crear tabla si no existe
db.run(`CREATE TABLE IF NOT EXISTS estudiantes (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    edad INTEGER,
    promedio REAL
)`);

// === CRUD ===

// CREATE
function crearEstudiante(nombre, apellido, edad, promedio) {
    const sql = `INSERT INTO estudiantes (nombre, apellido, edad, promedio) VALUES (?, ?, ?, ?)`;
    db.run(sql, [nombre, apellido, edad, promedio], function(err) {
        if (err) return console.error(err.message);
        console.log(`✅ Estudiante agregado con ID: ${this.lastID}`);
    });
}

// READ
function leerEstudiantes() {
    db.all(`SELECT * FROM estudiantes`, [], (err, rows) => {
        if (err) return console.error(err.message);
        console.log("📄 Lista de estudiantes:");
        rows.forEach(row => {
            console.log(row);
        });
    });
}

// UPDATE
function actualizarEstudiante(id, nombre, apellido, edad, promedio) {
    const sql = `UPDATE estudiantes SET nombre = ?, apellido = ?, edad = ?, promedio = ? WHERE id = ?`;
    db.run(sql, [nombre, apellido, edad, promedio, id], function(err) {
        if (err) return console.error(err.message);
        console.log(`✏️ Estudiante con ID ${id} actualizado (${this.changes} cambios)`);
    });
}

// DELETE
function eliminarEstudiante(id) {
    const sql = `DELETE FROM estudiantes WHERE id = ?`;
    db.run(sql, id, function(err) {
        if (err) return console.error(err.message);
        console.log(`🗑️ Estudiante con ID ${id} eliminado (${this.changes} cambios)`);
    });
}

// === Ejemplos de uso (puedes comentar/descomentar según necesidad) ===

//crearEstudiante("Laura", "García", 22, 8.5);
//leerEstudiantes();
//actualizarEstudiante(1, "Laura", "Pérez", 23, 9.1);
//eliminarEstudiante(1);

db.close(); // cierra la conexión
