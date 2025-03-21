import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="proyecto",
        user="postgres",
        password="ALBERTO",
        client_encoding="UTF8"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM data_ejemplo")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.close()
except psycopg2.Error as e:
    print("Error al conectar a PostgreSQL:", e)
