import json
from pymongo import MongoClient

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["naturaleza"]  # Nombre de la base de datos

# Colecciones en MongoDB
espacios_collection = db["espaciosNaturales"]
albumes_collection = db["albumes"]
animales_collection = db["animales"]

# Función para cargar y transformar datos
def transformar_y_cargar(espacios_file, albumes_file, animales_file):
    # Leer archivos JSON
    with open(espacios_file, "r", encoding="utf-8") as f:
        espacios = json.load(f)
    with open(albumes_file, "r", encoding="utf-8") as f:
        albumes = json.load(f)
    with open(animales_file, "r", encoding="utf-8") as f:
        animales = json.load(f)
    
    # Crear un diccionario de animales por su ID para acceso rápido
    animales_dict = {animal["id"]: animal for animal in animales}
    
    # Transformar los datos de espacios para incluir álbumes y animales
    for espacio in espacios:
        espacio_id = espacio["id"]
        
        # Asociar álbumes al espacio
        espacio["albumes"] = []
        for album in albumes:
            if album["espacioId"] == espacio_id:
                # Asociar animales a las imágenes del álbum
                for imagen in album["imagenes"]:
                    if "animalId" in imagen and imagen["animalId"] in animales_dict:
                        imagen["animal"] = animales_dict[imagen["animalId"]]
                
                espacio["albumes"].append(album)
    
    # Insertar datos transformados en MongoDB
    espacios_collection.insert_many(espacios)
    print(f"Espacios naturales insertados: {len(espacios)}")
    
    # Insertar álbumes y animales sin transformar (si los necesitas en colecciones separadas)
    albumes_collection.insert_many(albumes)
    print(f"Álbumes insertados: {len(albumes)}")
    
    animales_collection.insert_many(animales)
    print(f"Animales insertados: {len(animales)}")

# Llamar a la función con tus archivos JSON
if __name__ == "__main__":
    transformar_y_cargar("espaciosnaturales.json", "album.json", "animales.json")

