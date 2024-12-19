import os
import math
import psycopg2

# Variables globales para almacenar los datos del cliente
datos_cliente = {}

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
            if opcion == 1:
                ingresoDatos()
            elif opcion == 2:
                if datos_cliente:
                    generar_factura()
                else:
                    print("Primero debe ingresar los datos del cliente (opción 1).")
            elif opcion == 3:
                historial_datos()
            elif opcion == 4:
                borrar_datos()
            elif opcion == 5:
                print("¡Gracias por visitarnos! Vuelva pronto.")
            else:
                print("Opción no válida. Intente nuevamente.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.\n")

def ingresoDatos():
    global datos_cliente
    try:
        nombre = input("Ingrese el nombre del usuario: ").strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")

        nit_usuario = input("Ingrese el NIT del usuario (sin guiones ni espacios): ").strip()
        if not nit_usuario.isdigit():
            raise ValueError("El NIT debe contener solo números.")

        No_placa = input("Ingrese la placa del carro: ").strip()
        if not No_placa:
            raise ValueError("La placa no puede estar vacía.")

        hora_entrada = float(input("Ingrese la hora de entrada (Hora.Minutos): "))
        hora_salida = float(input("Ingrese la hora de salida (Hora.Minutos): "))
        if hora_salida <= hora_entrada:
            raise ValueError("La hora de salida debe ser mayor que la hora de entrada.")

        datos_cliente = {
            "nombre": nombre,
            "nit": nit_usuario,
            "placa": No_placa,
            "entrada": hora_entrada,
            "salida": hora_salida
        }
        print("Datos ingresados correctamente.")
    except ValueError as e:
        print(f"Error: {e}")

def total_pago(hora_entrada, hora_salida):
    tiempo_estancia = hora_salida - hora_entrada
    horas_totales = math.ceil(tiempo_estancia)
    if horas_totales == 1:
        return 15.00
    return 15.00 + (horas_totales - 1) * 20.00

def generar_factura():
    global datos_cliente
    try:
        tiempo_estancia = datos_cliente["salida"] - datos_cliente["entrada"]
        pago_total = total_pago(datos_cliente["entrada"], datos_cliente["salida"])

        factura = (
            "----------------------------------------------\n"
            f"Nombre: {datos_cliente['nombre']}\n"
            f"NIT: {datos_cliente['nit']}\n"
            f"Placa: {datos_cliente['placa']}\n"
            f"Hora de entrada: {datos_cliente['entrada']} [h.m]\n"
            f"Hora de salida: {datos_cliente['salida']} [h.m]\n"
            f"Tiempo de estancia: {tiempo_estancia:.2f} horas\n"
            f"Total a pagar: Q{pago_total:.2f}\n"
            "----------------------------------------------\n"
        )

        print("Factura generada:")
        print(factura)

        with open("/home/cindy/Documentos/cursos 2024/Proyecto IE/tarea6/facturas.txt", "a") as f:
            f.write(factura)
        print("Factura guardada en 'factura.txt'.")
    except Exception as e:
        print(f"Error al generar la factura: {e}")

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
        with open("/home/cindy/Documentos/cursos 2024/Proyecto IE/tarea6/facturas.txt", "r") as f:
            print("Historial del archivo:\n")
            print(f.read())
        
        conn = basePosgresql()
        if conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM "parqueo";')
            registros = cursor.fetchall()
            print("\n--- Historial en la base de datos ---")
            for registro in registros:
                print(registro)
            conn.close()
    except FileNotFoundError:
        print("El archivo 'factura.txt' no existe.")
    except Exception as e:
        print(f"Error: {e}")

def borrar_datos():
    try:
        if os.path.exists("/home/cindy/Documentos/cursos 2024/Proyecto IE/tarea6/facturas.txt"):
            os.remove("/home/cindy/Documentos/cursos 2024/Proyecto IE/tarea6/facturas.txt")
            print("Archivo 'factura.txt' eliminado.")
        else:
            print("El archivo 'factura.txt' no existe.")

        conn = basePosgresql()
        if conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM "parqueo";')
            conn.commit()
            conn.close()
            print("Datos eliminados de la base de datos.")
    except Exception as e:
        print(f"Error al borrar datos: {e}")

# Ejecutar el menú principal
menu()