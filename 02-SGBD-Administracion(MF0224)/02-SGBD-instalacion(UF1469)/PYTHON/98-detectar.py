import socket
import concurrent.futures
import platform
import subprocess
import re
import os
import sys
from datetime import datetime

# Configuración para manejar la codificación de caracteres
if platform.system() == "Windows":
    # Intentar establecer la codificación de la consola a UTF-8 en Windows
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleOutputCP(65001)  # Establecer codificación UTF-8
    except:
        pass

def check_port(ip, port, timeout=1):
    """Comprueba si un puerto específico está abierto en una dirección IP"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

def get_all_listening_ports():
    """Obtiene todos los puertos que están escuchando en el sistema"""
    ports = []
    
    if platform.system() == "Windows":
        # Ejecutar netstat para Windows
        result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'LISTENING' in line:
                match = re.search(r':(\d+)', line)
                if match:
                    port = int(match.group(1))
                    if port not in ports:
                        ports.append(port)
    else:
        # Para Linux/Mac
        result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'LISTEN' in line:
                match = re.search(r':(\d+)', line)
                if match:
                    port = int(match.group(1))
                    if port not in ports:
                        ports.append(port)
    
    return ports

def identify_mysql(ip, port):
    """Intenta identificar si el puerto tiene MySQL/MariaDB"""
    try:
        import pymysql
        try:
            conn = pymysql.connect(host=ip, port=port, user='', password='', connect_timeout=2)
            server_info = conn.get_server_info()
            conn.close()
            if "MariaDB" in server_info:
                return f"MariaDB ({server_info})"
            else:
                return f"MySQL ({server_info})"
        except pymysql.err.OperationalError as e:
            # Si hay error de autenticación, es probable que sea MySQL/MariaDB
            if "Access denied" in str(e):
                return "MySQL/MariaDB (autenticación requerida)"
            return None
        except Exception:
            return None
    except ImportError:
        # Si no está instalado pymysql, intentamos con conexión socket básica
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((ip, port))
            data = s.recv(1024)
            s.close()
            if b"mysql" in data.lower() or b"mariadb" in data.lower():
                return "MySQL/MariaDB"
            return None
        except:
            return None

def identify_postgres(ip, port):
    """Intenta identificar si el puerto tiene PostgreSQL"""
    try:
        import psycopg2
        try:
            conn = psycopg2.connect(host=ip, port=port, user='postgres', password='', connect_timeout=2)
            version = conn.server_version
            conn.close()
            return f"PostgreSQL (v{version})"
        except psycopg2.OperationalError as e:
            # Si hay error de autenticación, es probable que sea PostgreSQL
            if "password authentication" in str(e) or "authentication failed" in str(e):
                return "PostgreSQL (autenticación requerida)"
            return None
        except Exception:
            return None
    except ImportError:
        # Si no está instalado psycopg2, intentamos con conexión socket básica
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((ip, port))
            # Enviar un mensaje de inicio de PostgreSQL
            s.send(b'\x00\x00\x00\x08\x04\xd2\x16\x2f')
            data = s.recv(1024)
            s.close()
            if data and len(data) > 0:
                return "Posiblemente PostgreSQL"
            return None
        except:
            return None

def identify_sqlserver(ip, port):
    """Intenta identificar si el puerto tiene SQL Server"""
    try:
        import pyodbc
        try:
            conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={ip},{port};UID=sa;PWD=;CONNECTION TIMEOUT=2')
            cursor = conn.cursor()
            cursor.execute("SELECT @@version")
            version = cursor.fetchone()[0]
            conn.close()
            return f"Microsoft SQL Server ({version})"
        except pyodbc.Error as e:
            # Si hay error de autenticación, es probable que sea SQL Server
            error_msg = str(e)
            if "Login failed" in error_msg or "password" in error_msg.lower():
                return "Microsoft SQL Server (autenticación requerida)"
            return None
        except Exception:
            return None
    except ImportError:
        # Si no está instalado pyodbc, intentamos con conexión socket básica
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((ip, port))
            # SQL Server normalmente responde a TDS (Tabular Data Stream)
            s.send(b'\x12\x01\x00\x34\x00\x00\x00\x00\x00\x00\x15\x00\x06\x01\x00\x1b\x00\x01\x02\x00\x1c\x00\x0c\x03\x00\x28\x00\x04\x04\x00\x38\x00\x01\x05\x00\x39\x00\x01\x06\x00\x3a\x00\x01\x07\x00\x3b\x00\x01\x00\x00\x00')
            data = s.recv(1024)
            s.close()
            if data and len(data) > 0:
                return "Posiblemente Microsoft SQL Server"
            return None
        except:
            return None

def check_port_for_db(ip, port):
    """Comprueba si un puerto específico tiene un SGBD y devuelve el tipo"""
    # Comprobar MySQL/MariaDB
    result = identify_mysql(ip, port)
    if result:
        return result
    
    # Comprobar PostgreSQL
    result = identify_postgres(ip, port)
    if result:
        return result
    
    # Comprobar SQL Server
    result = identify_sqlserver(ip, port)
    if result:
        return result
    
    return None

def check_sqlite_files(directory="."):
    """Busca archivos SQLite en el directorio especificado"""
    sqlite_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.db', '.sqlite', '.sqlite3')):
                sqlite_files.append(os.path.join(root, file))
    
    return sqlite_files

def check_access_files(directory="."):
    """Busca archivos de Microsoft Access en el directorio especificado"""
    access_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.mdb', '.accdb')):
                access_files.append(os.path.join(root, file))
    
    return access_files

def main():
    print("\n=== DETECTOR DE SISTEMAS GESTORES DE BASES DE DATOS ===")
    print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Sistema operativo: {platform.system()} {platform.release()}")
    print("\nObteniendo puertos abiertos en localhost (127.0.0.1)...")
    
    # Obtener puertos que están escuchando en el sistema
    system_ports = get_all_listening_ports()
    print(f"\nPuertos escuchando en el sistema: {', '.join(map(str, sorted(system_ports)))}")
    
    # Verificar cada puerto abierto para buscar SGBD
    print("\n=== ANÁLISIS DE PUERTOS PARA DETECTAR SGBD ===")
    found_db = False
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_port = {executor.submit(check_port_for_db, '127.0.0.1', port): port for port in system_ports}
        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            try:
                db_type = future.result()
                if db_type:
                    found_db = True
                    print(f"[+] Puerto {port}: {db_type}")
            except Exception as exc:
                print(f"[!] Error al analizar puerto {port}: {str(exc)}")
    
    if not found_db:
        print("No se detectaron SGBD en ninguno de los puertos abiertos.")
    
    # Buscar archivos SQLite
    print("\n=== ARCHIVOS SQLITE DETECTADOS ===")
    sqlite_files = check_sqlite_files()
    if sqlite_files:
        for file in sqlite_files:
            print(f"[+] SQLite: {file}")
    else:
        print("No se encontraron archivos SQLite en el directorio actual.")
    
    # Buscar archivos de Access
    print("\n=== ARCHIVOS MICROSOFT ACCESS DETECTADOS ===")
    access_files = check_access_files()
    if access_files:
        for file in access_files:
            print(f"[+] Microsoft Access: {file}")
    else:
        print("No se encontraron archivos de Microsoft Access en el directorio actual.")
    
    print("\n=== ESCANEO COMPLETADO ===")

if __name__ == "__main__":
    main()