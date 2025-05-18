# Ejercicios SQL Progresivos para PostgreSQL con Northwind

Estos ejercicios están diseñados para practicar y profundizar en SQL usando la base de datos Northwind en PostgreSQL. Se agrupan en bloques temáticos y van aumentando en dificultad.

---

## PARTE 1: Consultas Básicas y Joins

**Ejercicio 1:**  
Mostrar todos los productos con su nombre, precio unitario y unidades en stock.
```sql
SELECT product_name, unit_price, units_in_stock
FROM products
ORDER BY unit_price DESC;
```

**Ejercicio 2:**  
Mostrar los productos y sus categorías.
```sql
SELECT p.product_id, p.product_name, c.category_name
FROM products p
JOIN categories c ON p.category_id = c.category_id
ORDER BY c.category_name, p.product_name;
```

**Ejercicio 3:**  
Mostrar los pedidos con información del cliente y empleado.
```sql
SELECT o.order_id, 
    c.company_name AS cliente, 
    CONCAT(e.first_name, ' ', e.last_name) AS empleado,
    o.order_date
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN employees e ON o.employee_id = e.employee_id
ORDER BY o.order_date DESC
LIMIT 20;
```

**Ejercicio 4:**  
Encontrar proveedores que no suministran ningún producto actualmente.
```sql
SELECT s.supplier_id, s.company_name, COUNT(p.product_id) AS numero_productos
FROM suppliers s
LEFT JOIN products p ON s.supplier_id = p.supplier_id
GROUP BY s.supplier_id, s.company_name
ORDER BY numero_productos;
```

---

## PARTE 2: Group By y Having

**Ejercicio 5:**  
Número de productos por categoría.
```sql
SELECT c.category_name, COUNT(p.product_id) AS numero_productos
FROM categories c
JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_name
ORDER BY numero_productos DESC;
```

**Ejercicio 6:**  
Ventas totales por producto (cantidad * precio).
```sql
SELECT p.product_name, 
    SUM(od.quantity * od.unit_price) AS ventas_totales
FROM products p
JOIN order_details od ON p.product_id = od.product_id
GROUP BY p.product_name
ORDER BY ventas_totales DESC
LIMIT 10;
```

**Ejercicio 7:**  
Ventas totales por categoría y país del cliente.
```sql
SELECT c.category_name, 
    cu.country, 
    SUM(od.quantity * od.unit_price) AS ventas_totales
FROM categories c
JOIN products p ON c.category_id = p.category_id
JOIN order_details od ON p.product_id = od.product_id
JOIN orders o ON od.order_id = o.order_id
JOIN customers cu ON o.customer_id = cu.customer_id
GROUP BY c.category_name, cu.country
ORDER BY c.category_name, ventas_totales DESC;
```

**Ejercicio 8:**  
Categorías con más de 10 productos.
```sql
SELECT c.category_name, COUNT(p.product_id) AS numero_productos
FROM categories c
JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_name
HAVING COUNT(p.product_id) > 10
ORDER BY numero_productos DESC;
```

**Ejercicio 9:**  
Clientes que han gastado más de $10000 en total.
```sql
SELECT c.company_name, 
    c.country,
    SUM(od.quantity * od.unit_price) AS total_compras
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_details od ON o.order_id = od.order_id
GROUP BY c.company_name, c.country
HAVING SUM(od.quantity * od.unit_price) > 10000
ORDER BY total_compras DESC;
```

---

## PARTE 3: Union y Operaciones de Conjuntos

**Ejercicio 10:**  
Lista combinada de ciudades de clientes y proveedores.
```sql
SELECT city, country, 'Cliente' AS tipo
FROM customers
UNION
SELECT city, country, 'Proveedor' AS tipo
FROM suppliers
ORDER BY country, city;
```

**Ejercicio 11:**  
Comparar resultados con y sin duplicados.
```sql
SELECT country FROM customers
UNION
SELECT country FROM suppliers
ORDER BY country;

SELECT country FROM customers
UNION ALL
SELECT country FROM suppliers
ORDER BY country;
```

**Ejercicio 12:**  
Ciudades donde hay tanto clientes como proveedores.
```sql
SELECT city, country FROM customers
INTERSECT
SELECT city, country FROM suppliers
ORDER BY country, city;
```

**Ejercicio 13:**  
Ciudades donde hay clientes pero no proveedores.
```sql
SELECT city, country FROM customers
EXCEPT
SELECT city, country FROM suppliers
ORDER BY country, city;
```

