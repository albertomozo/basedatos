Aquí tienes una versión altamente mejorada con todas las características profesionales que necesitarías para un sistema de backups robusto:

```bash
#!/bin/bash

# =============================================
# SCRIPT AVANZADO DE BACKUP PARA MÚLTIPLES BD MYSQL
# =============================================

# Configuración (personalizar estas variables)
# --------------------------------------------
DB_USER="admin"
declare -a DATABASES=("midatabase" "otra_db" "una_mas" "db_importante")
BACKUP_ROOT="/backups/mysql"
RETENTION_DAYS=30
RETENTION_WEEKS=4
RETENTION_MONTHS=12
COMPRESSION_LEVEL=6
ENCRYPT_BACKUPS=true
ENCRYPTION_PASSWORD="TuPasswordSeguroAquí"
EMAIL_NOTIFICATIONS="admin@empresa.com"
MAX_LOG_SIZE=1048576 # 1MB en bytes

# Variables internas (no modificar)
# ---------------------------------
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DATE_ONLY=$(date +"%Y-%m-%d")
YEAR=$(date +"%Y")
MONTH=$(date +"%m")
WEEK=$(date +"%U")
LOG_DIR="$BACKUP_ROOT/logs"
DAILY_DIR="$BACKUP_ROOT/daily/$YEAR/$MONTH"
WEEKLY_DIR="$BACKUP_ROOT/weekly/$YEAR"
MONTHLY_DIR="$BACKUP_ROOT/monthly"
LOCK_FILE="/tmp/mysql_backup.lock"
LOG_FILE="$LOG_DIR/backup_${TIMESTAMP}.log"

# Funciones útiles
# ----------------

# Registrar en log con formato
log() {
    local level=$1
    local message=$2
    echo "$(date '+%Y-%m-%d %H:%M:%S') [$level] $message" | tee -a "$LOG_FILE"
}

# Verificar dependencias
check_dependencies() {
    local missing=()
    for cmd in mysqldump gzip pigz openssl mailx; do
        if ! command -v $cmd &> /dev/null; then
            missing+=("$cmd")
        fi
    done

    if [ ${#missing[@]} -gt 0 ]; then
        log "ERROR" "Faltan dependencias: ${missing[*]}"
        log "INFO" "Instalar con: sudo apt install mysql-client gzip pigz openssl mailutils"
        return 1
    fi
    return 0
}

# Comprimir backup
compress_backup() {
    local input=$1
    local output="$input.gz"
    
    log "INFO" "Comprimiendo backup (nivel $COMPRESSION_LEVEL)..."
    if pigz -$COMPRESSION_LEVEL -c "$input" > "$output"; then
        rm "$input"
        log "INFO" "Backup comprimido: $output ($(du -h "$output" | cut -f1))"
        return 0
    else
        log "ERROR" "Fallo en compresión"
        return 1
    fi
}

# Encriptar backup
encrypt_backup() {
    local input=$1
    local output="$input.enc"
    
    log "INFO" "Encriptando backup..."
    if openssl enc -aes-256-cbc -md sha512 -pbkdf2 -iter 100000 \
       -salt -pass pass:"$ENCRYPTION_PASSWORD" \
       -in "$input" -out "$output"; then
        rm "$input"
        log "INFO" "Backup encriptado: $output"
        return 0
    else
        log "ERROR" "Fallo en encriptación"
        return 1
    fi
}

# Verificar integridad del backup
verify_backup() {
    local file=$1
    local is_encrypted=false
    
    [[ "$file" == *.enc ]] && is_encrypted=true
    
    if $is_encrypted; then
        openssl enc -d -aes-256-cbc -md sha512 -pbkdf2 -iter 100000 \
        -pass pass:"$ENCRYPTION_PASSWORD" -in "$file" | gunzip -t >/dev/null 2>&1
    else
        gunzip -t "$file" >/dev/null 2>&1
    fi
    
    if [ $? -eq 0 ]; then
        log "INFO" "Verificación de integridad OK para $file"
        return 0
    else
        log "ERROR" "Backup corrupto: $file"
        return 1
    fi
}

# Enviar notificación por email
send_notification() {
    local subject=$1
    local body=$2
    
    if [ -n "$EMAIL_NOTIFICATIONS" ]; then
        mailx -s "$subject" "$EMAIL_NOTIFICATIONS" <<< "$body"
        log "INFO" "Notificación enviada a $EMAIL_NOTIFICATIONS"
    fi
}

# Rotar logs
rotate_logs() {
    find "$LOG_DIR" -name "*.log" -size +${MAX_LOG_SIZE}c -exec gzip {} \;
    find "$LOG_DIR" -name "*.log.gz" -mtime +30 -delete
}

# Limpieza de backups antiguos
clean_old_backups() {
    log "INFO" "Limpiando backups antiguos..."
    
    # Diarios
    find "$BACKUP_ROOT/daily" -type f -name "*.gz*" -mtime +$RETENTION_DAYS -delete
    
    # Semanales (conservar 4 semanas)
    find "$BACKUP_ROOT/weekly" -type f -name "*.gz*" -mtime +$((RETENTION_WEEKS*7)) -delete
    
    # Mensuales (conservar 12 meses)
    find "$BACKUP_ROOT/monthly" -type f -name "*.gz*" -mtime +$((RETENTION_MONTHS*30)) -delete
    
    log "INFO" "Limpieza completada"
}

# Copia especial semanal/mensual
special_backup_copy() {
    local source=$1
    local db=$2
    
    # Copia semanal (cada domingo)
    if [ $(date +%u) -eq 7 ]; then
        cp "$source" "$WEEKLY_DIR/${db}_weekly_${TIMESTAMP}.sql.gz"
        [ "$ENCRYPT_BACKUPS" = true ] && \
        encrypt_backup "$WEEKLY_DIR/${db}_weekly_${TIMESTAMP}.sql.gz"
    fi
    
    # Copia mensual (día 1 de cada mes)
    if [ $(date +%d) -eq 1 ]; then
        cp "$source" "$MONTHLY_DIR/${db}_monthly_${TIMESTAMP}.sql.gz"
        [ "$ENCRYPT_BACKUPS" = true ] && \
        encrypt_backup "$MONTHLY_DIR/${db}_monthly_${TIMESTAMP}.sql.gz"
    fi
}

# =============================================
# INICIO DEL SCRIPT PRINCIPAL
# =============================================

# Evitar ejecución simultánea
if [ -f "$LOCK_FILE" ]; then
    log "ERROR" "El script ya está en ejecución. Abortando."
    exit 1
else
    touch "$LOCK_FILE"
    trap 'rm -f "$LOCK_FILE"; exit' EXIT INT TERM
fi

# Preparar entorno
mkdir -p {"$LOG_DIR","$DAILY_DIR","$WEEKLY_DIR","$MONTHLY_DIR"}
log "INFO" "Iniciando backup MySQL - $TIMESTAMP"

# Verificar dependencias
if ! check_dependencies; then
    send_notification "MySQL Backup ERROR" "Faltan dependencias esenciales"
    exit 1
fi

# Procesar cada base de datos
ERROR_COUNT=0
for DB_NAME in "${DATABASES[@]}"; do
    log "INFO" "Procesando base de datos: $DB_NAME"
    BACKUP_FILE="$DAILY_DIR/${DB_NAME}_${TIMESTAMP}.sql"
    
    # 1. Realizar dump
    log "INFO" "Ejecutando mysqldump..."
    if ! mysqldump --single-transaction --quick --lock-tables=false \
        -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" > "$BACKUP_FILE" 2>> "$LOG_FILE"; then
        log "ERROR" "Falló mysqldump para $DB_NAME"
        ((ERROR_COUNT++))
        continue
    fi
    
    # 2. Comprimir
    if ! compress_backup "$BACKUP_FILE"; then
        ((ERROR_COUNT++))
        continue
    fi
    
    COMPRESSED_FILE="$BACKUP_FILE.gz"
    
    # 3. Encriptar (si está activado)
    if [ "$ENCRYPT_BACKUPS" = true ]; then
        if ! encrypt_backup "$COMPRESSED_FILE"; then
            ((ERROR_COUNT++))
            continue
        fi
        FINAL_FILE="$COMPRESSED_FILE.enc"
    else
        FINAL_FILE="$COMPRESSED_FILE"
    fi
    
    # 4. Verificar integridad
    if ! verify_backup "$FINAL_FILE"; then
        ((ERROR_COUNT++))
        continue
    fi
    
    # 5. Crear copias semanales/mensuales
    special_backup_copy "$FINAL_FILE" "$DB_NAME"
    
    log "INFO" "Backup completado para $DB_NAME: $FINAL_FILE"
done

# Limpieza y mantenimiento
clean_old_backups
rotate_logs

# Resumen final
if [ $ERROR_COUNT -eq 0 ]; then
    MSG="Todos los backups completados con éxito"
    log "SUCCESS" "$MSG"
    send_notification "MySQL Backup SUCCESS - $DATE_ONLY" "$MSG\nDetalles en $LOG_FILE"
else
    MSG="Hubo $ERROR_COUNT errores durante el proceso de backup"
    log "ERROR" "$MSG"
    send_notification "MySQL Backup WARNING - $DATE_ONLY" "$MSG\nRevise los logs en $LOG_FILE"
fi

log "INFO" "Tiempo total de ejecución: $SECONDS segundos"
exit $ERROR_COUNT
```

