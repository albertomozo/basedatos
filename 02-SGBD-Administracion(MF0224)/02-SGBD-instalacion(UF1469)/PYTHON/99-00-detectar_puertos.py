import socket
import os
import sqlite3

def check_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex((host, port)) == 0

def detect_sqlite():
    dbs = []
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith(".sqlite") or file.endswith(".db"):
                dbs.append(os.path.join(root, file))
    return ('SQLite', dbs) if dbs else None

def detect_databases():
    services = {
        "MySQL": 3306,
        "MariaDB": 3306,
        "PostgreSQL": 5432,
        "SQL Server": 1433,
    }
    
    detected = []
    for name, port in services.items():
        if check_port("localhost", port):
            detected.append(name)
    
    sqlite_dbs = detect_sqlite()
    if sqlite_dbs:
        detected.append(sqlite_dbs)
    
    return detected

def main():
    detected = detect_databases()
    if detected:
        print("Servicios detectados:")
        for db in detected:
            if isinstance(db, tuple):
                print(f"{db[0]} detectado. Bases de datos encontradas:")
                for db_file in db[1]:
                    print(f"  - {db_file}")
            else:
                print(f"- {db}")
    else:
        print("No se detectaron bases de datos.")

if __name__ == "__main__":
    main()