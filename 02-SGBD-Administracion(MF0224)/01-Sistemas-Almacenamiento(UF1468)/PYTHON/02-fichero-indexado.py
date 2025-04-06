import struct

libros = [
    {"isbn": "978-0123456789", "titulo": "Libro A", "autor": "Autor X"},
    {"isbn": "978-9876543210", "titulo": "Libro B", "autor": "Autor Y"},
]

with open("libros.dat", "wb") as f_dat, open("libros.idx", "wb") as f_idx:
    for libro in libros:
        posicion = f_dat.tell()  # Posición actual en el fichero de datos
        isbn = libro["isbn"].encode("utf-8").ljust(13, b" ")
        titulo = libro["titulo"].encode("utf-8").ljust(50, b" ")
        autor = libro["autor"].encode("utf-8").ljust(30, b" ")
        f_dat.write(isbn + titulo + autor)
        f_idx.write(isbn + struct.pack("Q", posicion))  # Q para entero de 8 bytes