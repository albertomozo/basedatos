# Guía Genérica de Procedimientos Almacenados en Bases de Datos

## 1. Introducción a los Procedimientos Almacenados

### ¿Qué son los Procedimientos Almacenados?
Los procedimientos almacenados son colecciones de instrucciones SQL precompiladas y almacenadas en el servidor de base de datos. Funcionan como "mini-programas" que pueden ser invocados para realizar operaciones específicas.

### Ventajas de los Procedimientos Almacenados
- **Rendimiento**: Al estar precompilados, se ejecutan más rápido
- **Reutilización**: Se escriben una vez y se usan muchas veces
- **Seguridad**: Permiten controlar el acceso a las tablas
- **Reducción del tráfico de red**: Solo se envía la llamada al procedimiento, no todas las instrucciones
- **Modularidad**: Facilitan organizar la lógica de negocio
- **Mantenimiento**: Centralizan la lógica en un solo lugar

## 2. Conceptos Fundamentales (Comunes a la mayoría de SGBD)

### Elementos Básicos
- **Nombre del procedimiento**: Identificador único
- **Parámetros**: Valores que se pasan al procedimiento
- **Variables locales**: Almacenan valores temporales durante la ejecución
- **Cuerpo del procedimiento**: Instrucciones SQL y lógica de programación
- **Control de flujo**: Estructuras condicionales y de repetición
- **Manejo de errores**: Captura y gestión de excepciones

### Tipos de Parámetros (Concepto general)
- **Entrada (IN)**: Valores que se envían al procedimiento
- **Salida (OUT)**: Valores que el procedimiento devuelve
- **Entrada/Salida (INOUT)**: Combinación de ambos

## 3. Enfoque de Enseñanza por Conceptos

### Estructura General (Pseudocódigo)
```
CREAR PROCEDIMIENTO nombre_procedimiento (parámetros)
INICIO
    -- Declaración de variables locales
    -- Lógica del procedimiento
    -- Instrucciones SQL
FIN
```

### Conceptos de Programación en Procedimientos

#### Variables y Tipos de Datos
- Declaración de variables
- Asignación de valores
- Tipos de datos comunes (enteros, cadenas, fechas, etc.)

#### Estructuras de Control
- **Condicionales**: Si-Entonces-Sino (IF-THEN-ELSE)
- **Casos**: Evaluación de múltiples condiciones (CASE)
- **Bucles**: Mientras (WHILE), Repetir (REPEAT), Para (FOR)

#### Manejo de Errores
- Captura de excepciones
- Transacciones (Commit/Rollback)
- Notificación de errores

#### Cursores
- Definición conceptual
- Operaciones básicas (declarar, abrir, recorrer, cerrar)

## 4. Comparativa entre SGBD Populares

### Sintaxis Básica de Creación

| SGBD | Sintaxis Básica |
|------|-----------------|
| MySQL/MariaDB | `DELIMITER //`<br>`CREATE PROCEDURE nombre_proc(params)`<br>`BEGIN`<br>  `-- instrucciones`<br>`END //`<br>`DELIMITER ;` |
| SQL Server | `CREATE PROCEDURE nombre_proc`<br>`@param1 tipo,`<br>`@param2 tipo`<br>`AS`<br>`BEGIN`<br>  `-- instrucciones`<br>`END` |
| Oracle | `CREATE OR REPLACE PROCEDURE nombre_proc(`<br>  `param1 IN tipo,`<br>  `param2 OUT tipo)`<br>`AS`<br>`BEGIN`<br>  `-- instrucciones`<br>`END;` |
| PostgreSQL | `CREATE OR REPLACE FUNCTION nombre_func(`<br>  `param1 tipo,`<br>  `param2 tipo)`<br>`RETURNS tipo AS $$`<br>`BEGIN`<br>  `-- instrucciones`<br>`END;`<br>`$$ LANGUAGE plpgsql;` |
| SQLite | No soporta procedimientos almacenados nativos |

### Diferencias Clave en Parámetros

| SGBD | Sintaxis de Parámetros |
|------|------------------------|
| MySQL/MariaDB | `IN param1 tipo, OUT param2 tipo, INOUT param3 tipo` |
| SQL Server | `@param1 tipo = valor_defecto OUTPUT` |
| Oracle | `param1 IN tipo, param2 OUT tipo, param3 IN OUT tipo` |
| PostgreSQL | `IN param1 tipo, INOUT param2 tipo, OUT param3 tipo` |

## 5. Metodología de Enseñanza Práctica

### Enfoque Progresivo
1. **Procedimientos básicos**: Sin parámetros, solo SELECT/INSERT simples
2. **Introducción de parámetros**: Comenzar con parámetros de entrada
3. **Procedimientos con salida**: Agregando parámetros de salida
4. **Lógica de control**: Implementar condicionales y bucles
5. **Manejo de errores**: Introducir gestión de excepciones
6. **Procedimientos avanzados**: Cursores y casos de uso complejos

### Ejercicios Escalonados

#### Nivel 1: Procedimiento Básico
Crear un procedimiento que liste registros de una tabla.

#### Nivel 2: Procedimiento con Parámetros de Entrada
Filtrar registros según criterios pasados como parámetros.

#### Nivel 3: Procedimiento con Salida
Calcular y devolver estadísticas sobre los datos.

#### Nivel 4: Lógica Condicional
Implementar diferentes caminos de ejecución según condiciones.

#### Nivel 5: Procedimiento con Transacciones
Garantizar la integridad de los datos mediante transacciones.

