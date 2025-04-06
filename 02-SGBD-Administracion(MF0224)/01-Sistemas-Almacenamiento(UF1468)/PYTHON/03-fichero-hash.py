import hashlib

usuarios = {
    "usuario1": "contraseña1",
    "usuario2": "contraseña2",
}

with open("usuarios.hash", "wb") as f:
    for usuario, contraseña in usuarios.items():
        posicion = hash(usuario) % 100  # Función hash simple (ejemplo)
        f.seek(posicion * 52)  # Posición en el fichero (52 bytes por registro)
        nombre = usuario.encode("utf-8").ljust(20, b" ")
        contraseña = hashlib.sha256(contraseña.encode("utf-8")).digest()  # Hash de la contraseña
        f.write(nombre + contraseña)