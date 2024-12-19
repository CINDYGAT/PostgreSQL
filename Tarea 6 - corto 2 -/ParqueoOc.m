clc;
clear;

% Cargar el paquete de base de datos
pkg load database

% Variables globales para almacenar los datos del cliente y la conexión a la base de datos
global datos_cliente conn;
datos_cliente = struct();

try
    % Conectar a la base de datos
    conn = pq_connect(setdbopts('dbname', 'Tarea6', 'host', 'localhost', 'port', '5432', 'user', 'postgres', 'password', 'cindy123451'));
    disp('Conexión a la base de datos establecida.');
catch ME
    error('No se pudo conectar a la base de datos: %s', ME.message);
end

function menu()
    global datos_cliente;
    opcion = 0;
    while opcion ~= 5
        fprintf('\n\t\t¡Bienvenido al Menú Principal!\n');
        fprintf('1. Ingresar datos de facturación\n');
        fprintf('2. Generación de factura\n');
        fprintf('3. Historial de datos\n');
        fprintf('4. Borrar datos\n');
        fprintf('5. Salir\n');

        opcion = input('Seleccione una opción: ');
        switch opcion
            case 1
                ingresoDatos();
            case 2
                if ~isempty(datos_cliente)
                    generar_factura();
                else
                    fprintf('Primero debe ingresar los datos del cliente (opción 1).\n');
                end
            case 3
                historial_datos();
            case 4
                borrar_datos();
            case 5
                fprintf('¡Gracias por visitarnos! Vuelva pronto.\n');
            otherwise
                fprintf('Opción no válida. Intente nuevamente.\n');
        end
    end
end

function ingresoDatos()
    global datos_cliente;
    try
        datos_cliente.nombre = input('Ingrese el nombre del usuario: ', 's');
        if isempty(datos_cliente.nombre)
            error('El nombre no puede estar vacío.');
        end

        datos_cliente.nit = input('Ingrese el NIT del usuario (sin guiones ni espacios): ', 's');
        if ~all(isstrprop(datos_cliente.nit, 'digit'))
            error('El NIT debe contener solo números.');
        end

        datos_cliente.placa = input('Ingrese la placa del carro: ', 's');
        if isempty(datos_cliente.placa)
            error('La placa no puede estar vacía.');
        end

        datos_cliente.entrada = input('Ingrese la hora de entrada (Hora.Minutos): ');
        datos_cliente.salida = input('Ingrese la hora de salida (Hora.Minutos): ');
        if datos_cliente.salida <= datos_cliente.entrada
            error('La hora de salida debe ser mayor que la hora de entrada.');
        end
        fprintf('Datos ingresados correctamente.\n');
    catch ME
        fprintf('Error: %s\n', ME.message);
    end
end

function total = total_pago(hora_entrada, hora_salida)
    tiempo_estancia = hora_salida - hora_entrada;
    horas_totales = ceil(tiempo_estancia);
    if horas_totales == 1
        total = 15.00;
    else
        total = 15.00 + (horas_totales - 1) * 20.00;
    end
end

function generar_factura()
    global datos_cliente conn;
    try
        tiempo_estancia = datos_cliente.salida - datos_cliente.entrada;
        pago_total = total_pago(datos_cliente.entrada, datos_cliente.salida);

        factura = sprintf([...
            '----------------------------------------------\n', ...
            'Nombre: %s\n', ...
            'NIT: %s\n', ...
            'Placa: %s\n', ...
            'Hora de entrada: %.2f [h.m]\n', ...
            'Hora de salida: %.2f [h.m]\n', ...
            'Tiempo de estancia: %.2f horas\n', ...
            'Total a pagar: Q%.2f\n', ...
            '----------------------------------------------\n'], ...
            datos_cliente.nombre, datos_cliente.nit, datos_cliente.placa, ...
            datos_cliente.entrada, datos_cliente.salida, tiempo_estancia, pago_total);

        fprintf('Factura generada:\n');
        fprintf('%s\n', factura);

        % Guardar en la base de datos
        try
            query = sprintf("insert into parqueo values ('%s', '%s', '%s', '%.2f', '%.2f', '%.2f', '%.2f');", ...
                datos_cliente.nombre, datos_cliente.nit, datos_cliente.placa, ...
                datos_cliente.entrada, datos_cliente.salida, tiempo_estancia, pago_total);
            pq_exec_params(conn, query);
            disp('Factura guardada en la base de datos.');
        catch ME
            fprintf('Error al guardar en la base de datos: %s\n', ME.message);
        end

        % Guardar la factura en un archivo de texto
        archivo = 'C:\\Users\\Melissa A\\Documents\\Cursos 2do semestre 2024\\proyectos IE\\Tarea 6 - corto 2 -\\facturas.txt';
        fid = fopen(archivo, 'a');
        fprintf(fid, '%s', factura);
        fclose(fid);
        fprintf('Factura guardada en "facturas.txt".\n');
    catch ME
        fprintf('Error al generar la factura: %s\n', ME.message);
    end
end

function historial_datos()
    global conn;
    try
        N = pq_exec_params(conn, "select * from parqueo;");
        disp('---------------------------------------------------')
        disp('Historial de datos desde la base de datos:');
        disp(N.data);
        disp('---------------------------------------------------')
    catch ME
        fprintf('Error al obtener el historial: %s\n', ME.message);
    end
end

function borrar_datos()
    global conn;
    try
        pq_exec_params(conn, "delete from parqueo;");
        fprintf('Todos los registros de la base de datos han sido eliminados.\n');
    catch ME
        fprintf('Error al borrar los datos de la base de datos: %s\n', ME.message);
    end
end

% Ejecutar el menú principal
menu();

% Cerrar la conexión a la base de datos al finalizar
pq_close(conn);

