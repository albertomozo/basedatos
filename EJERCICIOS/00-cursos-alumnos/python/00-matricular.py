import mysql.connector
from mysql.connector import Error

def conectar_db():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='alberto',
            password='alberto',
            database='formacion'
        )
    except Error as e:
        print(f"Error de conexión: {e}")
        return None

def mostrar_alumnos():
    conn = conectar_db()
    if not conn:
        return
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT ID_Alumno, Nombre, Apellidos FROM Alumno")
        print("\nListado de Alumnos:")
        for alumno in cursor:
            print(f"{alumno['ID_Alumno']}: {alumno['Nombre']} {alumno['Apellidos']}")
    except Error as e:
        print(f"Error al obtener alumnos: {e}")
    finally:
        conn.close()

def mostrar_cursos():
    conn = conectar_db()
    if not conn:
        return
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT ID_Curso, Nombre_Curso FROM Curso")
        print("\nListado de Cursos Disponibles:")
        for curso in cursor:
            print(f"{curso['ID_Curso']}: {curso['Nombre_Curso']}")
    except Error as e:
        print(f"Error al obtener cursos: {e}")
    finally:
        conn.close()

def matricular_alumno():
    conn = conectar_db()
    if not conn:
        return
    
    try:
        id_alumno = int(input("\nIngrese ID del alumno: "))
        id_curso = int(input("Ingrese ID del curso: "))
        
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Matricula (ID_Alumno, ID_Curso) 
            VALUES (%s, %s)
        """, (id_alumno, id_curso))
        
        conn.commit()
        print("\nMatrícula realizada con éxito!")
        
    except Error as e:
        print(f"Error en la matrícula: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    while True:
        print("\nSistema de Matriculación")
        print("1. Ver alumnos")
        print("2. Ver cursos")
        print("3. Matricular alumno")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            mostrar_alumnos()
        elif opcion == "2":
            mostrar_cursos()
        elif opcion == "3":
            mostrar_alumnos()
            mostrar_cursos()
            matricular_alumno()
        elif opcion == "4":
            break
        else:
            print("Opción no válida")
