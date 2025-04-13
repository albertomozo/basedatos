

# me guistaria tambien una guia rápida de la consola de mongodb

Aquí tienes una guía rápida para usar la consola de MongoDB (Mongo Shell) con ejemplos paso a paso:

---

### **1. Iniciar el servidor MongoDB**

Primero, inicia el servidor de MongoDB. Abre una terminal y ejecuta:

```bash
mongod
```

Esto iniciará el servidor y lo dejará escuchando en el puerto predeterminado (`27017`).

---

### **2. Conectarse al servidor**

Abre otra terminal y ejecuta el siguiente comando para conectarte al servidor:

```bash
mongo
```

Esto abrirá el Mongo Shell, donde podrás interactuar con tu base de datos.

---

### **3. Listar las bases de datos existentes**

Para ver todas las bases de datos disponibles en el servidor, usa:

```bash
show dbs
```

Ejemplo de salida:

```
admin   0.000GB
config  0.002GB
local   0.000GB
```

---

### **4. Cambiar o crear una base de datos**

Para cambiar a una base de datos existente o crear una nueva, utiliza el comando `use`:

```bash
use mi_base_de_datos
```

Si la base de datos no existe, se creará automáticamente cuando insertes datos.

---

### **5. Mostrar las colecciones dentro de una base de datos**

Después de cambiar a una base de datos, puedes listar las colecciones con:

```bash
show collections
```

---

### **6. Crear una colección**

Puedes crear manualmente una colección con el comando `db.createCollection`:

```bash
db.createCollection("mi_coleccion")
```

---

### **7. Insertar documentos**

Para insertar un documento en una colección, usa `insertOne` o `insertMany`.

#### Insertar un documento único:

```bash
db.mi_coleccion.insertOne({nombre: "Juan", edad: 30, ciudad: "Madrid"})
```


#### Insertar múltiples documentos:

```bash
db.mi_coleccion.insertMany([
  {nombre: "Ana", edad: 25, ciudad: "Barcelona"},
  {nombre: "Luis", edad: 35, ciudad: "Valencia"}
])
```

---

### **8. Consultar documentos**

Para buscar documentos en una colección, usa `find`.

#### Consultar todos los documentos:

```bash
db.mi_coleccion.find()
```


#### Consultar documentos específicos:

```bash
db.mi_coleccion.find({ciudad: "Madrid"})
```

---

### **9. Actualizar documentos**

Para actualizar un documento, usa `updateOne` o `updateMany`.

#### Actualizar un documento:

```bash
db.mi_coleccion.updateOne(
  {nombre: "Juan"},
  {$set: {edad: 31}}
)
```


#### Actualizar múltiples documentos:

```bash
db.mi_coleccion.updateMany(
  {ciudad: "Valencia"},
  {$set: {ciudad: "Sevilla"}}
)
```

---

### **10. Eliminar documentos**

Para eliminar uno o varios documentos, usa `deleteOne` o `deleteMany`.

#### Eliminar un documento:

```bash
db.mi_coleccion.deleteOne({nombre: "Juan"})
```


#### Eliminar múltiples documentos:

```bash
db.mi_coleccion.deleteMany({ciudad: "Sevilla"})
```

---

### **11. Eliminar una colección**

Si deseas eliminar completamente una colección:

```bash
db.mi_coleccion.drop()
```

---

### **12. Eliminar una base de datos**

Para eliminar toda la base de datos actual:

```bash
db.dropDatabase()
```

---

### Comandos básicos resumidos

| Comando | Descripción |
| :-- | :-- |
| `show dbs` | Lista todas las bases de datos |
| `use &lt;nombre_db&gt;` | Cambia o crea una base de datos |
| `show collections` | Lista todas las colecciones en la base actual |
| `db.createCollection()` | Crea una nueva colección |
| `db.&lt;colección&gt;.insertOne()` | Inserta un documento único |
| `db.&lt;colección&gt;.find()` | Consulta documentos |
| `db.&lt;colección&gt;.updateOne()` | Actualiza un documento |
| `db.&lt;colección&gt;.deleteOne()` | Elimina un documento |
| `db.dropDatabase()` | Elimina la base de datos actual |

Esta guía te permitirá realizar operaciones básicas y esenciales en Mongo Shell para gestionar bases de datos MongoDB eficientemente.

<div>⁂</div>

[^1]: https://makeitrealcamp.gitbook.io/guias-de-make-it-real/bases-de-datos/mongodb

[^2]: https://www.ionos.es/digitalguide/paginas-web/desarrollo-web/mongodb-commands/

[^3]: https://www.freecodecamp.org/espanol/news/como-empezar-a-utilizar-mongodb-en-10-minutos/

[^4]: https://www.tutorialesprogramacionya.com/mongodbya/detalleconcepto.php?punto=6\&codigo=6\&inicio=0

[^5]: https://imaginaformacion.com/tutoriales/comandos-mas-importantes-de-mongodb

[^6]: https://geekflare.com/es/mongodb-queries-examples/

[^7]: https://www.youtube.com/watch?v=uunuOg812Zk

[^8]: https://github.com/AlanIsaacV/MongoDB

[^9]: https://jolugama.com/blog/2021/05/24/mongodb-tutorial-basico/

