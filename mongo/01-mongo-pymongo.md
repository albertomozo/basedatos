# libreria pymongo 

Hay varias librerias para acceder a Mongo, pero la más sencilla para empezae el pymongo

https://pymongo.readthedocs.io/en/stable/index.html


## Guía rápida para usar **PyMongo** con ejemplos paso a paso:

---

### **1. Instalación de PyMongo**

Primero, instala la librería usando `pip`:

```bash
python -m pip install pymongo
```

---

### **2. Conexión a MongoDB**

Conéctate al servidor de MongoDB utilizando `MongoClient`:

```python
from pymongo import MongoClient

# Conexión al servidor local
client = MongoClient("mongodb://localhost:27017/")
print("Conexión exitosa a MongoDB")

# Listar las bases de datos disponibles
databases = client.list_database_names()
print("Bases de datos disponibles:", databases)
```

---

### **3. Crear o acceder a una base de datos**

Si la base de datos no existe, MongoDB la creará automáticamente al insertar datos.

```python
db = client["mi_base_de_datos"]
print("Base de datos seleccionada:", db.name)
```

---

### **4. Crear o acceder a una colección**

Las colecciones también se crean automáticamente al insertar documentos.

```python
coleccion = db["mi_coleccion"]
print("Colección seleccionada:", coleccion.name)
```

---

### **5. Insertar documentos**

Puedes insertar uno o varios documentos en una colección.

#### Insertar un documento único:

```python
documento = {"nombre": "Juan", "edad": 30, "ciudad": "Madrid"}
resultado = coleccion.insert_one(documento)
print("ID del documento insertado:", resultado.inserted_id)
```


#### Insertar múltiples documentos:

```python
documentos = [
    {"nombre": "Ana", "edad": 25, "ciudad": "Barcelona"},
    {"nombre": "Luis", "edad": 35, "ciudad": "Valencia"}
]
resultado = coleccion.insert_many(documentos)
print("IDs de los documentos insertados:", resultado.inserted_ids)
```

---

### **6. Consultar documentos**

Puedes recuperar documentos usando `find()` o `find_one()`.

#### Recuperar todos los documentos:

```python
for doc in coleccion.find():
    print(doc)
```


#### Recuperar un documento específico:

```python
query = {"nombre": "Juan"}
doc = coleccion.find_one(query)
print("Documento encontrado:", doc)
```

---

### **7. Actualizar documentos**

Actualiza campos específicos en uno o varios documentos.

#### Actualizar un documento:

```python
query = {"nombre": "Juan"}
new_values = {"$set": {"edad": 31}}
coleccion.update_one(query, new_values)
print("Documento actualizado")
```


#### Actualizar múltiples documentos:

```python
query = {"ciudad": "Valencia"}
new_values = {"$set": {"ciudad": "Sevilla"}}
resultado = coleccion.update_many(query, new_values)
print(f"Documentos actualizados: {resultado.modified_count}")
```

---

### **8. Eliminar documentos**

Elimina uno o varios documentos según un criterio.

#### Eliminar un documento:

```python
query = {"nombre": "Juan"}
resultado = coleccion.delete_one(query)
print(f"Documentos eliminados: {resultado.deleted_count}")
```


#### Eliminar múltiples documentos:

```python
query = {"ciudad": "Sevilla"}
resultado = coleccion.delete_many(query)
print(f"Documentos eliminados: {resultado.deleted_count}")
```

---

### **9. Operaciones avanzadas: Agregaciones**

Realiza consultas más complejas con el método `aggregate()`.

```python
pipeline = [
    {"$match": {"edad": {"$gte": 30}}},
    {"$group": {"_id": "$ciudad", "total_personas": {"$sum": 1}}}
]
resultado = list(coleccion.aggregate(pipeline))
print("Resultados de la agregación:", resultado)
```

---

### **10. Cerrar la conexión**

Es buena práctica cerrar la conexión cuando termines.

```python
client.close()
print("Conexión cerrada")
```

---

Esta guía cubre las operaciones básicas y avanzadas con PyMongo para interactuar con MongoDB desde Python. Puedes usarla como referencia para enseñar conceptos fundamentales en tu curso sobre sistemas gestores de bases de datos (SGBD).

<div>⁂</div>

[^1]: https://www.ionos.es/digitalguide/paginas-web/desarrollo-web/mongodb-python/

[^2]: https://aitor-medrano.github.io/iabd2223/sa/07pymongo.html

[^3]: https://www.snellrojas.com/programacion/pymongo-para-utilizar-mongodb-desde-python/

[^4]: https://jarroba.com/python-mongodb-driver-pymongo-con-ejemplos/

[^5]: https://www.youtube.com/watch?v=pJO5gKxzsco

[^6]: https://www.youtube.com/watch?v=4oxvW6gBBi4

[^7]: https://www.mongodb.com/es/resources/languages/python

[^8]: http://codigo-python.blogspot.com/2017/11/pymongo-parte-1.html

