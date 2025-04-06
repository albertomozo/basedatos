# README - Gestión de Usuarios con Python

Este programa permite gestionar usuarios utilizando diferentes métodos de acceso a datos:
- **Acceso secuencial (archivo de texto)**
- **Acceso indexado (usando índices en memoria)**
- **Acceso hash (usando `shelve`)**

Proporciona un menú interactivo donde se pueden agregar, listar y buscar usuarios.

## 📌 Requisitos

- Python 3.x
- No requiere librerías externas

## 📖 Ayuda
- [ **w3schools.com** manejo ficheros en python](https://www.w3schools.com/python/python_file_handling.asp)
- [ **w3schools.com** Formateo de print ](https://www.w3schools.com/python/python_string_formatting.asp)



## 📂 Archivos generados

El programa trabaja con los siguientes archivos:

1. **`usuarios.txt`** → Archivo de texto donde se almacenan los usuarios en formato CSV (`ID,Nombre,Email`).
2. **`usuarios_db.db`** → Base de datos hash generada por `shelve` para acceso rápido a los usuarios.

## 🚀 Cómo ejecutar el programa

Ejecuta el siguiente comando en la terminal:

```sh
python gestion_usuarios.py
```

Si usas Python 3 en sistemas donde `python` apunta a la versión 2:

```sh
python3 gestion_usuarios.py
```

## 🛠️ Funcionalidades del programa

1️⃣ **Agregar usuario** → Guarda el usuario en `usuarios.txt` y `usuarios_db.db`.
2️⃣ **Listar usuarios** → Muestra todos los usuarios guardados en `usuarios.txt`.
3️⃣ **Buscar usuario (Secuencial)** → Recorre `usuarios.txt` línea por línea para encontrar un usuario.
4️⃣ **Buscar usuario (Indexado)** → Carga índices en memoria para mejorar la búsqueda en `usuarios.txt`.
5️⃣ **Buscar usuario (Hash)** → Usa `shelve` para acceder a `usuarios_db.db` de forma eficiente.
6️⃣ **Salir** → Cierra el programa.

## 📜 Formato del archivo `usuarios.txt`

Cada línea contiene un usuario con el siguiente formato:

```
ID,Nombre,Email
1,Juan Pérez,juan@example.com
2,Ana Gómez,ana@example.com
```

## 🔑 Estructura de `usuarios_db.db`

Es una base de datos clave-valor (`ID → (Nombre, Email)`). Ejemplo:

```
{
  "1": ("Juan Pérez", "juan@example.com"),
  "2": ("Ana Gómez", "ana@example.com")
}
```

## 📝 Notas

- Si `usuarios.txt` no existe, el programa lo creará automáticamente.
- `usuarios_db.db` se genera al agregar usuarios por primera vez.
- La búsqueda hash es más rápida que la indexada y la secuencial.

¡Disfruta gestionando usuarios con Python! 🚀

## archivo usuarios_db.bak
El archivo usuarios_db.bak es un archivo de respaldo generado automáticamente por shelve, que se utiliza para almacenar datos en formato clave-valor en usuarios_db.db.

### 📌 Significado de los archivos generados por shelve
Cuando usas **shelve.open("usuarios_db")**, Python crea varios archivos en el mismo directorio:

**usuarios_db.db** → Archivo principal donde se almacenan los datos en formato clave-valor.
**usuarios_db.bak** → Archivo de respaldo de la base de datos, creado automáticamente cuando shelve guarda cambios.
**usuarios_db.dat** → Contiene los datos almacenados en shelve.
**usuarios_db.dir** → Índice de claves de la base de datos.
#### ¿Para qué sirve usuarios_db.bak?
Este archivo actúa como un respaldo de seguridad en caso de corrupción de datos en usuarios_db.db. Si la base de datos se daña, shelve podría intentar recuperarla desde .bak.

#### ¿Puedo eliminar usuarios_db.bak?
No es recomendable eliminarlo manualmente, ya que podría ser útil en caso de fallos. Sin embargo, si deseas limpiar los archivos, puedes eliminarlos todos (usuarios_db.*) y el programa los regenerará cuando lo ejecutes nuevamente.

Si necesitas visualizar los datos almacenados en usuarios_db.db, puedes abrirlo en Python de la siguiente manera:

```python

import shelve

with shelve.open("usuarios_db") as db:
    for key in db:
        print(f"ID: {key}, Datos: {db[key]}")
```
Esto mostrará el contenido de la base de datos de manera legible. 🚀







