<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>



# **Ejercicio Práctico: Claves Foráneas y Restricciones en MariaDB**

## **Escenario Base**

Crearemos dos tablas relacionadas:

1. **clientes** (tabla padre)
2. **pedidos** (tabla hija)

---

## **Paso 1: Creación de Tablas SIN Claves Foráneas**

```sql
-- Crear base de datos
CREATE DATABASE tienda;
USE tienda;

-- Tabla clientes
CREATE TABLE clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL
);

-- Tabla pedidos SIN clave foránea
CREATE TABLE pedidos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cliente_id INT,
    producto VARCHAR(50) NOT NULL,
    fecha DATE NOT NULL
);
```


---

## **Paso 2: Insertar Datos y Generar Problemas**

### **Inserción inicial válida**

```sql
INSERT INTO clientes (nombre) VALUES ('Ana'), ('Luis');

INSERT INTO pedidos (cliente_id, producto, fecha) 
VALUES (1, 'Laptop', '2024-03-01'), 
       (2, 'Teléfono', '2024-03-02');
```


### **Generar inconsistencias**

```sql
-- 1. Registro huérfano (cliente_id inexistente)
INSERT INTO pedidos (cliente_id, producto, fecha)
VALUES (99, 'Tablet', '2024-03-03'); -- Se inserta sin error

-- 2. Eliminar cliente con pedidos existentes
DELETE FROM clientes WHERE id = 1; -- Elimina a Ana pero sus pedidos quedan
```

**Resultado:**

```
SELECT * FROM pedidos;
+----+------------+----------+------------+
| id | cliente_id | producto | fecha      |
+----+------------+----------+------------+
| 1  | 1          | Laptop   | 2024-03-01 | <-- ¡Cliente 1 ya no existe!
| 2  | 2          | Teléfono | 2024-03-02 |
| 3  | 99         | Tablet   | 2024-03-03 | <-- Cliente inexistente
+----+------------+----------+------------+
```


---

## **Paso 3: Solución con Claves Foráneas**

### **Recrear tablas con restricciones**

```sql
DROP TABLE pedidos;

CREATE TABLE pedidos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cliente_id INT,
    producto VARCHAR(50) NOT NULL,
    fecha DATE NOT NULL,
    CONSTRAINT fk_cliente
        FOREIGN KEY (cliente_id) 
        REFERENCES clientes(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```


---

## **Paso 4: Demostrar Restricciones**

### **Prueba 1: Insertar pedido con cliente inexistente**

```sql
INSERT INTO pedidos (cliente_id, producto, fecha)
VALUES (99, 'Smartwatch', '2024-03-04');
```

**Error:**

```
ERROR 1452 (23000): Cannot add or update a child row: 
a foreign key constraint fails (`tienda`.`pedidos`, 
CONSTRAINT `fk_cliente` FOREIGN KEY (`cliente_id`) 
REFERENCES `clientes` (`id`) ON DELETE CASCADE ON UPDATE CASCADE)
```


### **Prueba 2: Eliminar cliente con pedidos**

```sql
DELETE FROM clientes WHERE id = 2;
```

**Resultado:**

```
SELECT * FROM pedidos;
+----+------------+----------+------------+
| id | cliente_id | producto | fecha      |
+----+------------+----------+------------+
| 2  | 2          | Teléfono | 2024-03-02 | <-- ¡Eliminado automáticamente!
+----+------------+----------+------------+
```


---

## **Opciones de Restricción Clave**

### **1. ON DELETE**

| Opción | Comportamiento |
| :-- | :-- |
| **CASCADE** | Elimina los registros hijos automáticamente |
| **RESTRICT** | Bloquea la eliminación si existen registros hijos (valor por defecto) |
| **SET NULL** | Establece cliente_id = NULL en los pedidos (requiere columna NULL permitido) |
| **NO ACTION** | Similar a RESTRICT |

### **2. ON UPDATE**

| Opción | Comportamiento |
| :-- | :-- |
| **CASCADE** | Actualiza automáticamente el cliente_id en los pedidos |
| **RESTRICT** | Bloquea la actualización del ID en clientes si hay pedidos relacionados |


---

## **Ejemplo con SET NULL**

```sql
ALTER TABLE pedidos
DROP FOREIGN KEY fk_cliente;

ALTER TABLE pedidos
MODIFY cliente_id INT NULL,  -- Permitir valores NULL
ADD CONSTRAINT fk_cliente
    FOREIGN KEY (cliente_id) 
    REFERENCES clientes(id)
    ON DELETE SET NULL;

-- Eliminar cliente
DELETE FROM clientes WHERE id = 2;

-- Resultado
SELECT * FROM pedidos;
+----+------------+----------+------------+
| id | cliente_id | producto | fecha      |
+----+------------+----------+------------+
| 2  | NULL       | Teléfono | 2024-03-02 | <-- cliente_id = NULL
+----+------------+----------+------------+
```


---

## **Mejores Prácticas**

1. **Usar siempre claves foráneas** para mantener la integridad referencial
2. **Elegir ON DELETE** según necesidades:
    - CASCADE para relaciones fuertes (ej: factura-detalle)
    - SET NULL para relaciones opcionales
