import psycopg2
from psycopg2 import sql
from psycopg2 import Error
import crypt
DB_HOST = 'pavlov.ing.puc.cl'
DB_PORT = '5432'
DB_USER = 'grupo8'
DB_PASSWORD = 'bulla8'
DB_NAME = 'grupo8e2'

conn = None
cursor = None

table_name = "DireccionUsuario"

try:
    # Conexión con la base de datos
    conn = psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME
    )
    # Crear un cursor para ejecutar consultas
    cursor = conn.cursor()

    # Abrir CSV
    with open('../CSV/clientes.csv', 'r', encoding = 'ISO-8859-1') as file:
        data = file.read().split('\n')
        df = []
        cuts = []
        calles = []
        numeros = []
        for line in data[1:]:
            row = line.split(';')
            if len(row) == 6:
                
                cliente = row[0]
                direccion = row[-2:]
                cuts = direccion[-1]
                calle = ' '.join(direccion[0].split(',')[0].split(' ')[:-1])
                numero = direccion[0].split(',')[0].split(' ')[-1]

                df.append([cliente, cuts, calle, numero])


    exitos = 0
    fallos = 0
    
    for row in df:
        try:
            insert_query = """WITH cliente_cte AS (
                                SELECT id AS usuario_id
                                FROM usuario as u
                                WHERE u.nombre = %s
                                ),
                                direccion_cte AS (
                                    SELECT d.id AS direccion_id
                                    FROM direccion d
                                    WHERE d.comuna_cut = %s AND d.calle = %s AND d.numero = %s
                                )
                                INSERT INTO DireccionUsuario (usuario_id, direccion_id)
                                SELECT c.usuario_id, d.direccion_id
                                FROM cliente_cte c, direccion_cte d
                            """
            
            cursor.execute(insert_query, row)
            
            exitos += 1
        except (Exception, Error) as error:
            print(error)
            fallos += 1
            pass
        conn.commit()


    print("Data loaded successfully for {} rows in table {}.".format(exitos, table_name))
    print("Data loaded unsuccessfully for {} rows".format(fallos))
except (Exception, Error) as error:
    print("Error loading data:", error)
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()