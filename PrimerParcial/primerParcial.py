import psycopg2
from psycopg2 import sql
import math
import datetime
import getpass
import os

# Variables globales para almacenar los datos del cliente
resultados = {}

# Menú principal
def menu():
    opcion = 0
    while opcion != 10:
        print("\n\t\t¡Bienvenido al Menú Principal!")
        print("1. Ingresar nombre usuario")
        print("2. Calcular factorial")
        print("3. Sistema login")
        print("4. Calcular distancia entre dos puntos")
        print("5. Calcular IMC")
        print("6. Sueldo base semanal")
        print("7. Visualizar archivo de texto")
        print("8. Historial de datos")
        print("9. Borrar datos")
        print("10. Salir")
        try:
            opcion = int(input("Seleccione una opción: "))
            if opcion == 1:
                ingreso_datos()
            elif opcion == 2:
                calcular_factorial()
            elif opcion == 3:
                sistema_login()
            elif opcion == 4:
                calcular_distancia()
            elif opcion == 5:
                calcular_imc()
            elif opcion == 6:
                calcular_nomina()
            elif opcion == 7:
                visualizar_archivo()
            elif opcion == 8:
                #imprimir_resultados()
                mostrar_historial()
            elif opcion == 9:
                borrar_datos()
            elif opcion == 10:
                print("¡Gracias por visitarnos! Vuelva pronto.")
            else:
                print("Opción no válida. Intente nuevamente.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entre 1 y 9.")

# Función para ingresar nombre
def ingreso_datos():
    global resultados
    try:
        nombre = input("Ingrese el nombre del usuario: ").strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        print(f"Datos ingresados correctamente: {nombre}")

        resultados["nombre"] = nombre #guarde nombre en variable global resultados
        #print(f"Nombre guardado: {resultados['nombre']}")
    except Exception as e:
        print(f"Error: {e}")

# Calcular factorial
def calcular_factorial():
    global resultados
    try:
        while True:
            x = int(input("Ingresa un número entero positivo: "))
            resultados["x"] = x

            if x < 0:
                print("Error: El número debe ser positivo.")
            else:
                break
        factorial = math.factorial(x)
        print(f"El factorial de {x} es {factorial}")
        #almacenar datos en la variable global
        resultados["factorial"] = factorial     
    except ValueError:
        print("Error: Debe ingresar un número entero.")

# Sistema login
def sistema_login():
    global resultados
    intentos = 3
    try:
        while intentos > 0:
            usuario = input("Ingrese el nombre de usuario: ")
            resultados["usuario"] = usuario
            contrasena = getpass.getpass("Introduce tu contraseña: ")
            resultados["Contrasena"] = contrasena
            if usuario == "admin" and contrasena == "123":
                print("¡Inicio de sesión exitoso!")
                return
            else:
                intentos -= 1
                print(f"Credenciales incorrectas. Intentos restantes: {intentos}")
                if intentos == 0:
                    print("Has agotado todos los intentos. Cerrando el programa.")
                    return
            resultados["intentos"] = intentos
    except Exception as e:
        print(f"Error: {e}")     

# Calcular distancia
def calcular_distancia():
    global resultados
    try:
        x1 = float(input("x1 = "))
        y1 = float(input("y1 = "))
        x2 = float(input("x2 = "))
        y2 = float(input("y2 = "))
        resultados["x1"] = x1
        resultados["y1"] = y1
        resultados["x2"] = x2
        resultados["y2"] = y2
        distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        resultados["distancia"] = distancia
        print(f"La distancia entre ({x1}, {y1}) y ({x2}, {y2}) es: {distancia:.4f}")
    except ValueError:
        print("Error: Las coordenadas deben ser valores numéricos.")

