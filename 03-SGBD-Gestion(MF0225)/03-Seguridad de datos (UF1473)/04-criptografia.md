# Supuestos Prácticos de Seguridad Criptográfica en Bases de Datos

A continuación, presento varios casos prácticos que ilustran la aplicación de los elementos de seguridad criptográfica que hemos visto anteriormente.

## Supuesto 1: Sistema de Historias Clínicas Electrónicas

**Contexto:** Un hospital necesita implementar un sistema de historias clínicas electrónicas que cumpla con normativas de protección de datos sanitarios (tipo HIPAA o RGPD).

**Requerimientos de seguridad:**
- Confidencialidad de datos médicos sensibles
- Integridad de la información clínica
- Autenticación segura del personal sanitario
- No repudio de las acciones realizadas
- Auditoría de accesos y modificaciones

**Solución implementada:**

1. **Confidencialidad:**
   - Implementación de cifrado TDE (Transparent Data Encryption) en SQL Server para todos los datos en reposo
   - Cifrado a nivel de columna para datos especialmente sensibles (como diagnósticos, medicación, VIH, salud mental)
   - Algoritmo AES-256 para el cifrado simétrico de los datos

2. **Autenticación:**
   - Sistema de autenticación multifactor para el personal médico:
     - Contraseña compleja + tarjeta inteligente con certificado digital
   - Implementación de directorio LDAP con autenticación Kerberos
   - Roles y permisos basados en la función del personal (médicos, enfermeras, administrativos)

3. **Integridad y No repudio:**
   - Firmas digitales basadas en RSA para todas las modificaciones de historias clínicas
   - Registro de auditoría cifrado e inmutable con sellado de tiempo
   - Verificación de integridad mediante hashes SHA-256 para detectar alteraciones no autorizadas

4. **Conexión segura:**
   - Toda conexión a la base de datos requiere TLS 1.3
   - VPN obligatoria para accesos remotos
   - Certificados X.509 para autenticar conexiones cliente-servidor

**Ejemplo práctico de código (SQL Server):**

```sql
-- Creación de certificado maestro para TDE
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'C0mpl3j@Cl@v3M@3str@!';

-- Creación de certificado para TDE
CREATE CERTIFICATE TDE_Cert WITH SUBJECT = 'Certificado para TDE de Historias Clínicas';

-- Creación de clave de cifrado de base de datos
CREATE DATABASE ENCRYPTION KEY
WITH ALGORITHM = AES_256
ENCRYPTION BY SERVER CERTIFICATE TDE_Cert;

-- Activar cifrado de la base de datos
ALTER DATABASE HistoriasClinicas
SET ENCRYPTION ON;

-- Creación de columna cifrada con Always Encrypted
CREATE TABLE Pacientes (
    ID_Paciente INT PRIMARY KEY,
    Nombre NVARCHAR(100) NOT NULL,
    Apellidos NVARCHAR(100) NOT NULL,
    FechaNacimiento DATE NOT NULL,
    DiagnosticoPrincipal NVARCHAR(500) ENCRYPTED WITH (
        ENCRYPTION_TYPE = DETERMINISTIC,
        ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256',
        COLUMN_ENCRYPTION_KEY = DiagnosticosCEK
    )
);
```

## Supuesto 2: Sistema de Pagos para Comercio Electrónico

**Contexto:** Una plataforma de e-commerce necesita gestionar información de pagos con tarjetas de crédito de manera segura, cumpliendo con el estándar PCI DSS.

**Requerimientos de seguridad:**
- Confidencialidad de los datos de tarjetas
- Protección contra manipulaciones fraudulentas
- Autenticación segura de usuarios y comercios
- Registro de transacciones no repudiable

**Solución implementada:**

1. **Confidencialidad de datos financieros:**
   - Cifrado de datos sensibles mediante PostgreSQL con pgcrypto
   - Almacenamiento cifrado de tokens en lugar de números completos de tarjetas
   - Cifrado asimétrico RSA para intercambio de claves de sesión

