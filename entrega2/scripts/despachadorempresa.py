import psycopg2
from psycopg2 import sql
from psycopg2 import Error
import crypt

def despachadorEmpresa():
    DB_HOST = 'pavlov.ing.puc.cl'
    DB_PORT = '5432'
    DB_USER = 'grupo8'
    DB_PASSWORD = 'bulla8'
    DB_NAME = 'grupo8e2'

    conn = None
    cursor = None
    error_msg = ["Tabla DespachadorEmpresa:"]


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
                    df.append([row[2], row[3]])
        

        for row in df:
            try:
                insert_query = """WITH empresa_cte AS (
                                    SELECT e.id AS empresa_id
                                    FROM empresa AS e
                                    WHERE e.nombre = %s
                                    ),
                                    despachador_cte AS (
                                    SELECT d.id AS despachador_id
                                    FROM despachador AS d
                                    WHERE d.nombre = %s
                                    )
                                    
                                    INSERT INTO DespachadorEmpresa (despachador_id, empresa_id)
                                    SELECT despachador_id, empresa_id
                                    FROM despachador_cte, empresa_cte;
                                    """
                
                cursor.execute(insert_query, row)  
                conn.commit()
            except (Exception, psycopg2.Error) as error:
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