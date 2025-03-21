import sqlite3

def crear_conexion():
    conn = sqlite3.connect('mi_base_de_datos.db')
    return conn

def crear_tabla(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            edad INTEGER
        )
    ''')
    conn.commit()

def insertar_usuario(conn, nombre, edad):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (nombre, edad) VALUES (?, ?)', (nombre, edad))
    conn.commit()
    print("Usuario insertado con éxito.")

def mostrar_usuarios(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    if usuarios:
        print("\nUsuarios en la base de datos:")
        for usuario in usuarios:
            print(f"ID: {usuario[0]}, Nombre: {usuario[1]}, Edad: {usuario[2]}")
    else:
        print("No hay usuarios en la base de datos.")

def actualizar_usuario(conn, id, nombre, edad):
    cursor = conn.cursor()
    cursor.execute('UPDATE usuarios SET nombre = ?, edad = ? WHERE id = ?', (nombre, edad, id))
    conn.commit()
    if cursor.rowcount > 0:
        print("Usuario actualizado con éxito.")
    else:
        print("No se encontró un usuario con ese ID.")

def eliminar_usuario(conn, id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    conn.commit()
    if cursor.rowcount > 0:
        print("Usuario eliminado con éxito.")
    else:
        print("No se encontró un usuario con ese ID.")

def menu():
    conn = crear_conexion()
    crear_tabla(conn)
    
    while True:
        print("\n--- MENÚ CRUD DE USUARIOS ---")
        print("1. Insertar usuario")
        print("2. Mostrar usuarios")
        print("3. Actualizar usuario")
        print("4. Eliminar usuario")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            nombre = input("Ingrese el nombre del usuario: ")
            edad = int(input("Ingrese la edad del usuario: "))
            insertar_usuario(conn, nombre, edad)
        elif opcion == '2':
            mostrar_usuarios(conn)
        elif opcion == '3':
            id = int(input("Ingrese el ID del usuario a actualizar: "))
            nombre = input("Ingrese el nuevo nombre: ")
            edad = int(input("Ingrese la nueva edad: "))
            actualizar_usuario(conn, id, nombre, edad)
        elif opcion == '4':
            id = int(input("Ingrese el ID del usuario a eliminar: "))
            eliminar_usuario(conn, id)
        elif opcion == '5':
            print("Gracias por usar el programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
    
    conn.close()

if __name__ == "__main__":
    menu()

