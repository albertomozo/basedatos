## Comparativa de MariaDB, SQLite y PostgreSQL

**Configuración y Propiedades**


| Característica | MariaDB | SQLite | PostgreSQL |
| :-- | :-- | :-- | :-- |
| Tipo de SGBD | Relacional, cliente-servidor | Relacional, embebido | Relacional, objeto-relacional |
| Licencia | GPL | Dominio público | PostgreSQL License (similar a BSD/MIT) |
| Arquitectura | Multi-hilo | Serverless | Multi-proceso |
| Almacenamiento | Múltiples motores (InnoDB, MyISAM, etc.) | Archivo único | MVCC (Multiversion Concurrency Control) |

**Estructura de Carpetas**

- **MariaDB**:
    - /etc/mysql/ (configuración)
    - /var/lib/mysql/ (datos)
    - /var/log/mysql/ (logs)
- **SQLite**:
    - No tiene estructura de carpetas fija (archivo único)
- **PostgreSQL**:
    - /etc/postgresql/ (configuración)
    - /var/lib/postgresql/ (datos)
    - /var/log/postgresql/ (logs)

**Archivos de Configuración Principal**

- MariaDB: my.cnf
- SQLite: No tiene (configuración en tiempo de compilación o en la aplicación)
- PostgreSQL: postgresql.conf, pg_hba.conf

**Puertos por Defecto**

- MariaDB: 3306
- SQLite: N/A (no usa conexiones de red)
- PostgreSQL: 5432

**Herramientas de Administración**

- MariaDB: phpMyAdmin, MySQL Workbench
- SQLite: SQLite Browser, SQLite Studio
- PostgreSQL: pgAdmin, DBeaver

**Tipos de Datos Específicos**

- MariaDB: ENUM, SET
- SQLite: Tipado dinámico
- PostgreSQL: ARRAY, HSTORE, JSON, UUID

**Características Únicas**

- MariaDB: Compatibilidad con MySQL, Galera Cluster
- SQLite: Portabilidad, cero configuración
- PostgreSQL: Extensibilidad, soporte para datos geoespaciales (PostGIS)

Esta estructura proporciona una base sólida para tu presentación comparativa. Puedes expandir cada sección con más detalles y ejemplos específicos según sea necesario para tus ejercicios y documentación adjunta. Recuerda utilizar elementos visuales como iconos o códigos de color para mejorar la legibilidad y el impacto visual de tu cheatsheet en Google Slides.





[Maria DB]( https://mariadb.com/kb/en/configuring-mariadb-with-option-files/)

[^3]: https://stackoverflow.com/questions/54565945/how-to-represent-nested-folder-subfolder-structure-in-sqlite-database

[^4]: https://www.postgresql.org/docs/current/runtime-config-file-locations.html

[diferencias entre los SGBD](https://www.bitsathy.ac.in/choosing-between-postgresql-mariadb-and-sqlite/)

[^6]: https://sqlite.org/forum/info/3063ec0d633226451a46ad4eb29b64c438f256e7db535136b84cac084cb58ee7

[^7]: https://www.postgresql.org/docs/current/storage-file-layout.html

[^8]: https://www.opensourceforu.com/2023/08/choosing-between-postgresql-mariadb-and-sqlite/

[^9]: https://www.cartodruid.es/en/-/importacion-de-ficheros-sqlite-a-cartodruid

[^10]: https://mariadb.com/kb/en/understanding-mariadb-architecture/

[^11]: https://docs.keeper.io/en/keeper-connection-manager/advanced-configuration/guacamole.properties/mysql-mariadb-configuration-properties

[^12]: https://docs.cerebrohq.com/en/articles/3349437-database-file-structure-location

[^13]: https://www.datacamp.com/blog/sqlite-vs-postgresql-detailed-comparison

[^14]: https://stackoverflow.com/questions/59547067/what-is-the-configuration-file-of-mariadb

[^15]: https://github.com/xerial/sqlite-jdbc/blob/master/USAGE.md

[^16]: https://docs.hevodata.com/destinations/databases/postgresql/postgresql-data-structure/

[^17]: https://db-engines.com/en/system/MariaDB;PostgreSQL;SQLite

[^18]: https://docs.cloudera.com/cem/1.5.1/installation/topics/cem-install-configure-mariadb.html

[^19]: https://www.sqlite.org/different.html

[^20]: https://docs.keeper.io/en/keeper-connection-manager/advanced-configuration/guacamole.properties/postgresql-configuration-properties

[^21]: https://www.digitalocean.com/community/tutorials/sqlite-vs-mysql-vs-postgresql-a-comparison-of-relational-database-management-systems


