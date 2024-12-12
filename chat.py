import os
import math
import psycopg2

def menu():
    opcion = 0
    while opcion != 5:
        print("\n¡Bienvenido al Menú Principal!")
        print("Seleccione una opción:")
        print("1. Ingresar datos de facturación")
        print("2. Generación de factura")
        print("3. Historial de datos")
        print("4. Borrar datos")
        print("5. Salir")

        try:
            opcion = int(input("Ingrese su opción: "))

            if opcion < 1 or opcion > 5:
                print("Entrada inválida. Por favor, ingrese un número entre 1 y 5.\n")
                continue

            if opcion == 1:
                datos = ingresoDatos()
                generar_factura(datos)

            elif opcion == 2:
                generar_factura(datos)

            elif opcion == 3:
                historial_datos()

            elif opcion == 4:
                borrar_datos()

            elif opcion == 5:
                print("\u00a1Gracias por visitarnos. Vuelva pronto!\n")

        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.\n")

def ingresoDatos():
    nombre = input("Ingrese el nombre del usuario: ").strip()
    if not nombre or nombre.isdigit():
        raise ValueError("El nombre no puede ser un número o estar vacío.")

    nit_usuario = input("Ingrese el NIT (sin guiones ni espacios): ").strip()
    if not nit_usuario.isdigit():
        raise ValueError("El NIT debe ser un número positivo.")

    No_placa = input("Ingrese la placa del carro: ").strip()
    if not No_placa:
        raise ValueError("Error en el ingreso de la placa. Por favor, intente de nuevo.")

    hora_entrada = float(input("Ingrese la hora de entrada al estacionamiento como Hora.Minutos: "))
    hora_salida = float(input("Ingrese la hora de salida del estacionamiento Hora.Minutos: "))

    return nombre, nit_usuario, No_placa, hora_entrada, hora_salida

def total_pago(hora_entrada, hora_salida):
    tiempo_estancia = hora_salida - hora_entrada
    horas_totales = math.ceil(tiempo_estancia)
    
    if horas_totales == 1:
        return 15.00
    else:
        return 15.00 + (horas_totales - 1) * 20.00

def generar_factura(datos):
    nombre, nit_usuario, No_placa, hora_entrada, hora_salida = datos
    tiempo_estancia = hora_salida - hora_entrada
    pago_total = total_pago(hora_entrada, hora_salida)

    print("\nResumen de la transacción")
    print("----------------------------------------------")
    print(f"Nombre: {nombre}")
    print(f"NIT: {nit_usuario}")
    print(f"Número de Placa: {No_placa}")
    print(f"Hora de entrada: {hora_entrada} [h.m]")
    print(f"Hora de salida: {hora_salida} [h.m]")
    print(f"Tiempo total en el parqueo: {math.ceil(tiempo_estancia)} horas")
    print(f"Total a cancelar: Q{pago_total}")

    with open("factura.txt", "a") as f:
        f.write("----------------------------------------------\n")
        f.write(f"Nombre: {nombre}\n")
        f.write(f"NIT: {nit_usuario}\n")
        f.write(f"Número de Placa: {No_placa}\n")
        f.write(f"Hora de entrada: {hora_entrada} [h.m]\n")
        f.write(f"Hora de salida: {hora_salida} [h.m]\n")
        f.write(f"Tiempo total en el parqueo: {math.ceil(tiempo_estancia)} horas\n")
        f.write(f"Total a cancelar: Q{pago_total}\n")
        f.write("----------------------------------------------\n")

    conn = basePosgresql()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Parqueo (nombre, nit, placa, hora_entrada, hora_salida, tiempo_estancia, pago_total)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            (nombre, nit_usuario, No_placa, hora_entrada, hora_salida, math.ceil(tiempo_estancia), pago_total)
        )
        conn.commit()
        conn.close()

def basePosgresql():
    try:
        conn = psycopg2.connect(
            dbname="Tarea6",
            user="postgres",
            password="cindy123451",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

def historial_datos():
    try:
        with open("factura.txt", "r") as f:
            print("\n--- Historial de Facturas (Archivo) ---")
            print(f.read())

        conn = basePosgresql()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Parqueo;")
            registros = cursor.fetchall()
            print("\n--- Historial de Facturas (Base de Datos) ---")
            for registro in registros:
                print(registro)
            conn.close()
    except FileNotFoundError:
        print("El archivo 'factura.txt' no existe.")
    except Exception as e:
        print("Error al consultar el historial:", e)

def borrar_datos():
    try:
        if os.path.exists("factura.txt"):
            os.remove("factura.txt")
            print("El archivo 'factura.txt' fue eliminado correctamente.")
        else:
            print("El archivo 'factura.txt' no existe.")

        conn = basePosgresql()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Parqueo;")
            conn.commit()
            conn.close()
            print("Todos los datos han sido borrados de la base de datos.")
    except Exception as e:
        print("Error al borrar datos:", e)

menu()
