import os
import subprocess
import sqlite3
import pymysql  # Instalar con: pip install pymysql
import psycopg2  # Instalar con: pip install psycopg2
import pyodbc  # Instalar con: pip install pyodbc

def detect_mysql():
    try:
        connection = pymysql.connect(host='localhost', user='root', password='')
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES;")
        dbs = [db[0] for db in cursor.fetchall()]
        connection.close()
        return ('MySQL', dbs)
    except:
        return None

def detect_mariadb():
    try:
        connection = pymysql.connect(host='localhost', user='root', password='', port=3306)
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES;")
        dbs = [db[0] for db in cursor.fetchall()]
        connection.close()
        return ('MariaDB', dbs)
    except:
        return None

def detect_postgresql():
    try:
        connection = psycopg2.connect(host='localhost', user='postgres', password='', dbname='postgres')
        cursor = connection.cursor()
        cursor.execute("SELECT datname FROM pg_database;")
        dbs = [db[0] for db in cursor.fetchall()]
        connection.close()
        return ('PostgreSQL', dbs)
    except:
        return None

def detect_sqlite():
    dbs = []
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith(".sqlite") or file.endswith(".db"):
                dbs.append(os.path.join(root, file))
    return ('SQLite', dbs) if dbs else None

def detect_sqlserver():
    try:
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sys.databases;")
        dbs = [row[0] for row in cursor.fetchall()]
        conn.close()
        return ('SQL Server', dbs)
    except:
        return None

def main():
    detected_dbs = []
    for detector in [detect_mysql, detect_mariadb, detect_postgresql, detect_sqlite, detect_sqlserver]:
        result = detector()
        if result:
            detected_dbs.append(result)
    
    if detected_dbs:
        for dbms, dbs in detected_dbs:
            print(f"{dbms} detectado. Bases de datos encontradas:")
            for db in dbs:
                print(f"  - {db}")
    else:
        print("No se detectaron bases de datos.")

if __name__ == "__main__":
    main()
