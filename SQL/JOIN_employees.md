<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

## Guía para Entender las JOIN en SQL con Ejemplos en la BD `employees` de MySQL

Las cláusulas JOIN en SQL permiten combinar datos de dos o más tablas relacionadas, devolviendo información más completa y útil en una sola consulta. A continuación, te explico los tipos principales de JOIN y cómo usarlos con ejemplos prácticos basados en la base de datos `employees` de MySQL.

---

**Tipos de JOIN más comunes en MySQL**


| JOIN | Qué hace |
| :-- | :-- |
| INNER JOIN | Devuelve solo las filas que tienen coincidencia en ambas tablas |
| LEFT JOIN | Devuelve todas las filas de la tabla izquierda y las coincidencias de la tabla derecha |
| RIGHT JOIN | Devuelve todas las filas de la tabla derecha y las coincidencias de la tabla izquierda |
| CROSS JOIN | Devuelve el producto cartesiano de ambas tablas |
| SELF JOIN | Une una tabla consigo misma, útil para jerarquías (como empleados y sus managers) |


---

## **1. INNER JOIN**

Devuelve solo las filas donde hay coincidencia en ambas tablas.

**Ejemplo: Mostrar empleados y el nombre de su departamento**

```sql
SELECT e.first_name, e.last_name, d.dept_name
FROM employees e
INNER JOIN dept_emp de ON e.emp_no = de.emp_no
INNER JOIN departments d ON de.dept_no = d.dept_no;
```

Este ejemplo une las tablas `employees`, `dept_emp` y `departments` para mostrar el nombre y apellido de cada empleado junto con el nombre de su departamento[^3][^5].

---

## **2. LEFT JOIN**

Devuelve todos los registros de la tabla izquierda y los que coinciden de la derecha. Si no hay coincidencia, los campos de la derecha serán NULL.

**Ejemplo: Mostrar todos los empleados y, si tienen, su departamento actual**

```sql
SELECT e.first_name, e.last_name, d.dept_name
FROM employees e
LEFT JOIN dept_emp de ON e.emp_no = de.emp_no
LEFT JOIN departments d ON de.dept_no = d.dept_no
AND de.to_date = '9999-01-01';
```

Aquí se muestran todos los empleados, aunque algunos no tengan un departamento asignado actualmente (el campo dept_name será NULL)[^5][^6].

---

## **3. RIGHT JOIN**

Devuelve todos los registros de la tabla derecha y los que coinciden de la izquierda.

**Ejemplo: Mostrar todos los departamentos y los empleados asignados**

```sql
SELECT d.dept_name, e.first_name, e.last_name
FROM departments d
RIGHT JOIN dept_emp de ON d.dept_no = de.dept_no
RIGHT JOIN employees e ON de.emp_no = e.emp_no;
```

Así puedes ver todos los departamentos aunque no tengan empleados asignados actualmente (los campos de empleados serán NULL)[^5].

---

## **4. SELF JOIN**

Une una tabla consigo misma. Muy útil para jerarquías, como empleados y sus managers.

**Ejemplo: Mostrar empleados junto a su manager**

```sql
SELECT 
  e.emp_no AS Emp_Id,
  e.last_name AS Employee,
  m.emp_no AS Mgr_Id,
  m.last_name AS Manager
FROM employees e
JOIN employees m ON e.manager_id = m.emp_no;
```

En este caso, la tabla `employees` se usa dos veces (con alias `e` y `m`) para mostrar cada empleado junto a su manager[^2][^5].

---

## **5. CROSS JOIN**

Devuelve todas las combinaciones posibles entre ambas tablas (producto cartesiano).

**Ejemplo: Combinaciones de todos los empleados con todos los departamentos**

```sql
SELECT e.first_name, d.dept_name
FROM employees e
CROSS JOIN departments d;
```

Este JOIN no suele usarse salvo en casos muy específicos, ya que puede generar muchos resultados[^5].

---

## **Resumen Visual**

| Tipo de JOIN | ¿Incluye filas sin coincidencia? | Tabla principal | Tabla secundaria | Uso típico |
| :-- | :-- | :-- | :-- | :-- |
| INNER JOIN | No | Ambas | Ambas | Relacionar datos estrictamente vinculados |
| LEFT JOIN | Sí (izquierda) | Izquierda | Derecha | Mostrar todo de la izquierda, coincida o no |
| RIGHT JOIN | Sí (derecha) | Derecha | Izquierda | Mostrar todo de la derecha, coincida o no |
| CROSS JOIN | N/A (todas las combinaciones) | Ambas | Ambas | Casos especiales, combinaciones completas |
| SELF JOIN | Depende del tipo de JOIN usado | Mismo tabla | Mismo tabla | Jerarquías o relaciones dentro de la misma tabla |


---

## **Consejos Prácticos**

- Usa INNER JOIN para obtener solo datos que tengan relación en ambas tablas.
- Usa LEFT JOIN si te interesa mostrar todos los registros de la tabla principal, aunque no tengan coincidencia.
- Usa SELF JOIN para relaciones jerárquicas (como empleado-manager).
- Practica combinando varias tablas usando JOIN para consultas más complejas[^4][^5].

---


<div style="text-align: center">⁂</div>

[^1]: https://www.w3schools.com/mysql/mysql_join.asp

[^2]: https://www.w3resource.com/mysql-exercises/join-exercises/write-a-query-to-find-the-employee-id-name-along-with-their-manager_id-manager-name.php

[^3]: https://www.datacamp.com/doc/mysql/mysql-inner-join

[^4]: https://labex.io/tutorials/sql-database-joins-for-personnel-data-301348

[^5]: https://ultahost.com/knowledge-base/mysql-joins-examples/

[^6]: https://www.linkedin.com/pulse/step-guide-sql-joins-made-easy--xvwlf

[^7]: https://onecompiler.com/mysql/3xdds2hs2

[^8]: https://datalemur.com/sql-tutorial/sql-joins-inner-outer-left-right

[^9]: https://www.youtube.com/watch?v=lXQzD09BOH0

[^10]: https://www.w3resource.com/mysql-exercises/join-exercises/write-a-query-to-get-the-department-name-and-number-of-employees-in-the-department.php

