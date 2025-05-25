# **Gestión de Usuarios en PostgreSQL:  Resumen de Comandos SQL**

En PostgreSQL, la gestión de usuarios se realiza a través de **roles**. Un rol es un concepto unificado que puede representar tanto a un usuario (una persona que inicia sesión) como a un grupo de permisos. La clave para diferenciar si un rol es un usuario o un grupo es el atributo `LOGIN`.

---

## **1. Creación de Roles (Usuarios o Grupos)**

Utilizamos el comando `CREATE ROLE` para crear nuevos roles.

* **Para crear un usuario (un rol que puede iniciar sesión):**

    ```sql
    CREATE ROLE nombre_usuario WITH LOGIN PASSWORD 'tu_contraseña_segura';
    ```

    Puedes añadir atributos adicionales para definir sus capacidades:

    ```sql
    CREATE ROLE admin_app WITH LOGIN SUPERUSER CREATEDB CREATEROLE PASSWORD 'otra_contraseña';
    ```

    * **`LOGIN`**: Permite al rol iniciar sesión en la base de datos.
    * **`PASSWORD '...'`**: Establece la contraseña para el rol.
    * **`SUPERUSER`**: Otorga todos los privilegios sobre el sistema (úsalos con extrema precaución).
    * **`CREATEDB`**: Permite al rol crear nuevas bases de datos.
    * **`CREATEROLE`**: Permite al rol crear, modificar o eliminar otros roles.
    * **`VALID UNTIL 'AAAA-MM-DD HH:MI:SS'`**: Establece una fecha de caducidad para la contraseña.

* **Para crear un grupo (un rol que NO puede iniciar sesión):**
    Estos roles se usan para agrupar permisos y asignarlos a otros roles con `LOGIN`.

    ```sql
    CREATE ROLE nombre_grupo NOLOGIN;
    ```

    * **`NOLOGIN`**: Impide que este rol inicie sesión directamente.

---

## **2. Modificación de Roles Existentes**

El comando `ALTER ROLE` permite cambiar los atributos de un rol ya existente.

```sql
ALTER ROLE nombre_rol WITH CREATEDB;         -- Otorga permiso para crear bases de datos
ALTER ROLE nombre_rol WITH NOLOGIN;          -- Quita la capacidad de login (lo convierte en grupo)
ALTER ROLE nombre_rol WITH PASSWORD 'nueva_contraseña'; -- Cambia la contraseña del rol
ALTER ROLE nombre_rol RENAME TO nuevo_nombre_rol; -- Cambia el nombre del rol
ALTER ROLE nombre_rol WITH NOSUPERUSER;      -- Revoca el atributo de superusuario
```

Para quitar un atributo, simplemente usa `NO` antes del nombre del atributo (ej., `NOSUPERUSER`, `NOCREATEDB`).

---

## **3. Eliminación de Roles**

El comando `DROP ROLE` elimina un rol del sistema de base de datos.
**Importante**: Un rol no puede ser eliminado si posee objetos en la base de datos. Primero, debes transferir la propiedad de esos objetos o eliminarlos.

```sql
DROP ROLE nombre_rol;
```

---

## **4. Gestión de Membresías (Asignar Usuarios a Grupos)**

Esto se refiere a hacer que un rol sea miembro de otro rol, heredando así sus privilegios. Se utiliza el comando `GRANT`.

```sql
GRANT nombre_grupo TO nombre_usuario;
```

* `nombre_grupo`: El rol cuyos permisos quieres otorgar (normalmente un rol `NOLOGIN`).
* `nombre_usuario`: El rol que recibirá esos permisos (normalmente un rol `LOGIN`).

Opcionalmente, puedes usar `WITH ADMIN OPTION` para permitir que `nombre_usuario` pueda, a su vez, otorgar la membresía de `nombre_grupo` a otros roles:

```sql
GRANT nombre_grupo TO nombre_usuario WITH ADMIN OPTION;
```

Para **revocar la membresía**:

```sql
REVOKE nombre_grupo FROM nombre_usuario;
```

---

## **5. Otorgar y Revocar Privilegios sobre Objetos**

Estos comandos son fundamentales para definir qué puede hacer un rol con tus bases de datos, tablas, esquemas, etc.

* **Conexión a una base de datos:**

    ```sql
    GRANT CONNECT ON DATABASE nombre_base_de_datos TO nombre_rol;
    ```

* **Uso de un esquema:**

    ```sql
    GRANT USAGE ON SCHEMA nombre_esquema TO nombre_rol;
    ```

* **Permisos sobre tablas (SELECT, INSERT, UPDATE, DELETE):**

    ```sql
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE nombre_tabla TO nombre_rol;
    ```

    Para otorgar todos los privilegios sobre una tabla:

    ```sql
    GRANT ALL PRIVILEGES ON TABLE nombre_tabla TO nombre_rol;
    ```

* **Permisos para futuras tablas en un esquema (privilegios por defecto):**
    Muy útil para que los nuevos objetos creados en un esquema otorguen automáticamente ciertos permisos.

    ```sql
    ALTER DEFAULT PRIVILEGES IN SCHEMA nombre_esquema GRANT SELECT ON TABLES TO nombre_rol;
    ALTER DEFAULT PRIVILEGES IN SCHEMA nombre_esquema GRANT INSERT, UPDATE ON TABLES TO nombre_rol;
    ```

* **Revocar privilegios:**

    ```sql
    REVOKE SELECT ON TABLE nombre_tabla FROM nombre_rol;
    REVOKE ALL PRIVILEGES ON DATABASE nombre_base_de_datos FROM nombre_rol;
    ```

---

## **6. Visualización de Roles y Permisos (desde `psql`)**

Estos son metacomandos de `psql` que facilitan la inspección.

* **Ver todos los roles existentes y sus atributos principales:**

    ```sql
    \du
    ```

    (Equivalente a `SELECT rolname, rolsuper, rolcreaterole, rolcreatedb, rolreplication, rolbypassrls, rolcatupdate FROM pg_roles;`)

* **Ver los permisos de un rol específico y su membresía:**

    ```sql
    \du+ nombre_rol
    ```

* **Ver los privilegios de una tabla (o vista):**

    ```sql
    \dp nombre_tabla
    ```