# Calcular IMC
def calcular_imc():
    global resultados
    try:
        genero = input("Ingrese su género ('hombre' o 'mujer'): ").strip().lower()
        resultados["genero"] = genero
        if genero not in ["hombre", "mujer"]:
            raise ValueError("Debe ingresar 'hombre' o 'mujer'.")
        peso = float(input("Ingrese su peso (kg): "))
        altura = float(input("Ingrese su altura (m): "))
        resultados["peso"] = peso
        resultados["altura"] = altura
        if peso <= 0 or altura <= 0:
            raise ValueError("Peso y altura deben ser positivos.")
        imc = peso / (altura ** 2)
        resultados["imc"] = imc
        print(f"Su IMC es: {imc:.2f}")
        if imc < 18.5:
            print("Bajo peso, consulte a su médico.")
        elif imc < 24.9:
            print("Peso normal, continúe con buenos hábitos.")
        elif imc < 29.9:
            print("Sobrepeso, considere una rutina de ejercicios.")
        else:
            print("Obesidad, consulte a su médico para un plan adecuado.")
    except ValueError as e:
        print(f"Error: {e}")

# Calcular nómina
def calcular_nomina():
    global resultados
    PRECIO_HORA = 6
    try:
        horas_trabajo = int(input("Ingrese horas trabajadas: "))
        horas_extras = int(input("Ingrese horas extras: "))
        resultados["horas_trabajo"] = horas_trabajo
        resultados["horas_extras"] = horas_extras
        if horas_extras < 10:
            precio_extra = PRECIO_HORA * 1.5
        elif horas_extras <= 20:
            precio_extra = PRECIO_HORA * 1.4
        else:
            precio_extra = PRECIO_HORA * 1.2
        sueldo = (horas_trabajo * PRECIO_HORA) + (horas_extras * precio_extra)
        resultados["precio_extra"] = precio_extra
        resultados["sueldo"] = sueldo
        print(f"Sueldo base semanal: {sueldo:.2f}")
    except ValueError:
        print("Error: Ingrese valores numéricos.")

# Visualizar archivos txt
def visualizar_archivo():
    global resultados
    try:
 # Acceder a los valores de resultados correctamente
        salida = (
            "----------------------------------------------\n"
            f"Nombre: {resultados.get('nombre', 'N/A')}\n"
            f"Tipo de operacion: Funcion factorial\n"
            f"x: {resultados.get('x', 'N/A')}\n"
            f"Factorial: {resultados.get('factorial', 'N/A')}\n"
            f"----------------------------------------------\n"
            f"Tipo de operacion: Login\n"
            f"Intentos: {resultados.get('intentos', 'N/A')} \n"
            f"Usuario: {resultados.get('usuario', 'N/A')} \n"
            f"Contraseña: {resultados.get('contrasena', 'N/A')} \n"
            f"----------------------------------------------\n"
            f"Tipo de operacion: Distancia\n"
            f"x1: {resultados.get('x1', 0):.2f}\n"
            f"y1: {resultados.get('y1', 0):.2f}\n"
            f"x2: {resultados.get('x2', 0):.2f}\n"
            f"y2: {resultados.get('y2', 0):.2f}\n"
            f"Distancia: {resultados.get('distancia', 0):.2f}\n"
            f"----------------------------------------------\n"
            f"Tipo de operacion: IMC\n"
            f"Género: {resultados.get('genero', 'N/A')}\n"
            f"Peso: {resultados.get('peso', 0):.2f}\n"
            f"Altura: {resultados.get('altura', 0):.2f}\n"
            f"IMC: {resultados.get('imc', 0):.2f}\n"
            f"----------------------------------------------\n"
            f"Tipo de operacion: Sueldo Semanal \n"
            f"Horas trabajadas: {resultados.get('horas_trabajo', 0):.2f}\n"
            f"Horas extras: {resultados.get('horas_extras', 0):.2f}\n"
            f"Precio hora extra: {resultados.get('precio_extra', 0):.2f}\n"
            f"Sueldo semanal: {resultados.get('sueldo', 0):.2f}\n"
            "----------------------------------------------\n"
        )

        print("Archivo txt generado:")
        print(salida)

        with open("C:/Users/karen/Downloads/Primer Parcial/salidap.txt", "a") as f:
            f.write(salida)
        print("Archivo guardado en 'salidap.txt'.")
    except Exception as e:
        print(f"Error al generar la factura: {e}")

