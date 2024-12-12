import psycopg2

try:
    conn = psycopg2.connect(
        dbname="Tarea6",
        user="postgres",
        password="cindy123451",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    conn.commit()
    print("Conexión exitosa a la base de datos")
    cur.close()
    conn.close()
except Exception as e:
    print("Error al conectar a la base de datos:", e)