# Guía Rápida: Campos JSON en PostgreSQL

## ¿Qué son los campos JSON?

PostgreSQL ofrece dos tipos de datos para almacenar JSON:
- **JSON**: Almacena texto JSON exactamente como se ingresa (preserva espacios, orden de claves)
- **JSONB**: Almacena JSON en formato binario (más eficiente, soporta indexación)

**Recomendación**: Usa JSONB en la mayoría de casos por su mejor rendimiento.

## Características principales

**Ventajas:**
- Flexibilidad para datos semi-estructurados
- No requiere esquema fijo
- Soporta indexación (JSONB)
- Validación automática de formato JSON
- Operadores especializados para consultas

**Limitaciones:**
- Menor rendimiento que columnas relacionales para datos estructurados
- Tamaño máximo de 1GB por campo
- JSON no soporta indexación (solo JSONB)

## Operadores principales para consultas

```sql
-- Acceso a propiedades
-> 'clave'          -- Devuelve JSON
->> 'clave'         -- Devuelve texto
#> '{clave,subclave}' -- Acceso a rutas anidadas (JSON)
#>> '{clave,subclave}' -- Acceso a rutas anidadas (texto)

-- Búsquedas y comparaciones
@> '{"clave":"valor"}'  -- Contiene
<@ '{"clave":"valor"}'  -- Está contenido en
? 'clave'               -- Existe la clave
?| array['clave1','clave2'] -- Existe alguna clave
?& array['clave1','clave2'] -- Existen todas las claves

-- Operadores de ruta
jsonb_path_exists(campo, '$.clave')  -- Verificar existencia
jsonb_path_query(campo, '$.clave')   -- Consultar valor
```

## Funciones útiles

```sql
-- Manipulación
jsonb_set(campo, '{clave}', '"nuevo_valor"')  -- Modificar valor
jsonb_insert(campo, '{clave}', '"valor"')     -- Insertar
campo - 'clave'                               -- Eliminar clave
campo || '{"nueva":"clave"}'                  -- Concatenar

-- Conversión y extracción
jsonb_each(campo)           -- Expandir a filas clave-valor
jsonb_array_elements(campo) -- Expandir array a filas
jsonb_keys(campo)           -- Obtener todas las claves
```

## Indexación

```sql
-- Índice GIN (recomendado para JSONB)
CREATE INDEX idx_datos_gin ON tabla USING GIN (campo_jsonb);

-- Índice en ruta específica
CREATE INDEX idx_datos_nombre ON tabla USING GIN ((campo_jsonb -> 'nombre'));

-- Índice de expresión
CREATE INDEX idx_datos_email ON tabla ((campo_jsonb ->> 'email'));
```

## Ejemplo práctico## Consejos de rendimiento

1. **Usa JSONB** en lugar de JSON para mejor rendimiento
2. **Crea índices GIN** en campos JSONB que consultes frecuentemente
3. **Evita SELECT \*** con campos JSON grandes
4. **Considera extraer campos frecuentemente consultados** a columnas separadas
5. **Usa operadores específicos** (@>, ?, etc.) en lugar de conversiones a texto cuando sea posible

## Cuándo usar campos JSON

**Ideal para:**
- Configuraciones de usuario
- Metadatos variables
- Logs y eventos
- APIs que reciben datos dinámicos
- Prototipado rápido

**Evitar cuando:**
- Los datos tienen estructura fija y conocida
- Necesitas integridad referencial estricta
- Realizas muchas consultas relacionales complejas
- El rendimiento es crítico para consultas simples

Los campos JSON en PostgreSQL ofrecen una excelente flexibilidad para manejar datos semi-estructurados mientras mantienes las ventajas de una base de datos relacional.