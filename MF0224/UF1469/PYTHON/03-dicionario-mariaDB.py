import mysql.connector

def conectar_bd(host, usuario, clave):
    return mysql.connector.connect(
        host=host,
        user=usuario,
        password=clave
    )

def obtener_bases_datos(conexion):
    cursor = conexion.cursor()
    cursor.execute("SHOW DATABASES")
    bases_datos = [bd[0] for bd in cursor.fetchall()]
    cursor.close()
    return bases_datos

def obtener_diccionario_bd(conexion, base_datos):
    cursor = conexion.cursor()
    cursor.execute(f"USE {base_datos}")
    cursor.execute("SHOW TABLES")
    tablas = [tabla[0] for tabla in cursor.fetchall()]
    
    diccionario_bd = {}
    for tabla in tablas:
        cursor.execute(f"DESCRIBE {tabla}")
        columnas = [col[0] for col in cursor.fetchall()]
        diccionario_bd[tabla] = columnas
    
    cursor.close()
    return diccionario_bd

def main():
    host = input("Ingrese el host de la BD (ej. localhost): ")
    usuario = input("Ingrese el usuario de la BD: ")
    clave = input("Ingrese la contraseña: ")
    
    conexion = conectar_bd(host, usuario, clave)
    
    if conexion.is_connected():
        print("Conectado a MariaDB")
        bases_datos = obtener_bases_datos(conexion)
        print("Bases de datos disponibles:")
        for i, bd in enumerate(bases_datos, 1):
            print(f"{i}. {bd}")
        
        seleccion = int(input("Seleccione una base de datos (número): "))
        base_datos = bases_datos[seleccion - 1]
        
        diccionario_bd = obtener_diccionario_bd(conexion, base_datos)
        print("\nDiccionario de la base de datos:")
        print(diccionario_bd)
    
        conexion.close()
    else:
        print("Error de conexión")

if __name__ == "__main__":
    main()