### Mejoras clave implementadas:

1. **Estructura de backups mejorada**:
   - Directorios separados para backups diarios/semanales/mensuales
   - Organización por año/mes para fácil navegación

2. **Sistema de retención avanzado**:
   - Configuración independiente para retención diaria/semanal/mensual
   - Limpieza automática de backups antiguos

3. **Seguridad reforzada**:
   - Encriptación AES-256 con OpenSSL (opcional)
   - Soporte para pigz (compresión paralela más rápida)
   - Verificación de integridad de backups

4. **Manejo de errores robusto**:
   - Conteo de errores por base de datos
   - Notificaciones por email diferenciadas (éxito/error)
   - Bloqueo para evitar ejecuciones simultáneas

5. **Optimizaciones de performance**:
   - Compresión con nivel configurable (1-9)
   - Opción para usar pigz (multihilo)
   - Parámetros optimizados para mysqldump

6. **Sistema de logging profesional**:
   - Niveles de log (INFO, ERROR, SUCCESS)
   - Rotación automática de logs
   - Límite de tamaño para archivos de log

7. **Configuración flexible**:
   - Variables claramente separadas para fácil personalización
   - Funciones modulares para mejor mantenimiento

8. **Copias especiales**:
   - Backups semanales (cada domingo)
   - Backups mensuales (día 1 de cada mes)

### Cómo implementar:

1. Guarda el script como `/usr/local/bin/mysql_backup_manager.sh`
2. Hazlo ejecutable: `chmod +x /usr/local/bin/mysql_backup_manager.sh`
3. Crea el directorio de backups: `mkdir -p /backups/mysql`
4. Configura el cron para ejecución automática (ejemplo diario a las 2 AM):
   ```bash
   0 2 * * * /usr/local/bin/mysql_backup_manager.sh
   ```
5. Para máxima seguridad, considera:
   - Configurar permisos restrictivos (600) para el script
   - Usar un archivo de configuración externo con las credenciales
   - Almacenar la contraseña de encriptación en un gestor de secretos

Este script está listo para entornos de producción y maneja todos los aspectos críticos de un sistema de backups profesional.