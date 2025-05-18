# **Proyecto de Prácticas SQL Avanzado con PostgreSQL y Northwind**

`README.md` - Guía paso a paso para configurar el entorno y realizar ejercicios prácticos.

---

## **📌 Tabla de Contenidos**
1. [Requisitos Previos](#-requisitos-previos)
2. [Instalación de PostgreSQL](#-instalación-de-postgresql)
3. [Configuración de la Base de Datos Northwind](#-configuración-de-la-base-de-datos-northwind)
4. [Ejercicios Prácticos](#-ejercicios-prácticos)
   - [1. Análisis de Estructuras](#1-análisis-de-estructuras)
   - [2. Lenguaje de Definición y Manipulación (DDL/DML)](#2-lenguaje-de-definición-y-manipulación-ddl-dml)
   - [3. Transacciones y Concurrencia](#3-transacciones-y-concurrencia)
5. [Recursos Adicionales](#-recursos-adicionales)

---

## **🔧 Requisitos Previos**
- **PostgreSQL** instalado (versión 12+ recomendada).
- **Git** (para clonar el repositorio de Northwind).
- **psql** (CLI de PostgreSQL) o **PgAdmin** (GUI opcional).

---

## **🐘 Instalación de PostgreSQL**
### **En Linux (Ubuntu/Debian)**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### **En Windows/macOS**
- Descargar instalador oficial: [https://www.postgresql.org/download/](https://www.postgresql.org/download/)

### **Verificar instalación**
```bash
psql --version
```

---

## **📂 Configuración de la Base de Datos Northwind**
1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/pthom/northwind_psql.git
   cd northwind_psql
   ```

2. **Crear la base de datos**:
   ```bash
   createdb northwind
   ```

3. **Importar datos**:
   ```bash
   psql -d northwind -f northwind.sql
   ```

4. **Verificar tablas**:
   ```bash
   psql -d northwind -c "\dt"
   ```

---

## **💻 Ejercicios Prácticos**

### **1. Análisis de Estructuras**
#### **📌 Objetivo**: Familiarizarse con las tablas, relaciones y tipos de datos.
```sql
-- 1.1 Listar todas las tablas y sus columnas
\dt
\d+ orders

-- 1.2 Consultar relaciones entre tablas (ejemplo: pedidos y clientes)
SELECT 
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table,
    ccu.column_name AS foreign_column
FROM 
    information_schema.table_constraints tc
JOIN 
    information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
JOIN 
    information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
WHERE 
    tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = 'orders';
```

---

### **2. Lenguaje de Definición y Manipulación (DDL/DML)**
#### **📌 Objetivo**: Practicar consultas avanzadas, modificaciones de esquema y optimización.
```sql
-- 2.1 Crear una nueva tabla "supplier_audit"
CREATE TABLE supplier_audit (
    id SERIAL PRIMARY KEY,
    supplier_id INT REFERENCES suppliers(supplier_id),
    old_company_name VARCHAR(100),
    new_company_name VARCHAR(100),
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2.2 Actualizar precios con condicional (aumentar 10% productos sin stock)
UPDATE products
SET unit_price = unit_price * 1.10
WHERE units_in_stock = 0;

-- 2.3 Consulta compleja: Ventas por categoría (usando JOIN y GROUP BY)
SELECT 
    c.category_name, 
    SUM(od.quantity * od.unit_price) AS total_ventas
FROM 
    order_details od
JOIN 
    products p ON od.product_id = p.product_id
JOIN 
    categories c ON p.category_id = c.category_id
GROUP BY 
    c.category_name
ORDER BY 
    total_ventas DESC;
```

---

### **3. Transacciones y Concurrencia**
#### **📌 Objetivo**: Gestionar operaciones atómicas y bloqueos.
```sql
-- 3.1 Transacción con ROLLBACK en caso de error
BEGIN;
    INSERT INTO orders (order_id, customer_id, order_date) 
    VALUES (20000, 'ALFKI', CURRENT_DATE);
    
    INSERT INTO order_details (order_id, product_id, unit_price, quantity)
    VALUES (20000, 1, 18.00, 5);
    
    -- Verificar stock antes de COMMIT
    IF (SELECT units_in_stock FROM products WHERE product_id = 1) < 5 THEN
        RAISE NOTICE 'Stock insuficiente';
        ROLLBACK;
    ELSE
        COMMIT;
    END IF;

-- 3.2 Bloqueo pesimista (FOR UPDATE)
BEGIN;
    SELECT * FROM products WHERE product_id = 1 FOR UPDATE;
    -- En otra sesión, este SELECT se bloqueará:
    -- SELECT * FROM products WHERE product_id = 1 FOR UPDATE NOWAIT;
    UPDATE products SET units_in_stock = units_in_stock - 5 WHERE product_id = 1;
COMMIT;
```

---

## **📚 Recursos Adicionales**
- **Documentación PostgreSQL**: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)
- **Diagrama ER de Northwind**: [https://github.com/pthom/northwind_psql/blob/master/northwind_er.png](https://github.com/pthom/northwind_psql/blob/master/northwind_er.png)

---

## **🚀 Cómo Continuar**
1. Ejecuta cada ejercicio en orden.
2. Documenta tus observaciones en un archivo `NOTES.md`.
3. Experimenta modificando consultas y analizando resultados con `EXPLAIN ANALYZE`.

---

**🎯 ¡Listo para comenzar!**  
Si tienes problemas, consulta los issues del repositorio Northwind o abre un nuevo problema en tu fork.