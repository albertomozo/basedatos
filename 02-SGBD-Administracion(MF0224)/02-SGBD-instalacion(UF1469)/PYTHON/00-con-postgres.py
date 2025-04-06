import psycopg2

try:
    dsn = "dbname=proyecto user=postgres password=ALBERTO host=localhost port=5432"
    conn = psycopg2.connect(dsn)
    
    print("Conexión exitosa")
except psycopg2.Error as e:
    print(f"Error al conectar a PostgreSQL: {e}")