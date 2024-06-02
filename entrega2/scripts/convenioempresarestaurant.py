import psycopg2
from psycopg2 import sql
from psycopg2 import Error
import crypt

def convenioEmpresaRestaurant():
    DB_HOST = 'pavlov.ing.puc.cl'
    DB_PORT = '5432'
    DB_USER = 'grupo8'
    DB_PASSWORD = 'bulla8'
    DB_NAME = 'grupo8e2'

    conn = None
    cursor = None
    error_msg = ["Tabla ConvenioEmpresaRestaurant:"]

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
            df = []
            for line in data[1:]:
                row = line.split(';')
                if len(row) == 8:
                    df.append([row[2], row[4]])
        
        
        for row in df:
            try:
                row[1] = tuple(row[1].split())
                insert_query = """WITH empresa_cte AS (
                                    SELECT id AS empresa_id
                                    FROM empresa as e
                                    WHERE e.nombre = %s
                                ),

                                restaurant_cte AS (
                                        SELECT pr.restaurant_id AS restaurant_id
                                        FROM platoRestaurant pr
                                        WHERE pr.plato_id IN %s 
                                )
                                INSERT INTO ConvenioEmpresaRestaurant (empresa_id, restaurant_id)
                                SELECT e.empresa_id, r.restaurant_id
                                FROM empresa_cte e, restaurant_cte r
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