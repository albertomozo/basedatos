import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",  # Cambia si es remoto
        user="root",
        password="lanbide",
        #database="nombre_base_datos",
        port=3366  # Puerto por defecto de MariaDB/MySQL
    )

    cursor = conn.cursor()
    cursor.execute("SELECT VERSION();")
    version = cursor.fetchone()
    print(f"Versión de MariaDB: {version[0]}")

    cursor.close()
    conn.close()
except mysql.connector.Error as e:
    print(f"Error al conectar a MariaDB: {e}")
