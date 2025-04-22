<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

## Estrategias para manejar columnas de tipo fecha en SQLite

SQLite no tiene un tipo de dato dedicado para fechas (`DATE` o `DATETIME`). Sin embargo, ofrece varias estrategias y funciones para almacenar y manipular valores de fecha y hora de manera eficiente y flexible[^1][^5][^7].

**¿Cómo almacena SQLite los valores de fecha y hora?**

SQLite permite almacenar fechas y horas en cualquiera de estos tres formatos, usando los tipos de columna `TEXT`, `REAL` o `INTEGER`:

- **TEXT:** Usando el formato ISO-8601, por ejemplo `'2025-05-29 14:16:00'` o `'2025-05-29'`.
- **REAL:** Como número juliano (días desde el 24 de noviembre de 4714 a.C.), útil para cálculos astronómicos.
- **INTEGER:** Como timestamp Unix (segundos desde el 1 de enero de 1970)[^1][^2][^7].

Puedes declarar una columna como `DATE`, `DATETIME`, `TIMESTAMP` o cualquier nombre, pero internamente SQLite solo aplica una "afinidad de tipo" (usualmente NUMERIC) y no restringe el contenido. Por ejemplo, puedes poner cualquier valor en una columna declarada como `DATE`[^5].

---

## Estrategias recomendadas

**1. Usar formato TEXT (ISO-8601)**

- Almacena la fecha como texto: `'YYYY-MM-DD'` o `'YYYY-MM-DD HH:MM:SS'`.
- Ventajas: Legible, compatible con las funciones de fecha de SQLite, fácil de comparar y filtrar.
- Ejemplo:

```sql
CREATE TABLE eventos (
  id INTEGER PRIMARY KEY,
  fecha_evento TEXT
);
INSERT INTO eventos (fecha_evento) VALUES ('2025-04-22');
SELECT * FROM eventos WHERE fecha_evento &gt; '2025-01-01';
```

- Este es el método más común y recomendado para la mayoría de los casos[^2][^8].

**2. Usar formato INTEGER (timestamp Unix)**

- Almacena la fecha como número entero (segundos desde 1970-01-01).
- Ventajas: Eficiente en espacio, fácil de calcular diferencias, útil para orden cronológico.
- Ejemplo:

```sql
CREATE TABLE logs (
  id INTEGER PRIMARY KEY,
  fecha_log INTEGER
);
INSERT INTO logs (fecha_log) VALUES (strftime('%s','now'));
SELECT * FROM logs WHERE fecha_log &gt; strftime('%s','2025-01-01');
```

- Útil si necesitas cálculos de intervalos o interoperabilidad con sistemas Unix[^1][^2].

**3. Usar formato REAL (julian day)**

- Almacena la fecha como número real (días julianos).
- Menos común, pero útil para cálculos astronómicos o diferencias de fechas precisas[^1][^2].

---

## Funciones de fecha y hora en SQLite

SQLite incluye funciones integradas para manipular y consultar fechas, independientemente del formato elegido (siempre que uses los formatos esperados):

- `date()`: Devuelve la fecha en formato `'YYYY-MM-DD'`.
- `time()`: Devuelve la hora en formato `'HH:MM:SS'`.
- `datetime()`: Devuelve fecha y hora en formato `'YYYY-MM-DD HH:MM:SS'`.
- `strftime()`: Permite formatear la fecha/hora a tu gusto.
- `julianday()`: Devuelve el número juliano.
- `timediff()`: Calcula la diferencia entre dos fechas[^1][^2][^3][^6][^7].

**Ejemplo de uso de funciones:**

```sql
SELECT date('now'); -- Fecha actual
SELECT datetime('now', '+1 day'); -- Mañana
SELECT strftime('%d/%m/%Y', 'now'); -- Fecha en formato DD/MM/YYYY
SELECT julianday('now'); -- Día juliano actual
```


---

## Buenas prácticas y consideraciones

- **Consistencia:** Usa siempre el mismo formato en una columna para evitar errores de comparación y conversión[^4].
- **Validación:** Si quieres restringir el formato, utiliza restricciones `CHECK` en la definición de la tabla.
- **Comparaciones:** Si almacenas fechas como texto en formato ISO-8601, las comparaciones y ordenamientos funcionarán correctamente.
- **Conversión:** Usa las funciones de fecha para convertir entre formatos según lo necesites en tus consultas.