2. **Integridad de transacciones:**
   - Funciones hash HMAC para verificar integridad de mensajes de transacción
   - Firmas digitales para autorización de pagos
   - Checksums en transferencias de datos entre sistemas

3. **Autenticación y No repudio:**
   - Certificados digitales para autenticación mutua entre sistemas
   - Sistema de tokens JWT con firma para sesiones
   - Registros de auditoría firmados digitalmente y con timestamp

4. **Conexiones seguras:**
   - TLS 1.3 obligatorio para todas las conexiones
   - Exclusión de cifrados débiles en la configuración SSL
   - Renovación automática de certificados para evitar caducidades

**Ejemplo práctico de código (PostgreSQL):**

```sql
-- Instalación de extensión pgcrypto
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Creación de tabla de tarjetas con cifrado
CREATE TABLE informacion_pago (
    id_cliente INT PRIMARY KEY,
    nombre_titular VARCHAR(100) NOT NULL,
    token_tarjeta VARCHAR(100) NOT NULL,
    -- Solo se almacenan los últimos 4 dígitos
    ultimos_digitos CHAR(4) NOT NULL,
    -- Datos sensibles cifrados con clave simétrica
    datos_adicionales BYTEA,
    fecha_expiracion VARCHAR(5) NOT NULL
);

-- Función para insertar datos cifrados
CREATE OR REPLACE FUNCTION insertar_datos_pago(
    p_id_cliente INT,
    p_nombre VARCHAR,
    p_numero_tarjeta VARCHAR,
    p_fecha_exp VARCHAR,
    p_datos_adicionales TEXT,
    p_clave_cifrado VARCHAR
) RETURNS VOID AS $$
DECLARE
    v_ultimos_digitos CHAR(4);
    v_token VARCHAR;
BEGIN
    -- Obtener últimos 4 dígitos
    v_ultimos_digitos := SUBSTRING(p_numero_tarjeta FROM LENGTH(p_numero_tarjeta)-3);
    
    -- Generar token (en producción se usaría un sistema de tokenización)
    v_token := ENCODE(DIGEST(p_numero_tarjeta || RANDOM()::TEXT, 'sha256'), 'hex');
    
    -- Insertar datos con cifrado
    INSERT INTO informacion_pago VALUES (
        p_id_cliente,
        p_nombre,
        v_token,
        v_ultimos_digitos,
        ENCRYPT(p_datos_adicionales::BYTEA, p_clave_cifrado::BYTEA, 'aes'),
        p_fecha_exp
    );
    
    -- Registrar la acción en log de auditoría con firma
    PERFORM registrar_auditoria(
        'INSERTAR_PAGO',
        p_id_cliente::TEXT,
        CURRENT_USER,
        ENCODE(HMAC(p_id_cliente::TEXT || v_token, p_clave_cifrado, 'sha256'), 'hex')
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

## Supuesto 3: Sistema Bancario con Alta Disponibilidad

**Contexto:** Un banco requiere implementar un sistema para transacciones bancarias con alta disponibilidad y máxima seguridad.

**Requerimientos:**
- Confidencialidad extrema de los datos financieros
- Integridad verificable de todas las transacciones
- Autenticación robusta y no repudio de operaciones
- Protección contra ataques de intermediario (MITM)

**Solución implementada:**

1. **Infraestructura de seguridad:**
   - Oracle Database con Oracle Advanced Security
   - Sistema de HSM (Hardware Security Module) para almacenamiento seguro de claves
   - Cifrado híbrido: asimétrico para intercambio de claves, simétrico para datos

2. **Confidencialidad:**
   - TDE para cifrado de toda la base de datos en reposo
   - Enmascaramiento dinámico de datos según nivel de acceso del usuario
   - Cifrado de columnas críticas con Oracle Advanced Security

3. **Integridad y No repudio:**
   - Firma digital de cada transacción con RSA-4096
   - Registros de blockchain privado para el historial inmutable de transacciones
   - Sellado de tiempo certificado para cada operación financiera

4. **Conexiones seguras:**
   - mTLS (TLS mutuo) obligatorio para todas las conexiones
   - Rotación automática de claves cada 24 horas
   - Lista blanca de IPs permitidas

**Ejemplo práctico de código (Oracle):**

```sql
-- Configuración de Oracle Wallet para almacenar claves TDE
ALTER SYSTEM SET ENCRYPTION WALLET OPEN IDENTIFIED BY "P@55w0rdS3gur@";

