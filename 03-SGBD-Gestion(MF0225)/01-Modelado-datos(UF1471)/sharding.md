### **Sharding en Bases de Datos: Definición y Aplicación**  

El **sharding** (o **fragmentación horizontal**) es una técnica de diseño de bases de datos distribuidas que consiste en **dividir una tabla grande en particiones más pequeñas (llamadas "shards")**, cada una almacenada en un nodo distinto. Su objetivo principal es **mejorar el rendimiento y la escalabilidad** al distribuir la carga de trabajo.  

#### **¿En qué se diferencia del "partitioning" tradicional?**  
- **Partitioning** (particionamiento): División lógica de datos dentro de **una misma base de datos** (ej: particiones por rangos en PostgreSQL/MySQL).  
- **Sharding**: División física de datos en **múltiples servidores o instancias independientes**, típico en sistemas distribuidos (ej: MongoDB, Cassandra, sistemas Big Data).  

---

### **Aplicaciones del Sharding**  
1. **Bases de Datos NoSQL** (MongoDB, Cassandra, Elasticsearch):  
   - Distribuyen automáticamente los datos en shards para manejar grandes volúmenes.  
   - Ejemplo: Un shard almacena usuarios de la A-M, y otro de la N-Z.  

2. **Bases de Datos Relacionales Escalables** (PostgreSQL, MySQL):  
   - Se aplica manualmente o con extensiones (ej: **Citus** para PostgreSQL).  
   - Útil en aplicaciones con alto crecimiento (ej: redes sociales, e-commerce).  

3. **Sistemas Big Data** (Hadoop, Google Spanner):  
   - Los datos se dividen en bloques distribuidos en un clúster para procesamiento paralelo.  

---

### **Ventajas del Sharding**  
✔ **Escalabilidad horizontal**: Añadir más nodos permite manejar más datos y consultas.  
✔ **Mejor rendimiento**: Las consultas se ejecutan en paralelo sobre shards más pequeños.  
✔ **Alta disponibilidad**: Un shard caído no afecta a los demás (si hay replicación).  

### **Desventajas**  
✖ **Complejidad**: Consultas que requieren unir datos de múltiples shards (JOINs) son lentas.  
✖ **Desbalanceo**: Si la distribución no es uniforme, algunos shards pueden saturarse ("hot spots").  
✖ **Transacciones distribuidas**: Garantizar **ACID** es difícil (se usan modelos eventualmente consistentes).  

---

### **Tipos de Sharding**  
1. **Sharding por rango** (Range-based):  
   - Ej: Usuarios con ID 1-1000 en Shard1, 1001-2000 en Shard2.  
   - Problema: Puede causar desbalanceo si los datos no están uniformemente distribuidos.  

2. **Sharding por hash** (Hash-based):  
   - Se aplica una función hash a una clave (ej: `user_id`) para asignar el shard.  
   - Ventaja: Distribución más equilibrada.  

3. **Sharding por directorio** (Lookup-based):  
   - Una tabla de búsqueda (metadata) indica en qué shard está cada dato.  
   - Flexible pero con sobrecarga por consultar el directorio.  

---

### **Ejemplo Práctico**  
```sql
-- En una BD relacional con sharding (ej: Citus/PostgreSQL)  
CREATE TABLE users (  
   user_id bigserial PRIMARY KEY,  
   name varchar(100)  
) PARTITION BY HASH(user_id);  

-- Creación de shards en diferentes nodos  
CREATE TABLE users_shard1 PARTITION OF users  
   FOR VALUES WITH (MODULUS 3, REMAINDER 0);  

CREATE TABLE users_shard2 PARTITION OF users  
   FOR VALUES WITH (MODULUS 3, REMAINDER 1);  
```  
*En este caso, los datos se distribuyen en 3 shards según el `user_id`.*  

---

### **Conclusión**  
El **sharding** es clave en sistemas distribuidos para manejar escalabilidad masiva, pero requiere un diseño cuidadoso para evitar problemas de consistencia y rendimiento. Se usa ampliamente en **NoSQL, Big Data y bases de datos relacionales modernas** que necesitan crecer horizontalmente.
