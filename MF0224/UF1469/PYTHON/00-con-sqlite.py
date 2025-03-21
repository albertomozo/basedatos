import sqlite3

try:
    # Conectar (si no existe, se crea el archivo SQLite)
    conn = sqlite3.connect("db01.sqlite")

    cursor = conn.cursor()
    cursor.execute("SELECT sqlite_version();")
    version = cursor.fetchone()
    print(f"Versión de SQLite: {version[0]}")

    cursor.close()
    conn.close()
except sqlite3.Error as e:
    print(f"Error al conectar a SQLite: {e}")