-- Creación de tablespace cifrado
CREATE TABLESPACE datos_financieros
DATAFILE '/u01/app/oracle/oradata/ORCL/datos_fin01.dbf'
SIZE 100M
ENCRYPTION USING 'AES256'
DEFAULT STORAGE(ENCRYPT);

-- Tabla de transacciones con columnas cifradas
CREATE TABLE transacciones_bancarias (
    id_transaccion NUMBER PRIMARY KEY,
    cuenta_origen VARCHAR2(20) NOT NULL,
    cuenta_destino VARCHAR2(20) NOT NULL,
    importe NUMBER(12,2) ENCRYPT USING 'AES256',
    fecha_hora TIMESTAMP WITH TIME ZONE DEFAULT SYSTIMESTAMP,
    concepto VARCHAR2(100) ENCRYPT USING 'AES256',
    firma_digital RAW(256),
    hash_operacion RAW(64)
) TABLESPACE datos_financieros;

-- Procedimiento para realizar transacción con firma y hash
CREATE OR REPLACE PROCEDURE realizar_transaccion (
    p_origen VARCHAR2,
    p_destino VARCHAR2,
    p_importe NUMBER,
    p_concepto VARCHAR2
) AS
    v_id_transaccion NUMBER;
    v_datos_transaccion VARCHAR2(4000);
    v_hash RAW(64);
    v_firma RAW(256);
BEGIN
    -- Generar ID de transacción
    SELECT seq_transacciones.NEXTVAL INTO v_id_transaccion FROM DUAL;
    
    -- Datos para firmar y verificar
    v_datos_transaccion := p_origen || '|' || p_destino || '|' || 
                          TO_CHAR(p_importe) || '|' || p_concepto || '|' ||
                          TO_CHAR(SYSTIMESTAMP, 'YYYY-MM-DD HH24:MI:SS.FF');
    
    -- Generar hash SHA-512
    v_hash := DBMS_CRYPTO.HASH(
                UTL_RAW.CAST_TO_RAW(v_datos_transaccion),
                DBMS_CRYPTO.HASH_SH512);
    
    -- Firma digital (en producción se usaría HSM)
    v_firma := firma_digital_hsm(v_hash);
    
    -- Insertar transacción
    INSERT INTO transacciones_bancarias (
        id_transaccion, cuenta_origen, cuenta_destino,
        importe, concepto, firma_digital, hash_operacion
    ) VALUES (
        v_id_transaccion, p_origen, p_destino,
        p_importe, p_concepto, v_firma, v_hash
    );
    
    -- Registrar en blockchain privado del banco
    registrar_en_blockchain(v_id_transaccion, v_hash);
    
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        registrar_error(SQLCODE, SQLERRM, 'realizar_transaccion');
        RAISE;
