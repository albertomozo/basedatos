import socket
import concurrent.futures
import platform
import subprocess
import re
import os
import sys
from datetime import datetime
import time

# Configuración de timeout global
GLOBAL_TIMEOUT = 3  # segundos

def check_port(ip, port, timeout=1):
    """Comprueba si un puerto específico está abierto en una dirección IP"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

def get_all_listening_ports():
    """Obtiene todos los puertos que están escuchando en el sistema"""
    ports = []
    
    try:
        if platform.system() == "Windows":
            # Ejecutar netstat para Windows
            result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, timeout=5)
            for line in result.stdout.split('\n'):
                if 'LISTENING' in line:
                    match = re.search(r':(\d+)', line)
                    if match:
                        port = int(match.group(1))
                        if port not in ports:
                            ports.append(port)
        else:
            # Para Linux/Mac
            result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True, timeout=5)
            for line in result.stdout.split('\n'):
                if 'LISTEN' in line:
                    match = re.search(r':(\d+)', line)
                    if match:
                        port = int(match.group(1))
                        if port not in ports:
                            ports.append(port)
    except Exception as e:
        print(f"Error al obtener puertos: {str(e)}")
        # Puertos comunes como respaldo
        ports = [80, 443, 3306, 5432, 1433, 1434, 3389, 22, 21, 25, 8080, 8443]
    
    return ports

def identify_mysql(ip, port):
    """Intenta identificar si el puerto tiene MySQL/MariaDB con timeout estricto"""
    try:
        import pymysql
        try:
            conn = pymysql.connect(host=ip, port=port, user='', password='', connect_timeout=GLOBAL_TIMEOUT)
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
            s.settimeout(GLOBAL_TIMEOUT)
            s.connect((ip, port))
            data = s.recv(1024)
            s.close()
            if b"mysql" in data.lower() or b"mariadb" in data.lower():
                return "MySQL/MariaDB"
            return None
        except:
            return None

def identify_postgres(ip, port):
    """Intenta identificar si el puerto tiene PostgreSQL con timeout estricto"""
    try:
        import psycopg2
        try:
            conn = psycopg2.connect(host=ip, port=port, user='postgres', password='', connect_timeout=GLOBAL_TIMEOUT)
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
        return None  # Simplificado para evitar bloqueos

def identify_sqlserver(ip, port):
    """Intenta identificar si el puerto tiene SQL Server con timeout estricto"""
    try:
        import pyodbc
        try:
            conn_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={ip},{port};UID=sa;PWD=;CONNECTION TIMEOUT={GLOBAL_TIMEOUT}'
            conn = pyodbc.connect(conn_string)
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
        return None  # Simplificado para evitar bloqueos

def check_port_for_db(ip, port):
    """Comprueba si un puerto específico tiene un SGBD y devuelve el tipo con timeout estricto"""
    # Primero verificamos si el puerto está abierto para no perder tiempo
    if not check_port(ip, port, timeout=1):
        return None
        
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

def check_sqlite_files(directory=".", max_depth=2, current_depth=0):
    """Busca archivos SQLite en el directorio especificado con límite de profundidad"""
    if current_depth > max_depth:
        return []
        
    sqlite_files = []
    
    try:
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            if os.path.isfile(full_path) and item.endswith(('.db', '.sqlite', '.sqlite3')):
                sqlite_files.append(full_path)
            elif os.path.isdir(full_path):
                # Recursión limitada
                child_files = check_sqlite_files(full_path, max_depth, current_depth + 1)
                sqlite_files.extend(child_files)
    except PermissionError:
        pass  # Ignorar directorios sin permiso
    except Exception:
        pass  # Ignorar otros errores
    
    return sqlite_files

def check_access_files(directory=".", max_depth=2, current_depth=0):
    """Busca archivos de Microsoft Access en el directorio especificado con límite de profundidad"""
    if current_depth > max_depth:
        return []
        
    access_files = []
    
    try:
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            if os.path.isfile(full_path) and item.endswith(('.mdb', '.accdb')):
                access_files.append(full_path)
            elif os.path.isdir(full_path):
                # Recursión limitada
                child_files = check_access_files(full_path, max_depth, current_depth + 1)
                access_files.extend(child_files)
    except PermissionError:
        pass  # Ignorar directorios sin permiso
    except Exception:
        pass  # Ignorar otros errores
    
    return access_files

def main():
    print("\n=== DETECTOR DE SISTEMAS GESTORES DE BASES DE DATOS ===")
    print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Sistema operativo: {platform.system()} {platform.release()}")
    
    print("\nObteniendo puertos abiertos en localhost (127.0.0.1)...")
    start_time = time.time()
    
    # Obtener puertos que están escuchando
    system_ports = get_all_listening_ports()
    if not system_ports:
        print("No se detectaron puertos. Verificando puertos comunes...")
        # Puertos comunes de SGBD si netstat falla
        system_ports = [1433, 1434, 3306, 3307, 5432, 8080, 27017, 6379, 2638]
    
    print(f"\nPuertos a analizar: {', '.join(map(str, sorted(system_ports)))}")
    print(f"Total de puertos a analizar: {len(system_ports)}")
    
    # Verificar cada puerto abierto para buscar SGBD
    print("\n=== ANÁLISIS DE PUERTOS PARA DETECTAR SGBD ===")
    found_db = False
    results = []
    
    # Usamos un timeout más corto y menos workers para evitar saturación
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Iniciamos todos los trabajos
        future_to_port = {executor.submit(check_port_for_db, '127.0.0.1', port): port for port in system_ports}
        
        # Recogemos resultados con timeout adicional
        for future in concurrent.futures.as_completed(future_to_port, timeout=60):
            port = future_to_port[future]
            try:
                db_type = future.result(timeout=GLOBAL_TIMEOUT)  # Timeout adicional por si acaso
                if db_type:
                    found_db = True
                    result = f"[+] Puerto {port}: {db_type}"
                    print(result)
                    results.append((port, db_type))
                else:
                    print(f"[-] Puerto {port}: No se detectó SGBD")
            except concurrent.futures.TimeoutError:
                print(f"[!] Puerto {port}: Timeout durante análisis")
            except Exception as exc:
                print(f"[!] Error al analizar puerto {port}: {str(exc)}")
    
    if not found_db:
        print("No se detectaron SGBD en ninguno de los puertos analizados.")
    else:
        print("\n=== RESUMEN DE SGBD DETECTADOS ===")
        for port, db_type in results:
            print(f"[+] Puerto {port}: {db_type}")
    
    # Búsqueda limitada de archivos para evitar bloqueos
    print("\n=== ARCHIVOS SQLITE DETECTADOS ===")
    sqlite_files = check_sqlite_files()
    if sqlite_files:
        for file in sqlite_files[:10]:  # Mostrar máximo 10 resultados
            print(f"[+] SQLite: {file}")
        if len(sqlite_files) > 10:
            print(f"... y {len(sqlite_files) - 10} archivos más")
    else:
        print("No se encontraron archivos SQLite en el directorio actual.")
    
    print("\n=== ARCHIVOS MICROSOFT ACCESS DETECTADOS ===")
    access_files = check_access_files()
    if access_files:
        for file in access_files[:10]:  # Mostrar máximo 10 resultados
            print(f"[+] Microsoft Access: {file}")
        if len(access_files) > 10:
            print(f"... y {len(access_files) - 10} archivos más")
    else:
        print("No se encontraron archivos de Microsoft Access en el directorio actual.")
    
    elapsed_time = time.time() - start_time
    print(f"\n=== ESCANEO COMPLETADO EN {elapsed_time:.2f} SEGUNDOS ===")

if __name__ == "__main__":
    main()