---

## PARTE 4: Vistas

**Ejercicio 14:**  
Creación de una vista simple.
```sql
CREATE OR REPLACE VIEW vw_productos_por_categoria AS
SELECT c.category_name, 
    p.product_name, 
    p.unit_price, 
    p.units_in_stock
FROM categories c
JOIN products p ON c.category_id = p.category_id
ORDER BY c.category_name, p.product_name;

-- Consultar la vista
SELECT * FROM vw_productos_por_categoria;
```

**Ejercicio 15:**  
Vista con agregaciones.
```sql
CREATE OR REPLACE VIEW vw_ventas_por_categoria AS
SELECT c.category_name, 
    SUM(od.quantity * od.unit_price) AS ventas_totales,
    COUNT(DISTINCT o.order_id) AS numero_pedidos
FROM categories c
JOIN products p ON c.category_id = p.category_id
JOIN order_details od ON p.product_id = od.product_id
JOIN orders o ON od.order_id = o.order_id
GROUP BY c.category_name
ORDER BY ventas_totales DESC;

-- Consultar la vista
SELECT * FROM vw_ventas_por_categoria;
```

**Ejercicio 16:**  
Vista compleja para análisis de ventas.
```sql
CREATE OR REPLACE VIEW vw_analisis_ventas AS
SELECT 
    EXTRACT(YEAR FROM o.order_date) AS año,
    EXTRACT(MONTH FROM o.order_date) AS mes,
    c.category_name,
    p.product_name,
    SUM(od.quantity) AS unidades_vendidas,
    SUM(od.quantity * od.unit_price) AS ventas_totales,
    SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ventas_con_descuento
FROM orders o
JOIN order_details od ON o.order_id = od.order_id
JOIN products p ON od.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
GROUP BY EXTRACT(YEAR FROM o.order_date), EXTRACT(MONTH FROM o.order_date), 
      c.category_name, p.product_name
ORDER BY año, mes, ventas_totales DESC;

-- Consultar la vista
SELECT * FROM vw_analisis_ventas WHERE año = 1997 AND mes = 7 LIMIT 10;
```

**Ejercicio 17:**  
Vista materializada para mejor rendimiento.
```sql
CREATE MATERIALIZED VIEW mv_resumen_ventas_mensual AS
SELECT 
    EXTRACT(YEAR FROM o.order_date) AS año,
    EXTRACT(MONTH FROM o.order_date) AS mes,
    c.category_name,
    SUM(od.quantity * od.unit_price) AS ventas_totales,
    COUNT(DISTINCT o.customer_id) AS numero_clientes
FROM orders o
JOIN order_details od ON o.order_id = od.order_id
JOIN products p ON od.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
GROUP BY EXTRACT(YEAR FROM o.order_date), EXTRACT(MONTH FROM o.order_date), c.category_name
ORDER BY año, mes, category_name;

-- Consultar la vista materializada
SELECT * FROM mv_resumen_ventas_mensual ORDER BY año DESC, mes DESC;

-- Refrescar la vista materializada
REFRESH MATERIALIZED VIEW mv_resumen_ventas_mensual;
```

---

## PARTE 5: Ejercicios Acumulativos Complejos

**Ejercicio 18:**  
Crear vista para análisis de rendimiento de los empleados.
```sql
CREATE OR REPLACE VIEW vw_rendimiento_empleados AS
WITH ventas_por_empleado AS (
    SELECT 
     e.employee_id,
     CONCAT(e.first_name, ' ', e.last_name) AS nombre_empleado,
     EXTRACT(YEAR FROM o.order_date) AS año,
     EXTRACT(MONTH FROM o.order_date) AS mes,
     COUNT(DISTINCT o.order_id) AS num_pedidos,
     SUM(od.quantity * od.unit_price) AS ventas_totales
    FROM employees e
    JOIN orders o ON e.employee_id = o.employee_id
    JOIN order_details od ON o.order_id = od.order_id
    GROUP BY e.employee_id, nombre_empleado, año, mes
)
SELECT 
    vpe.*,
    ROUND(AVG(ventas_totales) OVER (PARTITION BY año, mes), 2) AS promedio_ventas_mes,
    ROUND(ventas_totales / AVG(ventas_totales) OVER (PARTITION BY año, mes) * 100, 2) AS porcentaje_sobre_promedio
FROM ventas_por_empleado vpe
ORDER BY año, mes, ventas_totales DESC;

-- Consultar la vista
SELECT * FROM vw_rendimiento_empleados WHERE año = 1997 LIMIT 20;
```

