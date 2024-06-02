import psycopg2
from psycopg2 import sql
from psycopg2 import Error
import crypt

def pedido():
    DB_HOST = 'pavlov.ing.puc.cl'
    DB_PORT = '5432'
    DB_USER = 'grupo8'
    DB_PASSWORD = 'bulla8'
    DB_NAME = 'grupo8e2'

    conn = None
    cursor = None
    error_msg = ["Tabla Pedido:"]

    try:
        conn = psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME
        )
        cursor = conn.cursor()

        with open('../CSV/pedidos2.csv', 'r', encoding = 'ISO-8859-1') as file:
            data = file.read().split('\n')
            header = data[0].split(';')
            df = []
            for line in data[1:]:
                row = line.split(';')
                if len(row) == 8:
                    df.append({h: r for h, r in zip(header, row)})
        for row in df:
            try:
                insert_query = """WITH usuario_cte AS (
                                    SELECT u.id AS usuario_id
                                    FROM usuario as u
                                    WHERE u.email = %s
                                    )

                                INSERT INTO Pedido (usuario_id, id, fecha, hora, estado)
                                SELECT usuario_cte.usuario_id, %s, %s, %s, TRIM(%s)
                                FROM usuario_cte;
                                """
                
                keys_to_extract = ['cliente', 'id','fecha', 'hora', 'estado']
                extracted = [row[key] for key in keys_to_extract]
                cursor.execute("SET DateStyle = 'ISO, DMY';")
                cursor.execute(insert_query, extracted)    
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

    try:
        conn = psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME
        )
        cursor = conn.cursor()

        with open('../CSV/calificacion.csv', 'r', encoding = 'ISO-8859-1') as file:
            data = file.read().split('\n')
            cal = []
            for line in data[1:]:
                row = line.split(';')
                if len(row) == 3:
                    cal.append(row)

        for row in cal:
            try:
                update_query = """UPDATE Pedido SET evaluacion_cliente = %s, evaluacion_servicio = %s WHERE id = %s"""
                cursor.execute(update_query, row[::-1])
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