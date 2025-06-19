# Guía de Subconsultas en SQL
## Base de datos Northwind - PostgreSQL

### ¿Qué es una subconsulta?

Una subconsulta (subquery) es una consulta SQL anidada dentro de otra consulta. Se ejecuta primero y su resultado se utiliza por la consulta externa. Las subconsultas pueden aparecer en diferentes cláusulas: SELECT, FROM, WHERE, HAVING.

---

## Tipos de Subconsultas

### 1. Subconsultas Escalares
Devuelven un único valor (una fila, una columna).

```sql
-- Ejemplo: Productos con precio mayor al promedio
SELECT product_name, unit_price
FROM products
WHERE unit_price > (
    SELECT AVG(unit_price) 
    FROM products
);
```

### 2. Subconsultas de Múltiples Filas
Devuelven múltiples filas, se usan con operadores IN, ANY, ALL, EXISTS.

```sql
-- Ejemplo: Clientes que han realizado pedidos
SELECT company_name
FROM customers
WHERE customer_id IN (
    SELECT DISTINCT customer_id 
    FROM orders
);
```

### 3. Subconsultas Correlacionadas
La subconsulta hace referencia a columnas de la consulta externa.

```sql
-- Ejemplo: Empleados con ventas superiores al promedio de su región
SELECT first_name, last_name
FROM employees e
WHERE EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.employee_id = e.employee_id
    AND o.freight > (
        SELECT AVG(freight) 
        FROM orders o2 
        WHERE o2.employee_id = e.employee_id
    )
);
```

---

## Subconsultas en la Cláusula WHERE

### Operador IN
```sql
-- Productos de categorías con más de 10 productos
SELECT product_name, category_id
FROM products
WHERE category_id IN (
    SELECT category_id
    FROM products
    GROUP BY category_id
    HAVING COUNT(*) > 10
);
```

### Operador EXISTS
```sql
-- Categorías que tienen productos descontinuados
SELECT category_name
FROM categories c
WHERE EXISTS (
    SELECT 1
    FROM products p
    WHERE p.category_id = c.category_id
    AND p.discontinued = 1
);
```

### Operadores ANY y ALL
```sql
-- Productos más caros que CUALQUIER producto de la categoría 1
SELECT product_name, unit_price
FROM products
WHERE unit_price > ANY (
    SELECT unit_price
    FROM products
    WHERE category_id = 1
);

-- Productos más caros que TODOS los productos de la categoría 1
SELECT product_name, unit_price
FROM products
WHERE unit_price > ALL (
    SELECT unit_price
    FROM products
    WHERE category_id = 1
);
```

---

## Subconsultas en la Cláusula SELECT

```sql
-- Lista de clientes con el número total de pedidos
SELECT 
    company_name,
    (SELECT COUNT(*) 
     FROM orders o 
     WHERE o.customer_id = c.customer_id) as total_orders
FROM customers c;
```

```sql
-- Productos con información de categoría
SELECT 
    product_name,
    unit_price,
    (SELECT category_name 
     FROM categories cat 
     WHERE cat.category_id = p.category_id) as category_name
FROM products p;
```

---

## Subconsultas en la Cláusula FROM

```sql
-- Promedio de ventas por empleado (usando subconsulta como tabla derivada)
SELECT 
    emp_name,
    AVG(total_sales) as avg_sales
FROM (
    SELECT 
        e.first_name || ' ' || e.last_name as emp_name,
        SUM(od.unit_price * od.quantity * (1 - od.discount)) as total_sales
    FROM employees e
    JOIN orders o ON e.employee_id = o.employee_id
    JOIN order_details od ON o.order_id = od.order_id
    GROUP BY e.employee_id, e.first_name, e.last_name
) as employee_sales
GROUP BY emp_name;
```

---

## Subconsultas con CTE (Common Table Expressions)

