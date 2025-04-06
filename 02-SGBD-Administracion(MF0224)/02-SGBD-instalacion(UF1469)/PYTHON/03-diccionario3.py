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
    
    # Obtener información de las tablas
    cursor.execute("""
    SELECT TABLE_NAME, TABLE_TYPE, ENGINE, TABLE_ROWS, AVG_ROW_LENGTH, DATA_LENGTH, INDEX_LENGTH
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = %s
    """, (base_datos,))
    tablas = cursor.fetchall()
    
    for tabla in tablas:
        nombre_tabla = tabla[0]
        diccionario[nombre_tabla] = {
            "Tipo": tabla[1],
            "Motor": tabla[2],
            "Filas aproximadas": tabla[3],
            "Longitud promedio de fila": tabla[4],
            "Tamaño de datos": tabla[5],
            "Tamaño de índices": tabla[6],
            "Columnas": []
        }
        
        # Obtener información de las columnas
        cursor.execute("""
        SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_KEY, COLUMN_DEFAULT, EXTRA
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
        """, (base_datos, nombre_tabla))
        columnas = cursor.fetchall()
        
        for columna in columnas:
            diccionario[nombre_tabla]["Columnas"].append({
                "Nombre": columna[0],
                "Tipo": columna[1],
                "Nulo": columna[2],
                "Clave": columna[3],
                "Predeterminado": columna[4],
                "Extra": columna[5]
            })
        
        # Obtener información de las claves foráneas
        cursor.execute("""
        SELECT CONSTRAINT_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
        FROM information_schema.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND REFERENCED_TABLE_NAME IS NOT NULL
        """, (base_datos, nombre_tabla))
        fks = cursor.fetchall()
        
        if fks:
            diccionario[nombre_tabla]["Claves foráneas"] = []
            for fk in fks:
                diccionario[nombre_tabla]["Claves foráneas"].append({
                    "Nombre": fk[0],
                    "Columna": fk[1],
                    "Tabla referenciada": fk[2],
                    "Columna referenciada": fk[3]
                })
    
    return diccionario

def imprimir_diccionario(diccionario):
    for tabla, info in diccionario.items():
        print(f"\nTabla: {tabla}")
        print("-" * 80)
        for clave, valor in info.items():
            if clave != "Columnas" and clave != "Claves foráneas":
                print(f"{clave}: {valor}")
        
        print("\nColumnas:")
        for columna in info["Columnas"]:
            print("-" * 40)
            for clave, valor in columna.items():
                print(f"  {clave}: {valor}")
        
        if "Claves foráneas" in info:
            print("\nClaves foráneas:")
            for fk in info["Claves foráneas"]:
                print("-" * 40)
                for clave, valor in fk.items():
                    print(f"  {clave}: {valor}")

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
