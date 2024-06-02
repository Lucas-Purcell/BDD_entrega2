import psycopg2
from psycopg2 import sql
from psycopg2 import Error
import crypt

def direccionUsuario():
    DB_HOST = 'pavlov.ing.puc.cl'
    DB_PORT = '5432'
    DB_USER = 'grupo8'
    DB_PASSWORD = 'bulla8'
    DB_NAME = 'grupo8e2'

    conn = None
    cursor = None
    error_msg = ["Tabla DireccionUsuario:"]

    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME
        )
        cursor = conn.cursor()

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
                conn.commit()
            except (Exception, Error) as error:
                error_msg.append([error, row])
                conn.rollback()

    except (Exception, Error) as error:
        error_msg.append(error)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return error_msg