#### Nivel 6: Procedimiento con Cursores
Procesar registros uno a uno mediante cursores.

## 6. Adaptación a Diferentes SGBD

### Estrategia de Enseñanza
1. **Enseñar conceptos**: Enfocarse primero en los conceptos universales
2. **Mostrar ejemplos genéricos**: Usar pseudocódigo para explicar la lógica
3. **Adaptación específica**: Proporcionar la sintaxis específica de cada SGBD
4. **Tabla de referencia**: Mantener a mano una tabla de equivalencias entre SGBD

### Ejemplo de Tabla de Equivalencias

| Concepto | MySQL/MariaDB | SQL Server | Oracle | PostgreSQL |
|----------|---------------|------------|--------|------------|
| Declarar variable | `DECLARE x INT;` | `DECLARE @x INT;` | `x NUMBER;` | `DECLARE x INT;` |
| Asignar valor | `SET x = 10;` | `SET @x = 10;` | `x := 10;` | `x := 10;` |
| Condicional | `IF... THEN... ELSE... END IF;` | `IF... BEGIN... END ELSE BEGIN... END` | `IF... THEN... ELSE... END IF;` | `IF... THEN... ELSE... END IF;` |
| Bucle | `WHILE... DO... END WHILE;` | `WHILE... BEGIN... END` | `LOOP... EXIT WHEN... END LOOP;` | `WHILE... LOOP... END LOOP;` |

## 7. Mejores Prácticas (Universales)

### Diseño
- **Nombres descriptivos**: Usar convenciones de nomenclatura consistentes
- **Un solo propósito**: Cada procedimiento debe realizar una tarea específica
- **Modularidad**: Dividir tareas complejas en procedimientos más pequeños
- **Comentarios**: Documentar el propósito, parámetros y funcionamiento

### Rendimiento
- **Evitar cursores** cuando sea posible (preferir operaciones de conjunto)
- **Minimizar el uso de tablas temporales**
- **Optimizar consultas** dentro de los procedimientos
- **Usar índices** adecuadamente

### Seguridad
- **Validar parámetros** de entrada
- **Evitar SQL dinámico** salvo cuando sea estrictamente necesario
- **Gestionar permisos** adecuadamente

### Mantenimiento
- **Control de versiones** para los procedimientos
- **Procedimientos de prueba** para validar funcionalidad
- **Scripts de instalación/actualización**

## 8. Caso de Estudio Universal

### Sistema de Gestión de Pedidos

#### Procedimiento 1: Crear Pedido (Pseudocódigo)
```
PROCEDIMIENTO crear_pedido(
    IN cliente_id, 
    IN productos_json, 
    OUT pedido_id, 
    OUT mensaje
)
INICIO
    INICIAR TRANSACCIÓN
    
    INSERTAR EN pedidos (cliente_id, fecha)
    VALORES (cliente_id, FECHA_ACTUAL())
    
    pedido_id = ÚLTIMO_ID_INSERTADO()
    
    PARA CADA producto EN productos_json HACER
        INSERTAR EN detalles_pedido (pedido_id, producto_id, cantidad, precio)
        VALORES (pedido_id, producto.id, producto.cantidad, ObtenerPrecio(producto.id))
        
        ACTUALIZAR inventario 
        ESTABLECER stock = stock - producto.cantidad 
        DONDE id = producto.id
    FIN PARA
    
    CONFIRMAR TRANSACCIÓN
    
    mensaje = "Pedido creado correctamente"
    
EXCEPCIÓN
    DESHACER TRANSACCIÓN
    mensaje = "Error al crear el pedido"
FIN
```

#### Procedimiento 2: Verificar Disponibilidad (Pseudocódigo)
```
PROCEDIMIENTO verificar_disponibilidad(
    IN productos_json, 
    OUT disponible, 
    OUT mensaje
)
INICIO
    disponible = VERDADERO
    mensaje = "Todos los productos están disponibles"
    
    PARA CADA producto EN productos_json HACER
        stock_actual = SELECCIONAR stock DESDE inventario DONDE id = producto.id
        
        SI stock_actual < producto.cantidad ENTONCES
            disponible = FALSO
            mensaje = CONCATENAR("Stock insuficiente para el producto ID: ", producto.id)
            SALIR DEL BUCLE
        FIN SI
    FIN PARA
FIN
```

## 9. Herramientas de Desarrollo y Depuración

### Herramientas Comunes
- Interfaces gráficas para gestión de bases de datos
- Editores de código con resaltado de sintaxis SQL
- Software de control de versiones

### Depuración de Procedimientos
- Técnicas de depuración según el SGBD
- Logging y trazabilidad
- Mensajes de error significativos

## 10. Consideraciones para Migración entre SGBD

### Estrategias
- Identificar diferencias de sintaxis
- Mapear tipos de datos equivalentes
- Adaptar funciones específicas del sistema
- Probar exhaustivamente la funcionalidad

### Proceso de Migración
1. Analizar los procedimientos existentes
2. Documentar la lógica de negocio
3. Reescribir usando la sintaxis del nuevo SGBD
4. Probar la equivalencia funcional

## Conclusión

Los procedimientos almacenados son una herramienta fundamental en el desarrollo de bases de datos, independientemente del SGBD utilizado. Aunque la sintaxis varía, los conceptos fundamentales son universales y transferibles. Al enseñar procedimientos almacenados, es importante enfocarse primero en los conceptos y luego en las implementaciones específicas, facilitando así el aprendizaje y la adaptación a diferentes sistemas.