```sql
-- Alternativa más legible usando WITH
WITH employee_sales AS (
    SELECT 
        e.employee_id,
        e.first_name || ' ' || e.last_name as emp_name,
        SUM(od.unit_price * od.quantity * (1 - od.discount)) as total_sales
    FROM employees e
    JOIN orders o ON e.employee_id = o.employee_id
    JOIN order_details od ON o.order_id = od.order_id
    GROUP BY e.employee_id, e.first_name, e.last_name
),
avg_sales AS (
    SELECT AVG(total_sales) as company_avg
    FROM employee_sales
)
SELECT 
    emp_name,
    total_sales,
    CASE 
        WHEN total_sales > (SELECT company_avg FROM avg_sales) 
        THEN 'Por encima del promedio'
        ELSE 'Por debajo del promedio'
    END as performance
FROM employee_sales;
```

---

## Ejemplos Prácticos Avanzados

### 1. Top 3 productos más vendidos por categoría
```sql
SELECT 
    category_name,
    product_name,
    total_quantity
FROM (
    SELECT 
        c.category_name,
        p.product_name,
        SUM(od.quantity) as total_quantity,
        ROW_NUMBER() OVER (
            PARTITION BY c.category_id 
            ORDER BY SUM(od.quantity) DESC
        ) as rn
    FROM categories c
    JOIN products p ON c.category_id = p.category_id
    JOIN order_details od ON p.product_id = od.product_id
    GROUP BY c.category_id, c.category_name, p.product_id, p.product_name
) ranked
WHERE rn <= 3;
```

### 2. Clientes con pedidos en todos los años disponibles
```sql
SELECT company_name
FROM customers c
WHERE NOT EXISTS (
    SELECT DISTINCT EXTRACT(YEAR FROM order_date) as year
    FROM orders
    WHERE EXTRACT(YEAR FROM order_date) IS NOT NULL
    EXCEPT
    SELECT DISTINCT EXTRACT(YEAR FROM order_date)
    FROM orders o
    WHERE o.customer_id = c.customer_id
);
```

### 3. Productos nunca pedidos
```sql
SELECT product_name
FROM products p
WHERE NOT EXISTS (
    SELECT 1
    FROM order_details od
    WHERE od.product_id = p.product_id
);
```

---

## Optimización y Buenas Prácticas

### 1. EXISTS vs IN
```sql
-- Preferir EXISTS para mejor rendimiento
-- En lugar de:
SELECT * FROM customers 
WHERE customer_id IN (SELECT customer_id FROM orders);

-- Usar:
SELECT * FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);
```

### 2. Evitar subconsultas en SELECT cuando sea posible
```sql
-- En lugar de múltiples subconsultas en SELECT:
SELECT 
    product_name,
    (SELECT category_name FROM categories WHERE category_id = p.category_id),
    (SELECT supplier_name FROM suppliers WHERE supplier_id = p.supplier_id)
FROM products p;

-- Usar JOINs:
SELECT 
    p.product_name,
    c.category_name,
    s.company_name as supplier_name
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN suppliers s ON p.supplier_id = s.supplier_id;
```

### 3. Usar LIMIT en subconsultas cuando sea apropiado
```sql
-- Para obtener solo el primer resultado
SELECT customer_id, 
       (SELECT order_date 
        FROM orders 
        WHERE customer_id = c.customer_id 
        ORDER BY order_date DESC 
        LIMIT 1) as last_order_date
FROM customers c;
```

---

## Consejos de Rendimiento

1. **Indexación**: Asegúrate de que las columnas usadas en subconsultas estén indexadas
2. **EXISTS vs IN**: EXISTS suele ser más eficiente para grandes conjuntos de datos
3. **Evita subconsultas correlacionadas** cuando sea posible, considera usar window functions
4. **Usa EXPLAIN ANALYZE** para evaluar el plan de ejecución
5. **Considera CTEs** para mejorar la legibilidad sin sacrificar rendimiento

---

## Ejercicios Propuestos

1. Encuentra todos los productos que nunca han sido pedidos
2. Lista los empleados que han vendido más que el promedio de la empresa
3. Obtén los 3 clientes con mayor volumen de compras por país
4. Encuentra las categorías donde todos los productos están descontinuados
5. Lista los proveedores que suministran productos en más de una categoría

¡Practica estos ejemplos y experimenta con tus propias subconsultas para dominar esta poderosa herramienta de SQL!