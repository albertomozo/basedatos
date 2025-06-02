<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# puedes ponerme unos ejemplos para simular esos problemas en un BD MAriaDb

Aquí tienes ejemplos prácticos para simular algunos de los ataques más comunes en una base de datos MariaDB, especialmente centrados en la inyección SQL, que es uno de los vectores más frecuentes y peligrosos.

## Ejemplos de ataques para simular en MariaDB

**1. Inyección SQL clásica para evadir autenticación**
Supón que tienes un formulario de login con los campos `usuario` y `clave`. Si la consulta SQL es vulnerable, un atacante podría introducir en el campo de contraseña:

```
' OR 1=1 --
```

La consulta resultante sería:

```sql
SELECT * FROM usuarios WHERE usuario = 'cualquiera' AND clave = '' OR 1=1 --';
```

Esto permite el acceso sin necesidad de conocer la contraseña real, ya que la condición `1=1` siempre es verdadera[^5][^6].

**2. Inyección para modificar datos**
Si el sistema permite ejecutar múltiples sentencias, un atacante podría modificar datos. Por ejemplo, en un campo vulnerable, introducir:

```
'; UPDATE usuarios SET clave='nueva_clave' WHERE usuario='admin'; --
```

Esto ejecutaría un cambio de contraseña para el usuario 'admin'[^1][^5].

**3. Inyección para extraer información de otras tablas**
Utilizando la cláusula `UNION`, un atacante puede intentar obtener datos de otras tablas:

```
' UNION SELECT usuario, clave, 1 FROM usuarios WHERE '1'='1
```

Esto puede mostrar nombres de usuario y contraseñas en la salida de la consulta original, si la aplicación muestra los resultados en pantalla[^5][^6].

**4. Inyección SQL ciega (Blind SQL Injection)**
Para probar si existe una vulnerabilidad sin recibir mensajes de error visibles, se pueden usar condiciones booleanas:

```
' AND 1=1 --
' AND 1=2 --
```

Si la respuesta de la aplicación cambia, indica que es vulnerable a inyección ciega[^3][^7].

**5. Inyección basada en tiempo**
Para comprobar vulnerabilidades cuando no hay respuesta directa, puedes usar la función `SLEEP()` de MariaDB/MySQL:

```
1' OR SLEEP(5) --
```

Si la respuesta se retrasa, la base de datos es vulnerable a este tipo de ataques[^3].

---

> **Advertencia:** Estos ejemplos son solo para fines educativos y de pruebas controladas en entornos propios y nunca deben usarse en sistemas ajenos sin autorización expresa.

Estos ejemplos cubren los principales escenarios de ataque que puedes simular en una base de datos MariaDB para entender cómo funcionan y cómo protegerte de ellos[^1][^5][^6].

<div style="text-align: center">⁂</div>

[^1]: https://diego.com.es/ataques-sql-injection-en-php

[^2]: https://deephacking.tech/introduccion-sql-injection/

[^3]: https://kinsta.com/es/blog/inyeccion-sql/

[^4]: https://oa.upm.es/82654/1/TFG_SOFIA_ALEJANDRA_CADENAS_FERNANDEZ.pdf

[^5]: https://openaccess.uoc.edu/bitstream/10609/62886/1/Seguridad en bases de datos_M%C3%B3dulo%203_Ataques%20a%20BB.DD.,%20SQL%20Injection.pdf

[^6]: https://www.datacamp.com/es/tutorial/sql-injection

[^7]: https://blog.hostalia.com/hostalia/ataques-de-inyeccion-sql-que-son-y-como-protegerse/

[^8]: https://www.youtube.com/watch?v=KFU6aBh4hEU

