<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

## Ejemplo Práctico para Probar la Herramienta Schema Diff en pgAdmin

A continuación, te muestro un ejemplo sencillo para que puedas probar y entender cómo funciona la herramienta **Schema Diff** en pgAdmin:

---

**1. Prepara dos bases de datos o dos esquemas**

Supongamos que tienes dos bases de datos llamadas `db_origen` y `db_destino` en el mismo servidor PostgreSQL (o en servidores de la misma versión principal).

- En `db_origen`, crea una tabla llamada `clientes`:

```sql
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100)
);
```

- En `db_destino`, crea una tabla similar pero con una diferencia, por ejemplo, sin la columna `email`:

```sql
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100)
);
```


---

**2. Abre Schema Diff en pgAdmin**

- Ve al menú **Tools** y selecciona **Schema Diff**[^1][^3].
- Se abrirá un panel donde podrás elegir el **servidor**, la **base de datos** y el **esquema** de origen y destino que quieres comparar.

---

**3. Selecciona los objetos a comparar**

- En el panel de Schema Diff, selecciona como origen `db_origen` y como destino `db_destino` (puedes comparar bases de datos completas o solo esquemas específicos)[^1][^3].
- Haz clic en el botón **Compare**.

---

**4. Visualiza las diferencias**

- El sistema te mostrará las diferencias encontradas, por ejemplo, te indicará que en la tabla `clientes` del destino falta la columna `email`[^1][^3].
- Puedes navegar por las diferencias y ver el DDL de cada objeto en ambas bases de datos.

---

**5. Genera el script de sincronización**

- Marca la casilla de los objetos que quieres sincronizar (por ejemplo, la tabla `clientes`).
- Haz clic en **Generate Script** para que pgAdmin genere automáticamente el SQL necesario para igualar el destino al origen (en este caso, agregar la columna `email` a la tabla `clientes` en `db_destino`)[^1].
- El script se abrirá en una nueva pestaña del Query Tool para que lo revises y ejecutes si lo deseas.

---

**Resumen del flujo:**

1. Crea diferencias entre dos bases de datos o esquemas.
2. Abre **Tools > Schema Diff**.
3. Selecciona origen y destino.
4. Haz clic en **Compare**.
5. Visualiza diferencias y genera el script de sincronización.

---

Este flujo te permitirá probar y familiarizarte con la herramienta **Schema Diff** de pgAdmin de manera práctica y segura[^1][^3].

<div style="text-align: center">⁂</div>

[^1]: https://www.pgadmin.org/docs/pgadmin4/8.14/schema_diff.html

[^2]: https://www.youtube.com/watch?v=WB13t-3JSMc

[^3]: https://www.enterprisedb.com/blog/how-get-most-out-schema-diff-tool-pgadmin-4

[^4]: https://www.youtube.com/watch?v=FdOgKqpAtOU

[^5]: https://www.bytebase.com/blog/top-postgres-schema-compare-tools/

[^6]: https://www.youtube.com/watch?v=W0E-i0mWb6Y

[^7]: https://aws.amazon.com/es/compare/the-difference-between-mysql-vs-postgresql/

[^8]: https://github.com/orgs/supabase/packages/container/package/pgadmin-schema-diff