#Conectar a la base de datos 
def basePosgresql():
    try:
        conn = psycopg2.connect(
            dbname="primerParcial",
            user="postgres",
            password="cindy123451",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None
    
# Mostrar historial
def mostrar_historial():
    global resultados
# Extraer valores desde el diccionario
    Nombre = resultados.get("nombre")
    Numero = resultados.get("x")
    Factorial = resultados.get("factorial")

    usuario = resultados.get("usuario")
    contrasena = resultados.get("Contrasena")
    Intentos = resultados.get("intentos") 

    x1 = resultados.get("x1") 
    y1 = resultados.get("y1") 
    x2 = resultados.get("x2") 
    y2 = resultados.get("y2")  
    distancia = resultados.get("distancia")

    genero = resultados.get("genero")
    peso = resultados.get("peso")
    altura = resultados.get("altura")
    imc = resultados.get("imc")

    horas_trabajo = resultados.get("horas_trabajo") 
    horas_extras = resultados.get("horas_extras")
    precio_extra = resultados.get("precio_extra") 
    sueldo = resultados.get("sueldo") 


    """Inserta datos en las tablas."""
    try:
        conn = basePosgresql()
        if conn:
            cursor = conn.cursor()
            # Query para insertar datos
            query = 'INSERT INTO factorial("nombre", "numero", "factorial") VALUES (%s, %s, %s)'
            cursor.execute(query, (Nombre, Numero, Factorial))

            query = 'INSERT INTO login("nombre", "intentos", "usuario", "contrasena") VALUES (%s, %s, %s, %s)'
            cursor.execute(query, (Nombre, Intentos, usuario, contrasena))

            query = 'INSERT INTO distancia("nombre", "x1", "y1", "x2", "y2", "distancia") VALUES (%s, %s, %s, %s, %s, %s)'
            cursor.execute(query, (Nombre, x1, y1, x2, y2, distancia))

            query = 'INSERT INTO imc("nombre", "genero", "peso", "altura", "imc") VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(query, (Nombre, genero, peso, altura, imc))

            query = 'INSERT INTO nominas("nombre", "Horas_trabajo", "horas_extra", "precio_hora_extra", "sueldo_base") VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(query, (Nombre, horas_trabajo, horas_extras, precio_extra, sueldo))

            conn.commit()
            conn.close()
            print("Datos insertados en la base de datos correctamente.")

        conn = basePosgresql()
        if conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM factorial;')
            cursor.execute('SELECT * FROM login;')
            cursor.execute('SELECT * FROM distancia;')
            cursor.execute('SELECT * FROM imc;')
            cursor.execute('SELECT * FROM nominas;')
            registros = cursor.fetchall()
            print("\n--- Historial en la base de datos ---")
            for registro in registros:
                print(registro)
            conn.close()
    except Exception as e:
        print(f"Error al insertar en la base de datos: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Borrar datos
def borrar_datos():
    try:
        if os.path.exists("C:/Users/karen/Downloads/Primer Parcial/salidap.txt"):
            os.remove("C:/Users/karen/Downloads/Primer Parcial/salidap.txt")
            print("Archivo 'salidap.txt' eliminado.")
        else:
            print("El archivo 'salidap.txt' no existe.")

        conn = basePosgresql()
        if conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM factorial;')
            cursor.execute('DELETE FROM login;')
            cursor.execute('DELETE FROM distancia;')
            cursor.execute('DELETE FROM imc;')
            cursor.execute('DELETE FROM nominas;')
            conn.commit()
            conn.close()
            print("Datos eliminados de la base de datos.")
    except Exception as e:
        print(f"Error al borrar datos: {e}")


##################################################################
def imprimir_resultados():
    global resultados
    if not resultados:
        print("No hay datos almacenados en resultados.")
        return
    print("\nValores almacenados en resultados:")
    for clave, valor in resultados.items():
        print(f"{clave}: {valor}")
###############################################################################

# Ejecutar el menú
if __name__ == "__main__":
    menu()
