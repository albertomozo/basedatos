## Guía Rápida: Replicación de Streaming (Física) en PostgreSQL

Esta guía te ayudará a configurar una replicación básica de "streaming" en PostgreSQL. Asumimos que tienes dos servidores: uno **primario** (maestro) y uno **secundario** (réplica o standby).

**Objetivo:** El servidor secundario mantendrá una copia idéntica y actualizada del primario, ideal para lectura de escalado y preparación para un posible failover.

### Requisitos Previos:

* **PostgreSQL instalado** en ambos servidores (versión compatible, preferiblemente la misma).
* **Conectividad de red** entre el primario y el secundario.
* **Usuario con privilegios de superusuario** (o un rol con `REPLICATION` en PostgreSQL 10+).

### Paso 1: Configuración en el Servidor Primario (Maestro)

1.  **Editar `postgresql.conf`:**
    Abre el archivo `postgresql.conf` (ubicación común: `/etc/postgresql/<version>/main/postgresql.conf` o `/var/lib/pgsql/data/postgresql.conf`) y ajusta los siguientes parámetros:

    ```ini
    # Habilitar el envío de WALs al secundario
    wal_level = replica

    # Número máximo de conexiones de WAL a las que se puede conectar un servidor en espera
    max_wal_senders = 10 # Un valor razonable, ajusta según tus necesidades

    # Tamaño de los segmentos WAL a mantener. Asegura que el secundario no se quede sin WALs
    wal_keep_durable_wal_size = 5GB # (PostgreSQL 13+) O wal_keep_segments para versiones anteriores (ej: 512, cada segmento es 16MB)
    # Ejemplo para versiones anteriores: wal_keep_segments = 320 (320 * 16MB = 5GB aprox)

    # Permitir que el primario escuche conexiones desde el secundario
    listen_addresses = '*' # O la IP específica del secundario
    ```

2.  **Editar `pg_hba.conf`:**
    Abre el archivo `pg_hba.conf` (mismo directorio que `postgresql.conf`) y añade una línea para permitir la conexión de replicación desde el secundario. **Asegúrate de que esta línea esté antes de cualquier regla `reject` general.**

    ```
    # TYPE  DATABASE        USER            ADDRESS                 METHOD
    host    replication     all             <IP_DEL_SECUNDARIO>/32  scram-sha-256 # O trust si estás en un entorno seguro y de prueba
    ```
    Reemplaza `<IP_DEL_SECUNDARIO>` con la dirección IP de tu servidor secundario. `scram-sha-256` es recomendado para seguridad; puedes usar `md5` para versiones anteriores de PG o `trust` para pruebas rápidas (no recomendado en producción).

3.  **Crear un usuario de replicación:**
    Conéctate a PostgreSQL como superusuario y crea un rol dedicado a la replicación:

    ```sql
    CREATE ROLE replicador WITH REPLICATION LOGIN ENCRYPTED PASSWORD 'tu_contraseña_segura';
    ```

4.  **Reiniciar PostgreSQL:**
    Para que los cambios surtan efecto, reinicia el servicio PostgreSQL en el primario:

    ```bash
    sudo systemctl restart postgresql # En sistemas basados en systemd (Ubuntu/Debian/RHEL 7+)
    # O sudo service postgresql restart
    ```

### Paso 2: Preparación en el Servidor Secundario (Réplica/Standby)

1.  **Detener PostgreSQL:**
    Asegúrate de que el servicio PostgreSQL esté detenido en el servidor secundario:

    ```bash
    sudo systemctl stop postgresql
    ```

2.  **Eliminar o Mover el Directorio de Datos Existente:**
    **¡Advertencia!** Esto eliminará cualquier dato existente en el secundario. Si este es un servidor nuevo, no hay problema. Si ya tenía datos, asegúrate de hacer una copia de seguridad o de que no necesitas esos datos.

    ```bash
    rm -rf /var/lib/postgresql/<version>/main # O la ubicación de tu data directory
    ```
    La ubicación común del directorio de datos es `/var/lib/postgresql/<version>/main` o `/var/lib/pgsql/data`.

