import shelve

FILENAME = "usuarios.txt"

# 🔹 Funciones para acceso secuencial
def guardar_usuario(id, nombre, email):
    with open(FILENAME, "a") as f:
        f.write(f"{id},{nombre},{email}\n")

def listar_usuarios():
    with open(FILENAME, "r") as f:
        for linea in f:
            print(linea.strip())

def buscar_usuario_secuencial(id):
    with open(FILENAME, "r") as f:
        for linea in f:
            datos = linea.strip().split(",")
            if datos[0] == id:
                return f"Usuario encontrado: {linea.strip()}"
    return "Usuario no encontrado"

# 🔹 Funciones para acceso indexado
def cargar_indices():
    indices = {}
    with open(FILENAME, "r") as f:
        for pos, linea in enumerate(f):
            id, _, _ = linea.strip().split(",")
            indices[id] = pos
    return indices

def buscar_usuario_indexado(id):
    indices = cargar_indices()
    if id in indices:
        with open(FILENAME, "r") as f:
            for i, linea in enumerate(f):
                if i == indices[id]:
                    return f"Usuario encontrado: {linea.strip()}"
    return "Usuario no encontrado"

# 🔹 Funciones para acceso hash
def guardar_usuario_hash(id, nombre, email):
    with shelve.open("usuarios_db") as db:
        db[id] = (nombre, email)

def buscar_usuario_hash(id):
    with shelve.open("usuarios_db") as db:
        if id in db:
            return f"Usuario encontrado: ID {id} -> {db[id]}"
    return "Usuario no encontrado"

# 🔹 Menú de opciones
def menu():
    while True:
        print("\nGestión de Usuarios")
        print("1. Agregar usuario")
        print("2. Listar usuarios")
        print("3. Buscar usuario (Secuencial)")
        print("4. Buscar usuario (Indexado)")
        print("5. Buscar usuario (Hash)")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            id = input("ID: ")
            nombre = input("Nombre: ")
            email = input("Email: ")
            guardar_usuario(id, nombre, email)
            guardar_usuario_hash(id, nombre, email)
            print("Usuario guardado.")

        elif opcion == "2":
            print("\nLista de usuarios:")
            listar_usuarios()

        elif opcion == "3":
            id = input("Ingrese ID a buscar: ")
            print(buscar_usuario_secuencial(id))

        elif opcion == "4":
            id = input("Ingrese ID a buscar: ")
            print(buscar_usuario_indexado(id))

        elif opcion == "5":
            id = input("Ingrese ID a buscar: ")
            print(buscar_usuario_hash(id))

        elif opcion == "6":
            print("Saliendo...")
            break

        else:
            print("Opción no válida, intente de nuevo.")

# Ejecutar el menú
menu()
