import shelve

with shelve.open("usuarios_db") as db:
    for key in db:
        print(f"ID: {key}, Datos: {db[key]}")