**Ejercicio 19:**  
Combinación de UNION, JOIN y GROUP BY para reporte completo.
```sql
WITH ventas_trimestre AS (
    SELECT 
     EXTRACT(YEAR FROM o.order_date) AS año,
     CASE 
         WHEN EXTRACT(MONTH FROM o.order_date) BETWEEN 1 AND 3 THEN 1
         WHEN EXTRACT(MONTH FROM o.order_date) BETWEEN 4 AND 6 THEN 2
         WHEN EXTRACT(MONTH FROM o.order_date) BETWEEN 7 AND 9 THEN 3
         ELSE 4
     END AS trimestre,
     'Trimestre' AS periodo_tipo,
     p.product_id,
     p.product_name,
     c.category_name,
     SUM(od.quantity) AS unidades_vendidas,
     SUM(od.quantity * od.unit_price) AS ventas_totales
    FROM orders o
    JOIN order_details od ON o.order_id = od.order_id
    JOIN products p ON od.product_id = p.product_id
    JOIN categories c ON p.category_id = c.category_id
    GROUP BY año, trimestre, p.product_id, p.product_name, c.category_name
),
ventas_semestre AS (
    SELECT 
     EXTRACT(YEAR FROM o.order_date) AS año,
     CASE 
         WHEN EXTRACT(MONTH FROM o.order_date) BETWEEN 1 AND 6 THEN 1
         ELSE 2
     END AS semestre,
     'Semestre' AS periodo_tipo,
     p.product_id,
     p.product_name,
     c.category_name,
     SUM(od.quantity) AS unidades_vendidas,
     SUM(od.quantity * od.unit_price) AS ventas_totales
    FROM orders o
    JOIN order_details od ON o.order_id = od.order_id
    JOIN products p ON od.product_id = p.product_id
    JOIN categories c ON p.category_id = c.category_id
    GROUP BY año, semestre, p.product_id, p.product_name, c.category_name
)
SELECT * FROM ventas_trimestre
UNION ALL
SELECT * FROM ventas_semestre
ORDER BY año, periodo_tipo, trimestre, ventas_totales DESC;
```

**Ejercicio 20:**  
Vista de análisis de rentabilidad por cliente y categoría.
```sql
CREATE OR REPLACE VIEW vw_rentabilidad_cliente_categoria AS
WITH rentabilidad AS (
    SELECT 
     c.customer_id,
     c.company_name,
     cat.category_id,
     cat.category_name,
     SUM(od.quantity * od.unit_price * (1 - od.discount)) AS ventas_netas,
     COUNT(DISTINCT o.order_id) AS num_pedidos,
     SUM(od.quantity) AS unidades_totales
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_details od ON o.order_id = od.order_id
    JOIN products p ON od.product_id = p.product_id
    JOIN categories cat ON p.category_id = cat.category_id
    GROUP BY c.customer_id, c.company_name, cat.category_id, cat.category_name
)
SELECT
    r.*,
    ROUND(ventas_netas / num_pedidos, 2) AS valor_promedio_pedido,
    ROUND(ventas_netas / unidades_totales, 2) AS valor_promedio_unidad,
    RANK() OVER (PARTITION BY category_id ORDER BY ventas_netas DESC) AS ranking_categoria,
    PERCENT_RANK() OVER (PARTITION BY category_id ORDER BY ventas_netas) AS percentil_categoria
FROM rentabilidad r
ORDER BY category_name, ventas_netas DESC;

-- Consultar la vista
SELECT * FROM vw_rentabilidad_cliente_categoria LIMIT 20;
```

---

### Ejemplo de uso combinado de vistas para análisis completo

```sql
SELECT 
    vac.año, 
    vac.mes, 
    vac.category_name, 
    SUM(vac.ventas_totales) AS ventas_categoria,
    ROUND(AVG(vre.porcentaje_sobre_promedio), 2) AS promedio_rendimiento_empleados
FROM vw_analisis_ventas vac
JOIN vw_rendimiento_empleados vre ON vac.año = vre.año AND vac.mes = vre.mes
GROUP BY vac.año, vac.mes, vac.category_name
ORDER BY vac.año, vac.mes, ventas_categoria DESC
LIMIT 20;
```

---