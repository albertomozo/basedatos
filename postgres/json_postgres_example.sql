-- Crear tabla con campo JSONB
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    datos_producto JSONB NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT NOW()
);

-- Crear índice GIN para búsquedas eficientes
CREATE INDEX idx_productos_datos ON productos USING GIN (datos_producto);

-- Insertar datos de ejemplo
INSERT INTO productos (nombre, datos_producto) VALUES 
('Smartphone', '{
    "marca": "TechCorp",
    "precio": 599.99,
    "categoria": "electrónicos",
    "especificaciones": {
        "pantalla": "6.1 pulgadas",
        "memoria": "128GB",
        "camara": "12MP"
    },
    "colores": ["negro", "blanco", "azul"],
    "disponible": true,
    "tags": ["móvil", "smartphone", "tecnología"]
}'),
('Laptop Gaming', '{
    "marca": "GameTech",
    "precio": 1299.99,
    "categoria": "electrónicos",
    "especificaciones": {
        "procesador": "Intel i7",
        "memoria": "16GB RAM",
        "almacenamiento": "512GB SSD",
        "grafica": "RTX 3060"
    },
    "colores": ["negro"],
    "disponible": true,
    "tags": ["laptop", "gaming", "ordenador"]
}'),
('Camiseta', '{
    "marca": "FashionBrand",
    "precio": 29.99,
    "categoria": "ropa",
    "especificaciones": {
        "material": "100% algodón",
        "tallas": ["S", "M", "L", "XL"]
    },
    "colores": ["rojo", "verde", "negro"],
    "disponible": false,
    "tags": ["ropa", "casual", "algodón"]
}');

-- EJEMPLOS DE CONSULTAS

-- 1. Buscar productos por precio exacto
SELECT nombre, datos_producto ->> 'precio' as precio
FROM productos 
WHERE datos_producto ->> 'precio' = '599.99';

-- 2. Buscar productos con precio menor a 1000
SELECT nombre, datos_producto ->> 'precio' as precio
FROM productos 
WHERE (datos_producto ->> 'precio')::numeric < 1000;

-- 3. Buscar productos disponibles
SELECT nombre 
FROM productos 
WHERE datos_producto ->> 'disponible' = 'true';

-- 4. Buscar productos que contengan especificaciones específicas
SELECT nombre 
FROM productos 
WHERE datos_producto @> '{"especificaciones": {"memoria": "128GB"}}';

-- 5. Buscar productos por categoría
SELECT nombre, datos_producto ->> 'categoria' as categoria
FROM productos 
WHERE datos_producto ->> 'categoria' = 'electrónicos';

-- 6. Buscar productos que tengan cierta marca
SELECT nombre, datos_producto ->> 'marca' as marca
FROM productos 
WHERE datos_producto ? 'marca' 
AND datos_producto ->> 'marca' ILIKE '%tech%';

-- 7. Buscar productos con colores específicos
SELECT nombre 
FROM productos 
WHERE datos_producto -> 'colores' ? 'negro';

-- 8. Buscar productos con tags específicos
SELECT nombre, datos_producto -> 'tags' as tags
FROM productos 
WHERE datos_producto -> 'tags' ? 'gaming';

-- 9. Extraer todos los colores disponibles (usando jsonb_array_elements)
SELECT DISTINCT color
FROM productos,
     jsonb_array_elements_text(datos_producto -> 'colores') as color
ORDER BY color;

-- 10. Obtener estadísticas de precios por categoría
SELECT 
    datos_producto ->> 'categoria' as categoria,
    COUNT(*) as total_productos,
    AVG((datos_producto ->> 'precio')::numeric) as precio_promedio,
    MIN((datos_producto ->> 'precio')::numeric) as precio_minimo,
    MAX((datos_producto ->> 'precio')::numeric) as precio_maximo
FROM productos 
GROUP BY datos_producto ->> 'categoria';

-- 11. Actualizar un campo específico del JSON
UPDATE productos 
SET datos_producto = jsonb_set(
    datos_producto,
    '{precio}',
    '549.99'
)
WHERE nombre = 'Smartphone';

-- 12. Agregar una nueva propiedad al JSON
UPDATE productos 
SET datos_producto = datos_producto || '{"descuento": 10}'
WHERE datos_producto ->> 'categoria' = 'electrónicos';

-- 13. Eliminar una propiedad del JSON
UPDATE productos 
SET datos_producto = datos_producto - 'descuento'
WHERE id = 1;

-- 14. Búsqueda de texto completo en valores JSON
SELECT nombre 
FROM productos 
WHERE datos_producto::text ILIKE '%intel%';

-- 15. Consulta compleja: productos electrónicos disponibles con precio < 800
SELECT 
    nombre,
    datos_producto ->> 'marca' as marca,
    datos_producto ->> 'precio' as precio,
    datos_producto -> 'especificaciones' as specs
FROM productos 
WHERE datos_producto @> '{"categoria": "electrónicos", "disponible": true}'
AND (datos_producto ->> 'precio')::numeric < 800;

-- Ver estructura de datos
SELECT 
    nombre,
    jsonb_pretty(datos_producto) as datos_formateados
FROM productos 
LIMIT 1;