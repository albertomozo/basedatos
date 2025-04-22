const sqlite3 = require('sqlite3').verbose();
const readline = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout
});

const db = new sqlite3.Database('estudiantes.db');

db.run(`CREATE TABLE IF NOT EXISTS estudiantes (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    edad INTEGER,
    promedio REAL
)`);

// === Validación de datos ===
function validarEstudiante(estudiante) {
  const errores = [];
  
  if (typeof estudiante.nombre !== 'string' || estudiante.nombre.trim() === '') {
    errores.push('Nombre inválido');
  }
  
  if (typeof estudiante.apellido !== 'string' || estudiante.apellido.trim() === '') {
    errores.push('Apellido inválido');
  }
  
  if (!Number.isInteger(estudiante.edad) || estudiante.edad < 1) {
    errores.push('Edad debe ser un número entero positivo');
  }
  
  if (typeof estudiante.promedio !== 'number' || estudiante.promedio < 0 || estudiante.promedio > 10) {
    errores.push('Promedio debe ser un número entre 0 y 10');
  }
  
  return errores;
}

// === Funciones CRUD mejoradas ===
function crearEstudiante(estudiante) {
  const sql = `INSERT INTO estudiantes (nombre, apellido, edad, promedio) VALUES (?, ?, ?, ?)`;
  db.run(sql, [estudiante.nombre, estudiante.apellido, estudiante.edad, estudiante.promedio], function(err) {
    if (err) return console.error('❌ Error:', err.message);
    console.log(`✅ Estudiante agregado con ID: ${this.lastID}`);
    mostrarMenu();
  });
}

function leerEstudiantes() {
  db.all(`SELECT * FROM estudiantes`, [], (err, rows) => {
    if (err) return console.error('❌ Error:', err.message);
    console.log("\n📄 Lista de estudiantes:");
    console.table(rows);
    mostrarMenu();
  });
}

function actualizarEstudiante(id, estudiante) {
  db.get(`SELECT * FROM estudiantes WHERE id = ?`, [id], (err, row) => {
    if (err) return console.error('❌ Error:', err.message);
    if (!row) return console.log('⚠️ Estudiante no encontrado');
    
    const sql = `UPDATE estudiantes SET nombre = ?, apellido = ?, edad = ?, promedio = ? WHERE id = ?`;
    db.run(sql, [
      estudiante.nombre || row.nombre,
      estudiante.apellido || row.apellido,
      estudiante.edad || row.edad,
      estudiante.promedio || row.promedio,
      id
    ], function(err) {
      if (err) return console.error('❌ Error:', err.message);
      console.log(`✏️ Estudiante con ID ${id} actualizado`);
      mostrarMenu();
    });
  });
}

function eliminarEstudiante(id) {
  db.run(`DELETE FROM estudiantes WHERE id = ?`, [id], function(err) {
    if (err) return console.error('❌ Error:', err.message);
    if (this.changes === 0) return console.log('⚠️ Estudiante no encontrado');
    console.log(`🗑️ Estudiante con ID ${id} eliminado`);
    mostrarMenu();
  });
}

// === Menú interactivo ===
function mostrarMenu() {
  console.log(`
=== MENÚ PRINCIPAL ===
1. Ver todos los estudiantes
2. Agregar nuevo estudiante
3. Actualizar estudiante
4. Eliminar estudiante
5. Salir
  `);
  
  readline.question('Seleccione una opción: ', (opcion) => {
    switch(opcion) {
      case '1': leerEstudiantes(); break;
      case '2': agregarEstudiante(); break;
      case '3': actualizarMenu(); break;
      case '4': eliminarMenu(); break;
      case '5': db.close(); process.exit(); break;
      default: 
        console.log('❌ Opción inválida');
        mostrarMenu();
    }
  });
}

// === Funciones auxiliares del menú ===
function agregarEstudiante() {
  const estudiante = {};
  readline.question('Nombre: ', nombre => {
    estudiante.nombre = nombre;
    readline.question('Apellido: ', apellido => {
      estudiante.apellido = apellido;
      readline.question('Edad: ', edad => {
        estudiante.edad = parseInt(edad);
        readline.question('Promedio: ', promedio => {
          estudiante.promedio = parseFloat(promedio);
          const errores = validarEstudiante(estudiante);
          if (errores.length > 0) {
            console.log('❌ Errores:', errores.join(', '));
            mostrarMenu();
          } else {
            crearEstudiante(estudiante);
          }
        });
      });
    });
  });
}

function actualizarMenu() {
  readline.question('ID del estudiante a actualizar: ', id => {
    db.get(`SELECT * FROM estudiantes WHERE id = ?`, [id], (err, row) => {
      if (err || !row) {
        console.log('⚠️ Estudiante no encontrado');
        return mostrarMenu();
      }
      
      const estudiante = {};
      readline.question(`Nuevo nombre (actual: ${row.nombre}): `, nombre => {
        estudiante.nombre = nombre || row.nombre;
        readline.question(`Nuevo apellido (actual: ${row.apellido}): `, apellido => {
          estudiante.apellido = apellido || row.apellido;
          readline.question(`Nueva edad (actual: ${row.edad}): `, edad => {
            estudiante.edad = edad ? parseInt(edad) : row.edad;
            readline.question(`Nuevo promedio (actual: ${row.promedio}): `, promedio => {
              estudiante.promedio = promedio ? parseFloat(promedio) : row.promedio;
              const errores = validarEstudiante(estudiante);
              if (errores.length > 0) {
                console.log('❌ Errores:', errores.join(', '));
                mostrarMenu();
              } else {
                actualizarEstudiante(id, estudiante);
              }
            });
          });
        });
      });
    });
  });
}

function eliminarMenu() {
  readline.question('ID del estudiante a eliminar: ', id => {
    eliminarEstudiante(id);
  });
}

// Iniciar aplicación
mostrarMenu();
