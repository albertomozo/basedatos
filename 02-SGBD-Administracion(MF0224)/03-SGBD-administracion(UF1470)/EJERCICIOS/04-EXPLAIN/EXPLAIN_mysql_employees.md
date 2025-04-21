# Ejercicio SQL Complejo con EXPLAIN usando la BD employees de MySQL

**Planteamiento del ejercicio**

Vamos a crear una consulta compleja que involucre varias tablas de la base de datos `employees`, utilizando joins, agregaciones y filtros. Luego, analizaremos el plan de ejecución con `EXPLAIN` y propondremos mejoras.

**Consulta SQL compleja**

Supongamos que queremos obtener una lista de los empleados que han trabajado en más de un departamento, mostrando su nombre, la cantidad de departamentos distintos y el salario promedio que han tenido en cada uno, solo para aquellos cuyo salario promedio supera los \$60,000.

```sql
SELECT 
    e.emp_no,
    e.first_name,
    e.last_name,
    COUNT(DISTINCT de.dept_no) AS num_departments,
    AVG(s.salary) AS avg_salary
FROM 
    employees e
JOIN 
    dept_emp de ON e.emp_no = de.emp_no
JOIN 
    salaries s ON e.emp_no = s.emp_no
WHERE 
    s.to_date = '9999-01-01' -- solo salarios actuales
GROUP BY 
    e.emp_no, e.first_name, e.last_name
HAVING 
    num_departments > 1
    AND avg_salary > 60000
ORDER BY 
    avg_salary DESC;
```

Esta consulta:

- Une tres tablas: `employees`, `dept_emp` y `salaries`.
- Agrupa por empleado.
- Cuenta los departamentos distintos por los que ha pasado cada empleado.
- Calcula el salario promedio actual.
- Filtra empleados que han estado en más de un departamento y cuyo salario promedio es mayor a \$60,000.
- Ordena de mayor a menor salario promedio.

---

## Análisis con EXPLAIN

Para analizar el rendimiento y el plan de ejecución, ejecutamos:

```sql
EXPLAIN
SELECT 
    e.emp_no,
    e.first_name,
    e.last_name,
    COUNT(DISTINCT de.dept_no) AS num_departments,
    AVG(s.salary) AS avg_salary
FROM 
    employees e
JOIN 
    dept_emp de ON e.emp_no = de.emp_no
JOIN 
    salaries s ON e.emp_no = s.emp_no
WHERE 
    s.to_date = '9999-01-01'
GROUP BY 
    e.emp_no, e.first_name, e.last_name
HAVING 
    num_departments &gt; 1
    AND avg_salary &gt; 60000
ORDER BY 
    avg_salary DESC;
```

**¿Qué observar en el resultado de EXPLAIN?**

- El tipo de join (idealmente debería ser `ref` o `eq_ref`, no `ALL`).
- Si hay full table scans (tipo `ALL`) en tablas grandes, es un problema.
- El uso de índices en las columnas de join (`emp_no`, `dept_no`) y en los filtros (`to_date`).
- El número de filas estimadas a procesar por cada tabla.

---

## Propuestas de mejora

**1. Indexar columnas utilizadas en joins y filtros**

Si no existen, crear índices en:

```sql
CREATE INDEX idx_dept_emp_empno ON dept_emp(emp_no);
CREATE INDEX idx_salaries_empno_todate ON salaries(emp_no, to_date);
```

Esto ayuda a que los joins y el filtro por salario actual sean mucho más rápidos[^4][^3].

**2. Seleccionar solo las columnas necesarias**

Evitar `SELECT *` y limitar los campos seleccionados reduce el volumen de datos procesados y transferidos[^4].

**3. Filtrar lo antes posible**

Colocar el filtro `s.to_date = '9999-01-01'` directamente en el join puede ayudar al optimizador a reducir el número de registros antes de las agregaciones.

**4. Revisar el uso de subconsultas o CTEs**

Si la consulta sigue siendo lenta, se puede probar con una CTE para calcular primero los salarios actuales y luego unir con el resto de las tablas, lo que puede mejorar la legibilidad y, en algunos casos, el rendimiento[^6].

---

## Consulta optimizada con CTE

