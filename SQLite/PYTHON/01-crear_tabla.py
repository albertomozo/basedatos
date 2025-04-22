import sqlite3

# Conectar a la base de datos (si no existe, la crea)
conn = sqlite3.connect('./SQLite/PYTHON/alb.db')
cursor = conn.cursor()

# Crear una tabla
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        edad INTEGER
    )
''')

# Insertar algunos datos de ejemplo
usuarios = [
    ('Juan', 30),
    ('María', 25),
    ('Pedro', 35)
]
cursor.executemany('INSERT INTO usuarios (nombre, edad) VALUES (?, ?)', usuarios)

# Guardar los cambios
conn.commit()

# Realizar una consulta
cursor.execute('SELECT * FROM usuarios')
resultados = cursor.fetchall()

# Imprimir los resultados
print("Usuarios en la base de datos:")
for row in resultados:
    print(f"ID: {row[0]}, Nombre: {row[1]}, Edad: {row[2]}")

# Cerrar la conexión
conn.close()
