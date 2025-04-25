# Script Bash para hacer una copia de seguridad de tu base de datos MySQL usando `mysqldump` en Linux 

```bash
#!/bin/bash

# Script de copia de seguridad para MySQL
# Base de datos: midatabase
# Usuario: admin
# Contraseña: alberto

# Configuración
DB_USER="*****"
DB_PASS="****"
DB_NAME="midatabase"
BACKUP_DIR="/ruta/donde/guardar/backups"  # Cambia esto a tu directorio deseado
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_backup_$DATE.sql"

# Crear directorio de backups si no existe
mkdir -p "$BACKUP_DIR"

# Verificar si mysqldump está instalado
if ! command -v mysqldump &> /dev/null; then
    echo "Error: mysqldump no está instalado. Por favor, instálalo primero."
    echo "Puedes instalarlo con: sudo apt install mysql-client"
    exit 1
fi

# Realizar el backup
echo "Realizando copia de seguridad de la base de datos $DB_NAME..."
mysqldump -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" > "$BACKUP_FILE"

# Verificar si el backup fue exitoso
if [ $? -eq 0 ]; then
    echo "Copia de seguridad completada con éxito."
    echo "Archivo creado: $BACKUP_FILE"
    
    # Opcional: Comprimir el backup
    echo "Comprimiendo el archivo de backup..."
    gzip "$BACKUP_FILE"
    echo "Backup comprimido: ${BACKUP_FILE}.gz"
else
    echo "Error al realizar la copia de seguridad."
    exit 1
fi
```

### Instrucciones de uso:

1. Guarda este script en un archivo, por ejemplo `backup_midatabase.sh`
2. Hazlo ejecutable: `chmod +x backup_midatabase.sh`
3. Edita el `BACKUP_DIR` para indicar dónde quieres guardar las copias de seguridad
4. Ejecútalo: `./backup_midatabase.sh`

### Características del script:

- Crea backups con marca de tiempo en el nombre del archivo
- Verifica que mysqldump esté instalado
- Comprime el backup automáticamente con gzip
- Proporciona mensajes informativos sobre el progreso

### Notas de seguridad:

Para mayor seguridad, considera:
1. Cambiar los permisos del archivo de backup: `chmod 600 ${BACKUP_FILE}.gz`
2. Usar un archivo de opciones de MySQL en lugar de la contraseña en texto plano
3. Configurar este script como un trabajo cron para backups automáticos


## PROPUESTA DE MEJORA.

Investigar sobre la orden cron (crontab) en linux para generar llamadas a scripts programadas con periocidad.