```sql
WITH current_salaries AS (
    SELECT emp_no, salary
    FROM salaries
    WHERE to_date = '9999-01-01'
)
SELECT 
    e.emp_no,
    e.first_name,
    e.last_name,
    COUNT(DISTINCT de.dept_no) AS num_departments,
    AVG(cs.salary) AS avg_salary
FROM 
    employees e
JOIN 
    dept_emp de ON e.emp_no = de.emp_no
JOIN 
    current_salaries cs ON e.emp_no = cs.emp_no
GROUP BY 
    e.emp_no, e.first_name, e.last_name
HAVING 
    num_departments &gt; 1
    AND avg_salary &gt; 60000
ORDER BY 
    avg_salary DESC;
```

---

## Resumen de buenas prácticas

- Usa índices en columnas de join y filtro.
- Selecciona solo las columnas necesarias.
- Filtra lo antes posible.
- Considera reestructurar la consulta con CTEs o subconsultas no correlacionadas.
- Analiza siempre con `EXPLAIN` antes y después de optimizar para medir mejoras[^3][^4][^6].

Este ejercicio es ideal para entender cómo analizar y mejorar consultas complejas en MySQL usando la base de datos `employees`.

<div>⁂</div>

[^1]: https://popsql.com/blog/complex-sql-queries

[^2]: https://blog.devart.com/how-to-write-complex-mysql-queries.html

[^3]: https://adictosaltrabajo.com/2016/10/24/optimizacion-de-consultas-en-mysql/

[^4]: https://www.datacamp.com/doc/mysql/mysql-optimizing-select-queries

[^5]: https://github.com/bmonroe44/MySQL-for-BI/blob/master/employee database queries.sql

[^6]: https://www.datacamp.com/es/blog/sql-query-optimization

[^7]: https://www.dataforgelabs.com/advanced-sql-concepts/complex-sql-queries

[^8]: https://www.youtube.com/watch?v=bqkUgq8hPMo

[^9]: https://www.youtube.com/watch?v=3Wz7NZalAA8

[^10]: https://www.pontia.tech/como-realizar-consultas-con-sql-10-consejos/

[^11]: https://stackoverflow.com/questions/69838134/complex-query-retrieve-employees-working-in-both-two-specific-departments

[^12]: https://www.youtube.com/watch?v=CIWKBLd3AyA

[^13]: https://www.exoscale.com/syslog/explaining-mysql-queries/

[^14]: https://learnsql.com/blog/25-advanced-sql-query-examples/

[^15]: https://www.reddit.com/r/mysql/comments/ohezl6/whats_the_proper_way_to_handle_complex_queries/

[^16]: https://www3.ntu.edu.sg/home/ehchua/programming/sql/SampleDatabases.html

[^17]: https://stackoverflow.com/questions/64255170/mysql-workplace-query

[^18]: https://dev.mysql.com/doc/en/explain.html

[^19]: https://www.sqlshack.com/es/tecnicas-de-optimizacion-de-consultas-en-sql-server-consejos-y-trucos-de-aplicacion/

[^20]: https://airbyte.com/data-engineering-resources/optimizing-mysql-queries

[^21]: https://wiki.cifprodolfoucha.es/index.php?title=Mysql_Optimización_en_el_diseño_de_BD

[^22]: https://www.youtube.com/watch?v=F4uHeqLfUB8

[^23]: https://dev.to/bilelsalemdev/advanced-sql-mastering-query-optimization-and-complex-joins-4gph

[^24]: https://creacionwebprofesional.org/mysql/consultas-avanzadas-en-mysql-con-clausulas-y-funciones-especiales/

[^25]: https://learnsql.es/blog/25-ejemplos-de-consultas-sql-avanzadas/

[^26]: https://www.thoughtspot.com/data-trends/data-modeling/optimizing-sql-queries

[^27]: https://urilynx.com/blog/sql-excellence

[^28]: https://learn.microsoft.com/es-es/sql/relational-databases/query-processing-architecture-guide?view=sql-server-ver16

[^29]: https://stackoverflow.com/questions/34821015/optimizing-a-sql-query-with-complex-filtering

[^30]: https://dev.mysql.com/doc/refman/8.1/en/select-optimization.html

[^31]: https://dev.to/tyzia/example-of-complex-sql-query-to-get-as-much-data-as-possible-from-database-9he

[^32]: https://www.w3resource.com/sql-exercises/employee-database-exercise/index.php

[^33]: https://www.linkedin.com/pulse/mysql-complex-queries-part-1-techverse-of-prasun-das-nae4c

[^34]: https://es.linkedin.com/advice/0/how-can-you-simplify-complex-sql-queries-using?lang=es\&lang=es

[^35]: https://learn.microsoft.com/es-es/sql/t-sql/queries/hints-transact-sql-query?view=sql-server-ver16

