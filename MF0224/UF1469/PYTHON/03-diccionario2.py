import mariadb
import sys

def conectar_mariadb():
    try:
        conn = mariadb.connect(
            user="alberto",
            password="alberto",
            host="localhost",
            port=3366
        )
        return conn
    except mariadb.Error as e:
        print(f"Error al conectar a MariaDB: {e}")
        sys.exit(1)

def listar_bases_datos(cursor):
    cursor.execute("SHOW DATABASES")
    return [db[0] for db in cursor]

def generar_diccionario_datos(cursor, base_datos):
    diccionario = {}
    cursor.execute(f"USE {base_datos}")
    cursor.execute("SHOW TABLES")
    tablas = [tabla[0] for tabla in cursor]

    for tabla in tablas:
        cursor.execute(f"SHOW COLUMNS FROM {tabla}")
        columnas = cursor.fetchall()
        diccionario[tabla] = [
            {
                "Campo": col[0],
                "Tipo": col[1],
                "Nulo": col[2],
                "Clave": col[3],
                "Predeterminado": col[4],
                "Extra": col[5]
            } for col in columnas
        ]
    
    return diccionario

def imprimir_diccionario(diccionario):
    for tabla, columnas in diccionario.items():
        print(f"\nTabla: {tabla}")
        print("-" * 80)
        for columna in columnas:
            for clave, valor in columna.items():
                print(f"{clave}: {valor}")
            print("-" * 40)

def main():
    conn = conectar_mariadb()
    cursor = conn.cursor()

    bases_datos = listar_bases_datos(cursor)
    print("Bases de datos disponibles:")
    for i, db in enumerate(bases_datos, 1):
        print(f"{i}. {db}")

    seleccion = int(input("\nSeleccione el número de la base de datos: ")) - 1
    base_datos_seleccionada = bases_datos[seleccion]

    diccionario = generar_diccionario_datos(cursor, base_datos_seleccionada)
    imprimir_diccionario(diccionario)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
