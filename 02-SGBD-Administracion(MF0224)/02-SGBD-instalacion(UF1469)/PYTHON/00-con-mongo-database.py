from pymongo import MongoClient

try:
    # Conectar al servidor de MongoDB
    client = MongoClient("mongodb://localhost:27017/")  # Cambia la URI si usas un servidor remoto o MongoDB Atlas
    print("Conexión exitosa a MongoDB")

    # Listar las bases de datos disponibles
    bases_de_datos = client.list_database_names()
    print("Bases de datos disponibles:")
    for bd in bases_de_datos:
        print(f"- {bd}")

except Exception as e:
    print("Error al conectar a MongoDB:", e)

finally:
    # Cerrar la conexión
    client.close()
