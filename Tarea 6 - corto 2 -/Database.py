import psycopg2

# Conectar a la base de datos
conn = psycopg2.connect(
    dbname="Tarea6",
    user="postgres",
    password="cindy123451",
    host="localhost",
    port="5432"
)

# Crear un cursor
cur = conn.cursor()

# Función para insertar datos
def insertar_datos(nombre, Nit, Placa, Entrada, Salida, Pago):
    query ='INSERT INTO parqueo("Nombre", "Nit", "Placa", "Entrada", "Salida", "Pago") VALUES (%s, %s, %s, %s, %s, %s)'
    cur.execute(query, (nombre, Nit, Placa, Entrada, Salida, Pago))
    conn.commit()
    print("Datos insertados correctamente")

# Función para leer datos
def leer_datos():
    query = 'SELECT * FROM parqueo'
    cur.execute(query)
    resultados = cur.fetchall()
    for fila in resultados:
        print(f"Nombre: {fila[0]}, Nit: {fila[1]}, Placa: {fila[2]}, Entrada: {fila[3]}, Salida: {fila[4]}, Pago: {fila[5]}")

# Ejemplo de uso
insertar_datos('Maria', 53151, 'P-123ABC', 8.00, 11.00, 45.00)
leer_datos()

# Cerrar cursor y conexión
cur.close()
conn.close()

