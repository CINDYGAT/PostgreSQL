pkg load database

% Conectar a la base de datos
conn = pq_connect(setdbopts('dbname', 'Tarea6', 'host', 'localhost', 'port', '5432', 'user', 'postgres', 'password', 'cindy123451'));

% Insertar un registro
try
    pq_exec_params(conn, "insert into parqueo values ('Lucas', '4565263','P056LKL', '18.5', '20.53','2.03','35');");
    disp("Registro insertado correctamente.");
catch ME
    fprintf("Error al insertar registro: %s\n", ME.message);
end

% Obtener registros
try
    N = pq_exec_params(conn, "select * from parqueo;");
    disp("Registros obtenidos:");
    disp(N.data);
catch ME
    fprintf("Error al obtener registros: %s\n", ME.message);
end

% Cerrar la conexión
pq_close(conn);
