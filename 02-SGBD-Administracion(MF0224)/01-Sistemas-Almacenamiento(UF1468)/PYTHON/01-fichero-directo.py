import struct

productos = [
    {"nombre": "Producto A", "precio": 10.99, "stock": 100},
    {"nombre": "Producto B", "precio": 20.50, "stock": 50},
]

with open("productos.bin", "wb") as f:
    for producto in productos:
        nombre = producto["nombre"].encode("utf-8").ljust(20, b" ")  # Nombre con 20 bytes
        precio = struct.pack("f", producto["precio"])  # Precio como float (4 bytes)
        stock = struct.pack("i", producto["stock"])  # Stock como entero (4 bytes)
        f.write(nombre + precio + stock)