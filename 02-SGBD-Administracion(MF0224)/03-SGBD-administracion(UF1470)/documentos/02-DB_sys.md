

### 🔎 **Principales vistas para el análisis del SGBD**  

1️⃣ **`sys.processlist`** → Similar a `SHOW PROCESSLIST`, pero con información más clara sobre procesos en ejecución.  
📌 **Ejemplo de uso:**  
```sql
SELECT * FROM sys.processlist;
```  
Esto te ayuda a detectar consultas largas o bloqueos en la base de datos.  

2️⃣ **`sys.schema_table_statistics`** → Muestra estadísticas de acceso a las tablas, útil para identificar cuellos de botella en el rendimiento.  
📌 **Ejemplo de uso:**  
```sql
SELECT * FROM sys.schema_table_statistics WHERE table_schema = 'nombre_de_tu_bd';
```  
Te permitirá ver qué tablas se están utilizando más y cuáles podrían necesitar optimización.  

3️⃣ **`sys.host_summary`** → Información detallada sobre los hosts que están conectados al servidor.  
📌 **Ejemplo de uso:**  
```sql
SELECT * FROM sys.host_summary;
```  
Ayuda a detectar conexiones excesivas desde ciertos hosts que puedan afectar el rendimiento.  

4️⃣ **`sys.user_summary`** → Muestra datos sobre la actividad de los usuarios en la base de datos.  
📌 **Ejemplo de uso:**  
```sql
SELECT * FROM sys.user_summary ORDER BY total_connections DESC;
```  
Te permite identificar usuarios con más actividad y posibles problemas de autenticación.  

### ⚙️ **Procedimientos almacenados útiles**  
Algunos procedimientos te permiten obtener información rápidamente sin necesidad de consultas manuales:  

🔹 **`sys.get_lock_waits`** → Muestra información sobre bloqueos en las tablas.  
📌 **Ejemplo de uso:**  
```sql
CALL sys.get_lock_waits();
```  
Si tu base de datos tiene problemas de concurrencia, este procedimiento te ayudará a identificarlos.  

🔹 **`sys.ps_setup_enable_monitor`** → Activa la captura de datos en `performance_schema` para un mejor análisis.  
📌 **Ejemplo de uso:**  
```sql
CALL sys.ps_setup_enable_monitor();
```  
Si necesitas información detallada sobre el rendimiento, este comando es clave.  

🔹 **`sys.ps_setup_disable_monitor`** → Desactiva la monitorización si ya no la necesitas.  
📌 **Ejemplo de uso:**  
```sql
CALL sys.ps_setup_disable_monitor();
```  

### 🛠️ **Consejos adicionales**  
- Usa estas vistas regularmente para detectar problemas antes de que afecten el rendimiento.  
- Filtra los resultados para obtener información más específica.  
- Combina los datos con herramientas externas (como `Grafana` o `Prometheus`) para una mejor visualización.  

¿Qué aspecto te interesa profundizar más? 🚀  
