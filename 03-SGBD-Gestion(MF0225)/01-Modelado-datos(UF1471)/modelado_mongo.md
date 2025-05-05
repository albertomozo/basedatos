# Guía Comparativa: Modelado Relacional vs. NoSQL (MongoDB)

## 1. Introducción al Modelado Relacional

### Conceptos Clave:
- **Discurso del Universo**: Todo lo que queremos representar en nuestra base de datos
- **Entidades**: Objetos del mundo real (Clientes, Productos, etc.)
- **Atributos**: Características de las entidades
- **Relaciones**: Cómo se conectan las entidades entre sí

### Ejemplo en Diagrama ER:
```
[Cliente] ---< [Pedido] >--- [Producto]
   |               |
  nombre        fecha
  email         estado
```

## 2. Modelado en MongoDB (NoSQL)

### Diferencias Fundamentales:
- **Sin esquema fijo**: Los documentos pueden variar en estructura
- **Denormalización**: Se prefieren datos embebidos sobre referencias
- **Orientado a documentos**: Jerarquías naturales de datos

### Patrones de Modelado Comunes:

#### a) Modelado Embebido (Embedded)
```json
// Documento de Cliente con pedidos embebidos
{
  "_id": "cliente123",
  "nombre": "Ana López",
  "email": "ana@example.com",
  "pedidos": [
    {
      "fecha": "2023-05-01",
      "productos": [
        {"productoId": "p1", "nombre": "Laptop", "cantidad": 1},
        {"productoId": "p2", "nombre": "Mouse", "cantidad": 2}
      ],
      "total": 1200.50
    }
  ]
}
```

#### b) Modelado por Referencia
```json
// Documento de Cliente
{
  "_id": "cliente123",
  "nombre": "Ana López",
  "email": "ana@example.com",
  "pedidos": ["pedido1", "pedido2"]
}

// Documento de Pedido separado
{
  "_id": "pedido1",
  "clienteId": "cliente123",
  "fecha": "2023-05-01",
  "productos": ["p1", "p2"],
  "total": 1200.50
}
```

## 3. Criterios para Elegir el Enfoque

| Criterio               | Embebido                            | Por Referencia                  |
|------------------------|-------------------------------------|----------------------------------|
| Relación 1:1 o 1:pocos | Ideal                               | No recomendado                  |
| Relación 1:muchos      | Depende del tamaño                  | Mejor para grandes volúmenes    |
| Frecuencia de lectura  | Lecturas rápidas (todo en un lugar) | Requiere múltiples consultas    |
| Frecuencia de updates  | Problemas si son frecuentes         | Mejor para updates independientes |
| Tamaño documento       | Cuidado con límite de 16MB          | Sin problemas de tamaño          |

## 4. Ejemplo Completo Comparativo

### Caso: Sistema de Blog (Posts y Comentarios)

**Modelo Relacional:**
```
[Usuario] ---< [Post] >---< [Comentario]
```

**Modelo MongoDB Embebido:**
```json
{
  "_id": "post123",
  "titulo": "Introducción a MongoDB",
  "autor": {
    "userId": "user1",
    "nombre": "Carlos"
  },
  "comentarios": [
    {
      "usuario": "Maria",
      "texto": "Excelente artículo",
      "fecha": "2023-05-10"
    }
  ]
}
```

**Modelo MongoDB por Referencia:**
```json
// Documento Post
{
  "_id": "post123",
  "titulo": "Introducción a MongoDB",
  "autorId": "user1",
  "comentarioIds": ["com1", "com2"]
}

// Documento Comentario
{
  "_id": "com1",
  "postId": "post123",
  "usuarioId": "user2",
  "texto": "Excelente artículo",
  "fecha": "2023-05-10"
}
```

## 5. Buenas Prácticas para MongoDB

1. **Pensar en cómo se accederá a los datos**: Modelar para los casos de uso más comunes
2. **Evitar joins excesivos**: MongoDB no está optimizado para operaciones JOIN complejas
3. **Considerar el crecimiento**: Documentos embebidos pueden crecer demasiado
4. **Usar índices adecuadamente**: Similar a SQL, pero con sintaxis diferente
5. **Atomicidad a nivel de documento**: Las transacciones son por documento

## 6. Ejercicio Práctico

**Escenario**: Sistema de reservas de hotel

**Modelo Relacional:**
```
[Cliente] ---< [Reserva] >--- [Habitación]
```

**Propuesta MongoDB:**
```json
{
  "_id": "reserva456",
  "fechaEntrada": "2023-06-15",
  "fechaSalida": "2023-06-20",
  "cliente": {
    "id": "cli789",
    "nombre": "Laura García",
    "email": "laura@example.com"
  },
  "habitacion": {
    "numero": 302,
    "tipo": "Suite",
    "precioNoche": 150
  },
  "serviciosAdicionales": [
    {"nombre": "Desayuno", "precio": 15},
    {"nombre": "Parking", "precio": 10}
  ]
}
```

¿Por qué este modelo podría ser mejor que uno relacional para este caso? Porque:
- Todas las información de la reserva está en un solo lugar
- No requiere joins para consultas comunes
- Permite variabilidad en servicios adicionales
- Es más intuitivo para desarrolladores al mapear directamente a objetos