import psycopg2
from psycopg2 import sql
from psycopg2 import Error
import crypt

def platoRestaurant():
    DB_HOST = 'pavlov.ing.puc.cl'
    DB_PORT = '5432'
    DB_USER = 'grupo8'
    DB_PASSWORD = 'bulla8'
    DB_NAME = 'grupo8e2'

    conn = None
    cursor = None
    error_msg = ["Tabla PlatoRestaurant:"]

    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME
        )
        with open('../CSV/platos.csv', 'r', encoding = 'ISO-8859-1') as file:
            data = file.read().split('\n')
            df = []
            for line in data[1:]:
                row = line.split(';')
                df.append([row[0], row[-3]])

        cursor = conn.cursor()

        for row in df:
            try:
                insert_query = """WITH plato_cte AS (
                                    SELECT p.id AS id
                                    FROM plato as p
                                    WHERE p.id = %s
                                    ),
                                    restaurant_cte AS (
                                    SELECT r.id AS id
                                    FROM restaurant as r
                                    WHERE r.nombre = %s
                                    )
                                    INSERT INTO PlatoRestaurant (plato_id, restaurant_id)
                                    SELECT plato_cte.id, restaurant_cte.id
                                    FROM plato_cte, restaurant_cte;
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