import psycopg2
from psycopg2 import sql
from psycopg2 import Error
import crypt

def servicioDespacho():
    DB_HOST = 'pavlov.ing.puc.cl'
    DB_PORT = '5432'
    DB_USER = 'grupo8'
    DB_PASSWORD = 'bulla8'
    DB_NAME = 'grupo8e2'

    conn = None
    cursor = None
    error_msg = ["Tabla ServicioDespacho:"]

    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME
        )
        cursor = conn.cursor()

        with open('../CSV/pedidos2.csv', 'r', encoding='ISO-8859-1') as file:
            data = file.read().split('\n')
            df = []
            for line in data[1:]:
                row = [s for s in line.split(';')]
                if len(row) == 8:
                    id_list = [int(x) for x in row[4].split()] 
                    df.append([row[0], id_list, row[3]])

        for row in df:
            try:
                insert_query = """
                WITH pedido_cte AS (
                    SELECT p.id AS pedido_id
                    FROM pedido AS p
                    WHERE p.id = %s
                ),
                rest_cte AS (
                    SELECT r.id AS restaurant_id
                    FROM restaurant AS r JOIN platoRestaurant AS pr ON r.id = pr.restaurant_id
                    WHERE pr.plato_id = ANY(%s)
                ),
                despachador_cte AS (
                    SELECT d.id AS despachador_id
                    FROM despachador AS d
                    WHERE d.nombre = %s
                )
                INSERT INTO ServicioDespacho (pedido_id, despachador_id, restaurant_id)
                SELECT pedido_id, despachador_id, restaurant_id
                FROM pedido_cte, despachador_cte, rest_cte;
                """
                
                cursor.execute(insert_query, row) 
                conn.commit()

            except (Exception, Error) as error:
                error_msg.append([error, row])
                conn.rollback()
    except (Exception, psycopg2.Error) as error:
        error_msg.append(error)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return error_msg