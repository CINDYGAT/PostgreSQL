pkg load database

% Conectar a la base de datos
conn = pq_connect(setdbopts('dbname', 'primerParcial', 'host', 'localhost', 'port', '5432', 'user', 'postgres', 'password', 'cindy123451'));

% Insertar un registro
try
    pq_exec_params(conn, "INSERT INTO factorial (nombre, numero, factorial) VALUES ('conectar base', 5, 120);");
    disp("Registro insertado correctamente.");
catch ME
    fprintf("Error al insertar registro: %s\n", ME.message);
end

% Obtener registros
try
    N = pq_exec_params(conn, "select * from factorial;");
    disp("Registros obtenidos:");
    disp(N.data);
catch ME
    fprintf("Error al obtener registros: %s\n", ME.message);
end

% Cerrar la conexión
pq_close(conn);
