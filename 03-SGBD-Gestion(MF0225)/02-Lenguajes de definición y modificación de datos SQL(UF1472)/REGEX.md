# REGEX

### 🔹 **1. MySQL / MariaDB**

Usa `REGEXP` o `RLIKE`.

```sql
SELECT * FROM usuarios WHERE nombre REGEXP '^A.*z$';
```

* Busca nombres que empiecen por "A" y terminen en "z".
* Soporta expresiones regulares similares a POSIX.

#### Ejemplo:

```sql
SELECT * FROM empleados WHERE email REGEXP '^[a-z0-9._%+-]+@empresa\\.com$';
```

---

### 🔹 **2. PostgreSQL**

Usa `~` para REGEX case-sensitive y `~*` para case-insensitive.

```sql
SELECT * FROM productos WHERE descripcion ~ '^[A-Z].*final$';
```

* `~`: distingue mayúsculas.
* `~*`: ignora mayúsculas/minúsculas.

#### Otros operadores útiles:

* `!~` → no coincide (case-sensitive)
* `!~*` → no coincide (case-insensitive)

---

### 🔹 **3. SQLite**

SQLite **soporta REGEXP solo si se implementa como función externa**. Por defecto, `REGEXP` no está implementado en SQLite. Puedes agregar soporte compilando con la función `regexp()` tú mismo, o usar `LIKE`/`GLOB` como alternativas básicas.

---

### 🔹 **4. Oracle**

Oracle usa la función `REGEXP_LIKE`.

```sql
SELECT * FROM clientes WHERE REGEXP_LIKE(telefono, '^[0-9]{9}$');
```

---

### 🔹 **5. SQL Server**

Usa `LIKE` para patrones simples, pero **no tiene soporte nativo para REGEX**. Puedes:

* Usar funciones CLR (C#) para extender funcionalidades.
* O, desde SQL Server 2016+, usar `STRING_SPLIT`, `TRANSLATE` y otras funciones para lógica más compleja, pero **REGEX puro requiere extensión externa**.

---

### ✅ Comparación rápida

| SGBD       | Soporte REGEX | Sintaxis básica                   |
| ---------- | ------------- | --------------------------------- |
| MySQL      | ✅ Sí          | `REGEXP` o `RLIKE`                |
| PostgreSQL | ✅ Sí          | `~`, `~*`, `!~`, `!~*`            |
| SQLite     | ⚠️ Limitado   | `REGEXP` solo con extensión       |
| Oracle     | ✅ Sí          | `REGEXP_LIKE(campo, 'expresión')` |
| SQL Server | ❌ Nativo no   | Requiere funciones externas (CLR) |

---


