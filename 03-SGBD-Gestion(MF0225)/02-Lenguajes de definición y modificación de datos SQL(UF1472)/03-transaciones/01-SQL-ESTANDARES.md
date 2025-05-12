# Estándares SQL: SQL-92 y SQL-2006

## SQL-92 (también llamado SQL2)
- Fue el segundo estándar oficial de SQL, publicado en 1992 por ISO/IEC.
- Estableció las bases fundamentales del lenguaje SQL que siguen siendo relevantes hoy.
- Principales características:
  - Sintaxis JOIN explícita (INNER JOIN, LEFT JOIN, etc.)
  - Definición de esquemas y catálogos
  - Operaciones de conjuntos (UNION, INTERSECT, EXCEPT)
  - Restricciones de integridad (PRIMARY KEY, FOREIGN KEY, CHECK)
  - Transacciones con COMMIT y ROLLBACK

## SQL:2006 (ISO/IEC 9075:2006)
- Publicado en 2006, fue un estándar importante que:
  - Introdujo integración formal con XML (SQL/XML)
  - Mejoró las funciones de ventana (window functions)
  - Añadió la cláusula MERGE (operación "upsert")
  - Mejoró el soporte para objetos y tipos de datos complejos

## Estándares más modernos

1. **SQL:2008** - Añadió:
   - Instrucción TRUNCATE TABLE
   - Mejoras en las funciones de ventana
   - Soporte para ORDER BY en expresiones de agregación

2. **SQL:2011** - Introdujo:
   - Soporte para tablas temporales (temporal databases)
   - Mejoras en el manejo de fechas y horas

3. **SQL:2016** - Principales novedades:
   - Funciones JSON
   - Polimorfismo para funciones de tabla
   - Mejoras en la seguridad (row-level security)

4. **SQL:2019** (también llamado SQL:2019) - Añadió:
   - SQL multidimensional (MDA)
   - Mejor soporte para grafos en bases de datos

5. **SQL:2023** - El estándar más reciente (a mayo de 2024):
   - Mejoras continuas en JSON
   - Nuevas funciones para manejo de datos espaciales
   - Mejor soporte para machine learning directamente en SQL

Los estándares SQL siguen evolucionando para adaptarse a las nuevas necesidades de almacenamiento y procesamiento de datos, especialmente en áreas como datos semiestructurados (JSON, XML), análisis avanzado y procesamiento en tiempo real.