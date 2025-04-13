# Importar la biblioteca necesaria
from pymongo import MongoClient

# Establecer una conexión con el servidor de MongoDB
# Cambia la URI según sea necesario (por ejemplo, para MongoDB Atlas o un servidor remoto)
client = MongoClient("mongodb://localhost:27017/")

# Acceder a una base de datos específica
db = client["ejer01"]

# Acceder a una colección dentro de la base de datos
coleccion = db["prueba"]

# Insertar un documento en la colección
documento = {"nombre": "Juan", "edad": 30, "ciudad": "Madrid"}
coleccion.insert_one(documento)
print("Documento insertado exitosamente.")

# Recuperar todos los documentos de la colección
documentos = coleccion.find()
print("Documentos en la colección:")
for doc in documentos:
    print(doc)

# Actualizar un documento en la colección
coleccion.update_one({"nombre": "Juan"}, {"$set": {"edad": 35}})
print("Documento actualizado exitosamente.")

# Eliminar un documento de la colección
#coleccion.delete_one({"nombre": "Juan"})
#print("Documento eliminado exitosamente.")

# Cerrar la conexión con MongoDB
client.close()