3. **Índices automáticos**: MariaDB crea índices en claves foráneas
4. **Nombre de restricciones**: Usar nombres descriptivos (ej: fk_tabla_columna)
5. **Orden en eliminación de tablas**:

```sql
DROP TABLE pedidos;  -- Primero eliminar tablas hijas
DROP TABLE clientes;
```


---

## **Conclusión**

Las claves foráneas son esenciales para:

- Evitar registros huérfanos
- Mantener la consistencia de los datos
- Automatizar comportamientos con CASCADE/SET NULL
- Cumplir con las reglas de negocio a nivel de base de datos

Este ejercicio muestra cómo pasar de un diseño vulnerable a inconsistencias a un modelo robusto y autocontenido mediante el uso apropiado de restricciones referenciales.

<div style="text-align: center">⁂</div>

[^1]: https://es.wikipedia.org/wiki/Clave_for%C3%A1nea

[^2]: https://www.ibm.com/docs/es/db2/11.1?topic=constraints-foreign-keys-in-referential

[^3]: https://mariadb.com/kb/en/foreign-keys/

[^4]: https://database.guide/what-is-an-orphaned-record/

[^5]: https://hevodata.com/learn/what-is-mariadb-foreign-key/

[^6]: https://www.restack.io/p/mariadb-answer-foreign-key-troubleshooting-cat-ai

[^7]: https://ingsystemas.webnode.es/bases-de-datos/llaves-primarias-y-foraneas/

[^8]: https://informaticosinlimites.com/base-de-datos/clave-primaria-y-foranea/

[^9]: http://download.nust.na/pub6/mysql/doc/refman/5.0/es/innodb-foreign-key-constraints.html

[^10]: https://www.cockroachlabs.com/docs/stable/foreign-key

[^11]: https://stackoverflow.com/questions/16163301/mysql-workbench-foreign-key-options-restrict-cascade-set-null-no-action-wh

[^12]: http://manual-tecnico-bd-oracle.readthedocs.io/es/latest/Modelo de datos.html

[^13]: https://learn.microsoft.com/es-es/sql/relational-databases/tables/disable-foreign-key-constraints-for-replication?view=sql-server-ver16

[^14]: https://learn.microsoft.com/en-us/sql/relational-databases/tables/primary-and-foreign-key-constraints?view=sql-server-ver16

[^15]: https://www.ibm.com/docs/en/ias?topic=constraints-foreign-key-referential

[^16]: https://www.primeinstitute.com/preguntas/importancia-y-diferencias-entre-clave-primaria-y-clave-foranea-en-bases-de-datos-todo-lo-que-necesitas-saber-18753

[^17]: https://www.ibm.com/docs/es/db2/11.5?topic=constraints-foreign-key-referential

[^18]: https://www.cockroachlabs.com/blog/what-is-a-foreign-key/

[^19]: https://codefinity.com/courses/v2/5ac24d9d-4a16-45b3-8856-07dec028c5e9/3d6c4ab0-f470-4b5d-ad0e-5f76d28ca0af/3cd3d9b1-2ba8-4377-94b6-5330f28478b9

[^20]: https://www.reddit.com/r/learnprogramming/comments/rdx1x6/how_to_set_up_a_foreign_key_in_mariadb/

[^21]: https://mariadb.com/docs/server/sql/features/constraints/enterprise-server/foreign-key/

[^22]: http://www.wiki.sharewiz.net/doku.php?id=mysql%3Afinding_and_deleting_orphaned_rows

[^23]: https://www.mariadbtutorial.com/mariadb-basics/mariadb-foreign-key/

[^24]: https://stackoverflow.com/questions/60288157/foreign-key-constraints-not-enforced-on-mariadb-what-am-i-doing-wrong

[^25]: https://www.reddit.com/r/SQL/comments/mlvooz/tables_with_no_foreign_keys/

[^26]: https://stackoverflow.com/questions/36551181/mysql-find-orphan-rows

[^27]: https://fromdual.com/mariadb-foreign-key-constraint-example

[^28]: https://mariadb.com/kb/en/possible-inconsistency-on-foreign-key-definition/

[^29]: https://code.openark.org/blog/mysql/things-that-dont-work-well-with-mysqls-foreign-key-implementation

[^30]: https://mariadb.com/resources/blog/get-rid-of-orphaned-innodb-temporary-tables-the-right-way/

[^31]: https://www.youtube.com/watch?v=hkge6sS-MmE

[^32]: https://www.ibm.com/docs/es/ida/9.1.2?topic=entities-primary-foreign-keys

[^33]: https://keepcoding.io/blog/llaves-primarias-y-foraneas/

[^34]: https://lopddirecta.es/que-significa-fk-en-base-de-datos/

[^35]: https://www.ibm.com/docs/en/db2/11.5.x?topic=constraints-foreign-key-referential

[^36]: https://dev.mysql.com/doc/en/create-table-foreign-keys.html

[^37]: https://stackoverflow.com/questions/67882002/can-you-have-no-or-weak-constraint-on-foreign-key-in-mysql-or-any-database

[^38]: https://planetscale.com/docs/learn/operating-without-foreign-key-constraints

[^39]: https://dataedo.com/kb/query/mariadb/tables-without-foreign-keys

[^40]: https://dba.stackexchange.com/questions/146349/mariadb-disable-foreign-key-checks

