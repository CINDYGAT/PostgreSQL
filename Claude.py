import os
import math
import psycopg2

def basePosgresql():
    """Establece la conexión con la base de datos PostgreSQL."""
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

def ingresoDatos():
    """Función para ingresar datos de estacionamiento"""
    nombre = input("Ingrese el nombre del usuario: ").strip()
    if not nombre or nombre.isdigit():
        raise ValueError("El nombre no puede ser un número o estar vacío.")
                    
    nit_usuario = int(input("Ingrese el NIT del sin guiones ni espacios: "))
    if nit_usuario <= 0:
        raise ValueError("El NIT no puede ser un número negativo o estar vacío.")
                    
    No_placa = input("Ingrese la placa del carro: ").strip()
    if not No_placa or No_placa.isdigit():
        raise ValueError("Error en el ingreso de la placa. Por favor, intente de nuevo.")
        
    hora_entrada = float(input("Ingrese la hora de entrada al estacionamiento como Hora.Minutos: "))
    if hora_entrada <= 0:
        raise ValueError("La hora de entrada no puede ser un número negativo o estar vacío.")
        
    hora_salida = float(input("Ingrese la hora de salida del estacionamiento Hora.Minutos: "))
    if hora_salida <= 0:
        raise ValueError("La hora de salida no puede ser un número negativo o estar vacío.")
    
    # Calcular tiempo de estancia y pago total
    tiempo_estancia = hora_salida - hora_entrada
    tiempo_estancia_redondeado = math.ceil(tiempo_estancia)
    pago_total = total_pago(hora_entrada, hora_salida)
    
    # Guardar en base de datos
    conn = basePosgresql()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Parqueo (nombre, nit, placa, hora_entrada, hora_salida, tiempo_estancia, total_pagado) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nombre, nit_usuario, No_placa, hora_entrada, hora_salida, tiempo_estancia_redondeado, pago_total))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error al guardar en base de datos: {e}")
    
    # Generar factura
    generacion_factura(nombre, nit_usuario, No_placa, hora_entrada, hora_salida, tiempo_estancia_redondeado, pago_total)
    
    print("Información guardada correctamente.\n")

def total_pago(hora_entrada, hora_salida):
    """Calcular el total a pagar por estacionamiento"""
    tiempo_estancia = hora_salida - hora_entrada
    
    # Redondear hacia arriba para contabilizar fracciones de hora como hora completa
    horas_totales = math.ceil(tiempo_estancia)
    pago_total = 0
    # Calcular el pago
    if horas_totales == 1:
        # Primera hora tiene tarifa fija
        pago_total = 15.00
    else:
        # Primera hora + horas adicionales
        # La primera hora cuesta Q15, las siguientes Q20
        pago_total = 15.00 + (horas_totales - 1) * 20.00
    
    return pago_total

def generacion_factura(nombre, nit_usuario, No_placa, hora_entrada, hora_salida, tiempo_estancia, pago_total):
    """Generar factura en archivo de texto"""
    print("Resumen de la transacción")
    print("----------------------------------------------\n")
    print(f"Nombre: {nombre}")
    print(f"NIT: {nit_usuario}")
    print(f"Número de Placa: {No_placa}")
    print(f"Hora de entrada: {hora_entrada} [h.m]")
    print(f"Hora de salida: {hora_salida} [h.m]")
    print(f"Tiempo total en el parqueo: {tiempo_estancia}")
    print(f"Total a cancelar: Q{pago_total:.2f}\n")
    
    # Generar factura en archivo de texto
    with open("factura.txt", "a") as f:
        f.write("----------------------------------------------\n")
        f.write(f"Nombre: {nombre}\n")
        f.write(f"NIT: {nit_usuario}\n")
        f.write(f"Número de Placa: {No_placa}\n")
        f.write(f"Hora de entrada: {hora_entrada} [h.m]\n")
        f.write(f"Hora de salida: {hora_salida} [h.m]\n")
        f.write(f"Tiempo total en el parqueo: {tiempo_estancia}\n")
        f.write(f"Total a cancelar: Q{pago_total:.2f}\n")
        f.write("----------------------------------------------\n")
    
    print("Documento electrónico creado y guardado correctamente.\n")

def historial_datos():
    """Mostrar historial de datos del archivo y base de datos"""
    try:
        # Mostrar contenido del archivo de texto
        print("Leyendo el archivo de facturas...\n")
        with open("factura.txt", "r") as f:
            print(f.read())
        
        # Mostrar registros de la base de datos
        conn = basePosgresql()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Parqueo;")
            registros = cursor.fetchall()

            if registros:
                print("\n--- Historial de Parqueo ---")
                for registro in registros:
                    print(f"Nombre: {registro[0]}, NIT: {registro[1]}, Placa: {registro[2]}, "
                          f"Hora Entrada: {registro[3]}, Hora Salida: {registro[4]}, "
                          f"Tiempo de estancia: {registro[5]}, Total cancelado: {registro[6]}")
            else:
                print("No hay registros en la base de datos.")
            
            conn.close()
    except FileNotFoundError:
        print("El archivo 'factura.txt' no existe. No hay datos para mostrar.") 
    except Exception as e:
        print("Error al consultar los datos:", e)

def borrar_datos():
    """Borrar datos del archivo de texto y base de datos"""
    try:
        # Eliminar archivo de texto
        if os.path.exists("factura.txt"):
            os.remove("factura.txt")
            print("El archivo de facturas fue eliminado correctamente")
        else:
            print("El archivo de facturas no existe")
        
        # Eliminar registros de la base de datos
        conn = basePosgresql()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Parqueo;")
            conn.commit()
            conn.close()
            print("Todos los datos han sido borrados de la base de datos.")
    except Exception as e:
        print(f"Error al borrar datos: {e}")

def menu():
    """Menú principal del sistema de parqueo"""
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
            
            # Validar rango de opción
            if opcion < 1 or opcion > 5:
                print("Entrada inválida. Por favor, ingrese un número entre 1 y 5.\n")
                continue

            # Procesar las opciones
            if opcion == 1:  # ingreso de datos de facturacion
                try:
                    ingresoDatos()  
                except ValueError as e:
                    print(f"Error: {e}")              

            elif opcion == 2: # Generación de factura
                print("La factura se genera automáticamente al ingresar los datos.")

            elif opcion == 3:  # Historial de datos
                try:
                    historial_datos()
                except Exception as e:
                    print(f"Error al mostrar los datos: {e}")
                    
            elif opcion == 4:  # Borrar datos
                borrar_datos()
            
            elif opcion == 5:  # opcion Salir
                print("¡Gracias por visitarnos. Vuelva pronto!\n")
                break
            
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.\n")

# Ejecutar el menú principal
if __name__ == "__main__":
    menu()