3.  **Copiar la Base de Datos Base del Primario:**
    Utiliza `pg_basebackup` para copiar la base de datos completa desde el primario. Ejecuta esto en el servidor **secundario**:

    ```bash
    pg_basebackup -h <IP_DEL_PRIMARIO> -D /var/lib/postgresql/<version>/main -U replicador -P -Xs -R
    ```
    * `-h <IP_DEL_PRIMARIO>`: Dirección IP del servidor primario.
    * `-D /var/lib/postgresql/<version>/main`: Directorio de datos del secundario (donde se copiarán los archivos).
    * `-U replicador`: Usuario de replicación que creaste en el primario.
    * `-P`: Muestra el progreso.
    * `-Xs`: Incluye los WALs de streaming.
    * `-R`: Crea automáticamente el archivo `standby.signal` (PostgreSQL 12+) o `recovery.conf` (versiones anteriores) necesario para la replicación.

    Se te pedirá la contraseña del usuario `replicador`.

    **Nota para PostgreSQL 11 y anteriores:** `pg_basebackup` creará un archivo llamado `recovery.conf` dentro del directorio de datos que contendrá la configuración de replicación. Asegúrate de que los parámetros de `primary_conninfo` y `restore_command` sean correctos si no usas `-R`.

    **Nota para PostgreSQL 12 y posteriores:** `pg_basebackup -R` creará un archivo `standby.signal` y un archivo `postgresql.auto.conf` con la cadena de conexión (`primary_conninfo`).

### Paso 3: Configuración Final en el Servidor Secundario

1.  **Verificar o Crear `standby.signal` (PostgreSQL 12+) / `recovery.conf` (PostgreSQL 11 y anteriores):**
    * **PostgreSQL 12+:** `pg_basebackup -R` debería haber creado `standby.signal` y `postgresql.auto.conf`. Si no, crea un archivo vacío llamado `standby.signal` en el directorio de datos. La cadena de conexión (`primary_conninfo`) estará en `postgresql.auto.conf`.
    * **PostgreSQL 11 y anteriores:** Abre el archivo `recovery.conf` (ubicado dentro del directorio de datos, creado por `pg_basebackup` con `-R`) y asegúrate de que contenga una línea similar a:

        ```ini
        standby_mode = on
        primary_conninfo = 'host=<IP_DEL_PRIMARIO> port=5432 user=replicador password=tu_contraseña_segura application_name=mi_replica'
        ```
        Ajusta `host`, `port`, `user`, `password` y `application_name` (un nombre descriptivo para tu réplica).

2.  **Editar `postgresql.conf` (Opcional pero Recomendado):**
    En el secundario, puedes ajustar `hot_standby_feedback = on` en `postgresql.conf` para evitar la cancelación de consultas largas en el secundario si el primario necesita limpiar tuplas que el secundario aún está leyendo.

3.  **Iniciar PostgreSQL:**
    Inicia el servicio PostgreSQL en el servidor secundario:

    ```bash
    sudo systemctl start postgresql
    ```

### Paso 4: Verificación

1.  **En el Primario:**
    Conéctate a PostgreSQL y verifica el estado de los `wal_senders`:

    ```sql
    SELECT client_addr, state, sync_state, sync_priority FROM pg_stat_replication;
    ```
    Deberías ver una entrada para tu réplica con `state = 'streaming'` y `sync_state = 'async'` (o `sync` si configuraste replicación síncrona, lo cual no cubrimos en esta guía rápida).

2.  **En el Secundario:**
    * Puedes verificar el progreso de la replicación mirando los logs de PostgreSQL.
    * Conéctate a la base de datos y realiza una consulta de lectura para asegurarte de que los datos estén siendo replicados. **¡Recuerda que el servidor secundario es de solo lectura mientras está en modo standby!**

    ```sql
    SELECT pg_is_in_recovery(); -- Debería devolver 't' (true)
    SELECT pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn(); -- Muestra la posición del WAL recibida y aplicada
    ```

---

### Consideraciones Adicionales y Pasos Siguientes:

* **Replicación Síncrona vs. Asíncrona:** Esta guía configura replicación asíncrona (por defecto). Para replicación síncrona, donde las transacciones en el primario no se confirman hasta que se escriben en el secundario, necesitarías ajustar `synchronous_standby_names` en el `postgresql.conf` del primario.
* **Archivado de WALs (`archive_mode`, `archive_command`):** Fundamental para Point-In-Time Recovery (PITR) y para evitar que el secundario se quede sin WALs si la replicación se interrumpe por un tiempo prolongado.
* **Herramientas de Alta Disponibilidad:** Para failover automático, considera herramientas como Patroni, repmgr, o pg_auto_failover.
* **Monitoreo:** Es crucial monitorear el estado de la replicación y el rendimiento de ambos servidores.
* **Seguridad:** Asegúrate de que tus contraseñas sean seguras y que `pg_hba.conf` esté configurado de forma restrictiva.

¡Espero que esta guía rápida te sea de gran utilidad para empezar con la replicación de PostgreSQL! ¿Hay algún otro tipo de replicación sobre el que te gustaría saber más, o alguna parte de esta guía que quisieras que profundizáramos?