import socket
import os
import sqlite3
import pymysql
import psycopg2
import pyodbc

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

def check_mysql_mariadb(port):
    try:
        connection = pymysql.connect(host='localhost', port=port, user='root', password='')
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES;")
        dbs = [db[0] for db in cursor.fetchall()]
        connection.close()
        return dbs
    except:
        return None

def check_postgresql():
    try:
        connection = psycopg2.connect(host='localhost', port=5432, user='postgres', password='', dbname='postgres')
        cursor = connection.cursor()
        cursor.execute("SELECT datname FROM pg_database;")
        dbs = [db[0] for db in cursor.fetchall()]
        connection.close()
        return dbs
    except:
        return None

def check_sqlserver():
    try:
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sys.databases;")
        dbs = [row[0] for row in cursor.fetchall()]
        conn.close()
        return dbs
    except:
        return None

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
            dbs = None
            if name in ["MySQL", "MariaDB"]:
                dbs = check_mysql_mariadb(port)
            elif name == "PostgreSQL":
                dbs = check_postgresql()
            elif name == "SQL Server":
                dbs = check_sqlserver()
            detected.append((name, port, dbs))
    
    sqlite_dbs = detect_sqlite()
    if sqlite_dbs:
        detected.append((sqlite_dbs[0], "N/A", sqlite_dbs[1]))
    
    return detected

def main():
    detected = detect_databases()
    if detected:
        print("Servicios detectados:")
        for db in detected:
            name, port, dbs = db
            print(f"- {name} detectado en el puerto {port}.")
            if dbs:
                print("  Bases de datos encontradas:")
                for db_name in dbs:
                    print(f"    - {db_name}")
    else:
        print("No se detectaron bases de datos.")

if __name__ == "__main__":
    main()