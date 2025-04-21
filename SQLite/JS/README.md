# 📘 CRUD de Estudiantes con Node.js y SQLite

Este proyecto es una pequeña aplicación en consola desarrollada en **Node.js**, que permite realizar operaciones **CRUD** (Crear, Leer, Actualizar y Eliminar) sobre una base de datos **SQLite**, usando la tabla `estudiantes`.

---

## 🧱 Estructura de la tabla

La base de datos contiene una tabla llamada `estudiantes` con la siguiente estructura:

```sql
CREATE TABLE estudiantes (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    edad INTEGER,
    promedio REAL
);
```

---

## 📋 Requisitos

- Tener instalado **Node.js** (https://nodejs.org)
- Acceso a una terminal (Git Bash, WSL, CMD, PowerShell…)
- (Opcional) Cliente de SQLite para ver la base de datos (`sqlite3`)

---

## 🛠️ Instalación

1. Clona este repositorio o descarga los archivos:

```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo
```

2. Instala las dependencias necesarias:

```bash
npm install
```

3. Ejecuta el script para probar las operaciones CRUD:

```bash
node crud.js
```

---

## 🗂️ Archivos del proyecto

```
.
├── estudiantes.db    # Base de datos SQLite (se crea automáticamente)
├── crud.js           # Script principal con funciones CRUD
└── package.json      # Configuración del proyecto Node.js
```

---

## 🔧 Contenido de `crud.js`

El archivo `crud.js` contiene las siguientes funciones:

- `crearEstudiante(nombre, apellido, edad, promedio)`  
- `leerEstudiantes()`  
- `actualizarEstudiante(id, nombre, apellido, edad, promedio)`  
- `eliminarEstudiante(id)`

Ejemplo de uso:

```javascript
//crearEstudiante("Laura", "García", 22, 8.5);
//leerEstudiantes();
//actualizarEstudiante(1, "Laura", "Pérez", 23, 9.1);
//eliminarEstudiante(1);
```

Descomenta las funciones que quieras ejecutar y vuelve a correr el script con `node crud.js`.

---

## 🚀 Próximos pasos

- Crear una **API REST** usando Express.js
- Añadir una **interfaz web** en HTML/JS
- Mejorar el manejo de errores y validaciones
- Añadir un sistema de logs o persistencia de cambios

---

## 🧑‍💻 Autor

Proyecto creado por [Tu Nombre](https://github.com/tu-usuario)  
¡Contribuciones, forks y estrellas ⭐ son bienvenidos!

---

## 📜 Licencia

Este proyecto está bajo licencia MIT. Puedes usarlo libremente para aprender o construir tu propio CRUD.

```




