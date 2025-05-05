# Ejercicio Práctico: Creación de una Base de Datos Distribuida con MariaDB en Red WiFi

**Objetivo:** Configurar una base de datos distribuida entre varios nodos MariaDB dentro de una red WiFi local, permitiendo a los alumnos entender los conceptos fundamentales de las bases de datos distribuidas.

## Escenario:
Una pequeña empresa tiene 3 departamentos (Ventas, Inventario y Personal) cada uno con su propio servidor MariaDB en la red WiFi local (192.168.1.0/24). Se necesita crear un sistema distribuido donde:

1. Cada departamento mantenga su propia base de datos
2. Se puedan realizar consultas que combinen datos de varios departamentos
3. Implementar replicación básica para alta disponibilidad

## Requisitos previos:
- 3 computadoras con MariaDB instalado (o 3 instancias en una sola máquina con puertos diferentes)
- Todas en la misma red WiFi
- Acceso administrativo a los servidores MariaDB

## Pasos del ejercicio:

### 1. Configuración inicial de los nodos

**Nodo 1 (Ventas - IP: 192.168.1.101):**
```sql
CREATE DATABASE ventas;
USE ventas;
CREATE TABLE clientes (
    id INT PRIMARY KEY,
    nombre VARCHAR(50),
    email VARCHAR(50)
);

INSERT INTO clientes VALUES 
(1, 'Juan Pérez', 'juan@empresa.com'),
(2, 'María García', 'maria@empresa.com');
```

**Nodo 2 (Inventario - IP: 192.168.1.102):**
```sql
CREATE DATABASE inventario;
USE inventario;
CREATE TABLE productos (
    id INT PRIMARY KEY,
    nombre VARCHAR(50),
    stock INT,
    precio DECIMAL(10,2)
);

INSERT INTO productos VALUES 
(1, 'Laptop', 15, 1200.00),
(2, 'Mouse', 50, 25.50);
```

**Nodo 3 (Personal - IP: 192.168.1.103):**
```sql
CREATE DATABASE personal;
USE personal;
CREATE TABLE empleados (
    id INT PRIMARY KEY,
    nombre VARCHAR(50),
    departamento VARCHAR(50),
    salario DECIMAL(10,2)
);

INSERT INTO empleados VALUES 
(1, 'Carlos Ruiz', 'Ventas', 2500.00),
(2, 'Ana López', 'Inventario', 2300.00);
```

### 2. Configurar usuarios y permisos remotos

En cada nodo, ejecutar (ajustando las IPs según corresponda):
```sql
CREATE USER 'admin_distribuido'@'192.168.1.%' IDENTIFIED BY 'password_seguro';
GRANT ALL PRIVILEGES ON *.* TO 'admin_distribuido'@'192.168.1.%';
FLUSH PRIVILEGES;
```

### 3. Crear tablas federadas (conectores entre nodos)

En cada nodo, habilitar el motor FEDERATED:
```sql
INSTALL SONAME 'ha_federated';
```

**En Nodo 1 (Ventas), crear enlace a Nodo 2 (Inventario):**
```sql
USE ventas;
CREATE TABLE productos_remotos (
    id INT PRIMARY KEY,
    nombre VARCHAR(50),
    stock INT,
    precio DECIMAL(10,2)
) ENGINE=FEDERATED 
CONNECTION='mysql://admin_distribuido:password_seguro@192.168.1.102:3306/inventario/productos';
```

**En Nodo 1 (Ventas), crear enlace a Nodo 3 (Personal):**
```sql
USE ventas;
CREATE TABLE empleados_remotos (
    id INT PRIMARY KEY,
    nombre VARCHAR(50),
    departamento VARCHAR(50),
    salario DECIMAL(10,2)
) ENGINE=FEDERATED 
CONNECTION='mysql://admin_distribuido:password_seguro@192.168.1.103:3306/personal/empleados';
```

### 4. Realizar consultas distribuidas

Ejemplo en Nodo 1:
```sql
-- Consulta que combina datos locales y remotos
SELECT c.nombre AS cliente, p.nombre AS producto
FROM clientes c
JOIN productos_remotos p ON 1=1; -- Ejemplo simple de combinación

-- Consulta más compleja
SELECT e.nombre AS empleado, COUNT(c.id) AS clientes_atendidos
FROM empleados_remotos e
LEFT JOIN clientes c ON e.nombre LIKE CONCAT('%', SUBSTRING_INDEX(c.nombre, ' ', 1), '%')
WHERE e.departamento = 'Ventas'
GROUP BY e.nombre;
```

### 5. Configurar replicación básica (opcional avanzado)

Configurar el Nodo 1 como maestro y los otros como esclavos para replicación:

**En Nodo 1 (maestro):**
```sql
[mysqld]
server-id = 1
log_bin = /var/log/mysql/mysql-bin.log
binlog_do_db = ventas
```

**En Nodos 2 y 3 (esclavos):**
```sql
[mysqld]
server-id = 2  # Usar 3 para el tercer nodo
relay-log = /var/log/mysql/mysql-relay-bin.log
log_bin = /var/log/mysql/mysql-bin.log
binlog_do_db = inventario  # o 'personal' en el tercer nodo
```

## Tareas para los alumnos:

1. Completar la configuración de todos los nodos
2. Crear consultas que combinen datos de al menos 2 nodos diferentes
3. Implementar medidas de seguridad básicas (mejorar contraseñas, restringir accesos)
4. Documentar el esquema distribuido completo
5. Proponer un mecanismo para sincronizar datos críticos entre nodos
6. Medir el rendimiento de consultas distribuidas vs locales

## Evaluación:
- Correcta configuración de los nodos
- Funcionamiento de consultas distribuidas
- Documentación clara del diseño
- Implementación de medidas de seguridad
- Análisis de rendimiento

**Nota:** Este ejercicio puede adaptarse para usar contenedores Docker si no se dispone de múltiples equipos físicos.