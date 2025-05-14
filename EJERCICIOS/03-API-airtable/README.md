# 🧩 Actividad: Carga de datos desde APIs públicas a Airtable

## 🎯 Objetivo

Extraer datos desde dos APIs públicas, convertirlos a CSV, y cargarlos a tablas en Airtable para consultarlos y analizarlos visualmente.

---

## 🌐 APIs propuestas

1. **Países del mundo**  
    [`https://restcountries.com/v3.1/all`](https://restcountries.com/v3.1/all)

2. **Universidades por país**  
    [`http://universities.hipolabs.com/search?country=Spain`](http://universities.hipolabs.com/search?country=Spain)

---

## 🔧 Herramientas necesarias

- Navegador web
- Cuenta gratuita en [Airtable.com](https://airtable.com)
- Convertidor online de JSON a CSV:  
  [https://json-csv.com/](https://json-csv.com/)  
  [https://convertcsv.com/json-to-csv.htm](https://convertcsv.com/json-to-csv.htm)

---

## 🧪 Pasos de la actividad

### 1. Crear una base en Airtable

- Iniciar sesión o crear cuenta.
- Crear una **base nueva** con dos tablas: `Países` y `Universidades`.

### 2. Obtener y convertir los datos

- Acceder a cada URL desde el navegador.
- Copiar el JSON completo y convertirlo a CSV usando un convertidor online.
- Descargar los archivos CSV.

### 3. Importar los CSV a Airtable

- En cada tabla, hacer clic en “Importar datos” (puedes subir CSV directamente).
- Airtable detectará automáticamente las columnas.

### 4. Opcional: crear relaciones

- Si usan campos como `country`, pueden crear un **campo vinculado entre tablas**.

### 5. Visualización y filtros

- Usar las vistas de Airtable para:
  - Ordenar por población.
  - Filtrar universidades por dominio.
  - Agrupar por región o continente.

---

## 🧠 Actividades complementarias o retos

- Buscar un país en concreto y listar sus universidades.
- Filtrar todos los países del continente europeo con más de 50 millones de habitantes.
- Mostrar las universidades que usen dominios `.es` o `.edu`.

---