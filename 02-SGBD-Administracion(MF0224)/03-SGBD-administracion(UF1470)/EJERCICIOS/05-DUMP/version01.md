Bash mejorado con un bucle para hacer backups de múltiples bases de datos MySQL, manteniendo la seguridad y añadiendo características adicionales:

```bash
#!/bin/bash

# Script de copia de seguridad para múltiples bases de datos MySQL
# Usuario: admin
# Contraseña: alberto

# Configuración
DB_USER="admin"
DB_PASS="alberto"
DATABASES=("midatabase" "otra_db" "una_mas")  # Lista de bases de datos a respaldar
BACKUP_DIR="/ruta/donde/guardar/backups"     # Directorio donde se guardarán los backups
RETENTION_DAYS=7                             # Número de días para conservar backups
DATE=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$BACKUP_DIR/backup_log_$DATE.txt"

# Crear directorio de backups si no existe
mkdir -p "$BACKUP_DIR"

# Función para registrar mensajes en el log
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Verificar si mysqldump está instalado
if ! command -v mysqldump &> /dev/null; then
    log "ERROR: mysqldump no está instalado. Por favor, instálalo primero."
    log "Puedes instalarlo con: sudo apt install mysql-client"
    exit 1
fi

# Iniciar proceso de backup
log "INICIANDO PROCESO DE BACKUP"

# Bucle principal para cada base de datos
for DB_NAME in "${DATABASES[@]}"; do
    BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_backup_$DATE.sql"
    log "Realizando backup de la base de datos: $DB_NAME..."
    
    # Ejecutar mysqldump
    mysqldump -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" > "$BACKUP_FILE" 2>> "$LOG_FILE"
    
    # Verificar resultado
    if [ $? -eq 0 ]; then
        log "Backup de $DB_NAME completado con éxito."
        
        # Comprimir el backup
        log "Comprimiendo backup de $DB_NAME..."
        gzip "$BACKUP_FILE" 2>> "$LOG_FILE"
        log "Backup comprimido: ${BACKUP_FILE}.gz"
        
        # Verificar integridad del backup comprimido
        gzip -t "${BACKUP_FILE}.gz" 2>> "$LOG_FILE"
        if [ $? -ne 0 ]; then
            log "ERROR: El backup de $DB_NAME está corrupto!"
        fi
    else
        log "ERROR: Falló el backup de $DB_NAME"
    fi
done

# Limpieza de backups antiguos
log "Eliminando backups antiguos (más de $RETENTION_DAYS días)..."
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete 2>> "$LOG_FILE"
find "$BACKUP_DIR" -name "*.log.txt" -mtime +$RETENTION_DAYS -delete 2>> "$LOG_FILE"

log "PROCESO DE BACKUP COMPLETADO"
echo "Resumen del proceso guardado en: $LOG_FILE"
```

### Características mejoradas:

1. **Soporte para múltiples bases de datos**:
   - Las bases de datos se definen en el array `DATABASES`
   - El bucle `for` procesa cada una automáticamente

2. **Mejor manejo de logs**:
   - Registro detallado con marca de tiempo
   - Log separado para cada ejecución
   - Output combinado en pantalla y archivo

3. **Gestión de backups antiguos**:
   - Eliminación automática de backups más viejos que `RETENTION_DAYS`
   - Limpieza de logs antiguos

4. **Verificación de integridad**:
   - Comprobación de que el backup comprimido no está corrupto

5. **Más robusto**:
   - Captura de errores de cada comando
   - Mensajes más descriptivos

### Cómo usar:

1. Edita la lista `DATABASES` con los nombres de tus bases de datos
2. Configura `BACKUP_DIR` con tu directorio preferido
3. Ajusta `RETENTION_DAYS` según cuánto tiempo quieres conservar los backups
4. Haz el script ejecutable: `chmod +x backup_multidb.sh`
5. Ejecútalo: `./backup_multidb.sh`

### Consejo adicional:

Para mayor seguridad, considera usar un archivo `.my.cnf` con las credenciales en lugar de ponerlas en el script:

```
[client]
user=admin
password=alberto
```

Y luego cambiar el comando mysqldump a:
```bash
mysqldump --defaults-file=/ruta/segura/.my.cnf "$DB_NAME" > "$BACKUP_FILE"
```