---

## Resumen

SQLite no tiene un tipo de columna `DATE` real, pero puedes almacenar fechas como `TEXT` (ISO-8601), `INTEGER` (timestamp Unix) o `REAL` (julian day). Usa las funciones integradas (`date()`, `datetime()`, `strftime()`, etc.) para manipular y consultar estos valores. El formato más simple y compatible es el texto ISO-8601, pero elige el que mejor se adapte a tus necesidades y mantén la consistencia en tu base de datos[^1][^2][^5][^7][^8].

<div style="text-align: center">⁂</div>

[^1]: https://www.sqlite.org/lang_datefunc.html

[^2]: https://www.w3resource.com/sqlite/snippets/sqlite-date-functions-explained.php

[^3]: https://www.geeksforgeeks.org/sqlite-date-and-time/

[^4]: https://stackoverflow.com/questions/31667495/whats-the-most-efficient-way-to-handle-datetimes-especially-since-a-column-of

[^5]: https://stackoverflow.com/questions/65596276/does-sqlite-actually-support-date-type

[^6]: https://www.sql-easy.com/learn/sqlite-date-time/

[^7]: https://sqlite.org/lang_datefunc.html

[^8]: https://www.sqlitetutorial.net/sqlite-date/

[^9]: https://www.sqlite.org/forum/info/5203f28a039a028754fda31591bbfb3c9ca9a949277cb45d789a2f78aecbd52f?t=h

[^10]: https://www.sqlite.org/datatype3.html

[^11]: https://sqlite.org/forum/info/fc9a1d37e56712e2

[^12]: https://www.youtube.com/watch?v=DQsBxP6VkFw

[^13]: https://www.reddit.com/r/sqlite/comments/16a37kr/date_or_numeric_or_text/

[^14]: https://support.atlassian.com/analytics/docs/sqlite-date-and-time-functions/

[^15]: https://www.sqlitetutorial.net/sqlite-date-functions/sqlite-date-function/

[^16]: https://www.sqlite.org/forum/info/5203f28a039a028754fda31591bbfb3c9ca9a949277cb45d789a2f78aecbd52f?t=h

[^17]: https://4js.com/online_documentation/fjs-fgl-3.00.05-manual-html/c_fgl_odiagsqt_005.html

[^18]: https://www.reddit.com/r/SQL/comments/18m1ady/what_data_type_should_i_use_for_a_date_in_db/

[^19]: https://www.sqlitetutorial.net/sqlite-date-functions/

[^20]: https://sqlite.org/lang_datefunc.html

[^21]: https://stackoverflow.com/questions/31761047/what-difference-between-the-date-time-datetime-and-timestamp-types

[^22]: https://community.appinventor.mit.edu/t/how-do-you-work-with-date-field-in-sqlite/78964

[^23]: https://sqlite-users.sqlite.narkive.com/af9RSJwH/sqlite-best-practice-storing-dates

[^24]: https://stackoverflow.com/questions/17227110/datetime-values-in-sqlite

[^25]: https://forum.xojo.com/t/best-practices-for-date-timestamps-and-sqlite-queries/46053

[^26]: https://www.autoitscript.com/forum/topic/182930-best-way-to-store-dates-in-sqlite/

[^27]: https://www.reddit.com/r/learnprogramming/comments/14g7urz/what_is_your_preferred_way_to_store_a_date_in/

[^28]: https://developer.android.com/topic/performance/sqlite-performance-best-practices

[^29]: https://www.tutorialspoint.com/sqlite/sqlite_date_time.htm

[^30]: https://github.com/pocketbase/pocketbase/discussions/1067

[^31]: https://sqldocs.org/sqlite-database/sqlite-datetime/

[^32]: https://www.youtube.com/watch?v=nJRvz5Rhrx0

[^33]: https://www.internotes.net/sqlite-dates

[^34]: https://stackoverflow.com/questions/52578666/how-to-select-sqlite-columns-based-on-date-from-date-column

[^35]: https://www.sqlitetutorial.net/sqlite-date-functions/sqlite-current_timestamp/

[^36]: https://www.sql-easy.com/learn/sqlite-date-time/