END;
/
```

## Supuesto 4: Sistema de Votación Electrónica

**Contexto:** Una organización necesita implementar un sistema de votación electrónica para sus elecciones internas, garantizando anonimato y verificabilidad.

**Requerimientos:**
- Anonimato de los votantes (disociación entre identidad y voto)
- Integridad completa del proceso electoral
- Verificabilidad de resultados sin comprometer el secreto del voto
- No repudio de participación en el proceso

**Solución implementada:**

1. **Arquitectura de seguridad:**
   - Sistema basado en MariaDB con cifrado nativo
   - Separación física de bases de datos de identidades y votos
   - Protocolo de cifrado homomórfico para recuento sin descifrado individual

2. **Confidencialidad y anonimato:**
   - Cifrado del voto con clave pública electoral (asimétrica)
   - Generación de tokens anónimos firmados para autorización
   - Zero-Knowledge Proofs para verificar elegibilidad sin revelar identidad

3. **Integridad y verificabilidad:**
   - Hash de cada voto incluido en un registro inmutable (blockchain)
   - Sistema de firmas ciegas para autorización sin vinculación
   - Recibos de votación verificables sin revelar el contenido

4. **Conexión y autenticación:**
   - Autenticación multifactor para acceder al sistema
   - Canal seguro TLS 1.3 con Perfect Forward Secrecy
   - Red privada segregada para el sistema electoral

**Ejemplo práctico de código (MariaDB):**

```sql
-- Activar cifrado de conexiones
SET GLOBAL ssl_cipher = 'TLSv1.3:ECDHE-RSA-AES256-GCM-SHA384';

-- Tabla de votantes (en una base de datos separada)
CREATE TABLE votantes (
    id_votante INT AUTO_INCREMENT PRIMARY KEY,
    hash_identidad VARCHAR(128) NOT NULL,
    token_firmado VARCHAR(256) NOT NULL,
    ha_votado BOOLEAN DEFAULT FALSE,
    timestamp_autenticacion DATETIME,
    INDEX (hash_identidad)
);

-- Tabla de votos (en otra base de datos física)
CREATE TABLE votos (
    id_voto INT AUTO_INCREMENT PRIMARY KEY,
    token_validacion VARCHAR(256) NOT NULL,
    voto_cifrado BLOB NOT NULL,
    hash_voto VARCHAR(128) NOT NULL,
    timestamp_voto DATETIME DEFAULT CURRENT_TIMESTAMP,
    firma_ciega VARCHAR(256) NOT NULL,
    INDEX (token_validacion)
);

-- Procedimiento para emitir voto anónimo
DELIMITER //
CREATE PROCEDURE emitir_voto(
    IN p_token_firmado VARCHAR(256),
    IN p_voto_cifrado BLOB,
    IN p_prueba_zkp VARCHAR(1024)
)
BEGIN
    DECLARE v_token_valido BOOLEAN DEFAULT FALSE;
    DECLARE v_token_validacion VARCHAR(256);
    DECLARE v_hash_voto VARCHAR(128);
    
    -- Iniciar transacción
    START TRANSACTION;
    
    -- Verificar token en base de datos de votantes
    SELECT COUNT(*) > 0, UUID() INTO v_token_valido, v_token_validacion
    FROM votantes 
    WHERE token_firmado = p_token_firmado 
    AND ha_votado = FALSE;
    
    -- Si el token es válido, registrar voto
    IF v_token_valido THEN
        -- Actualizar estado del votante
        UPDATE votantes 
        SET ha_votado = TRUE, 
            timestamp_autenticacion = NOW() 
        WHERE token_firmado = p_token_firmado;
        
        -- Calcular hash del voto cifrado
        SET v_hash_voto = SHA2(p_voto_cifrado, 512);
        
        -- Insertar voto anónimo
        INSERT INTO votos (
            token_validacion,
            voto_cifrado,
            hash_voto,
            firma_ciega
        ) VALUES (
            v_token_validacion,
            p_voto_cifrado,
            v_hash_voto,
            firma_digital_ciega(v_hash_voto, p_prueba_zkp)
        );
        
        -- Registrar hash en blockchain público
        CALL registrar_hash_blockchain(v_hash_voto);
        
        COMMIT;
        
        -- Devolver recibo de votación
        SELECT v_token_validacion AS recibo, v_hash_voto AS verificador;
    ELSE
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Token inválido o ya utilizado';
    END IF;
END //
DELIMITER ;
```

Estos supuestos prácticos ilustran cómo se implementan las diferentes técnicas criptográficas en contextos reales de bases de datos, abordando requisitos específicos de confidencialidad, integridad, autenticación y no repudio según las necesidades de cada aplicación.