import psycopg2
from psycopg2 import sql
from psycopg2 import Error
import crypt
def comuna():
    DB_HOST = 'pavlov.ing.puc.cl'
    DB_PORT = '5432'
    DB_USER = 'grupo8'
    DB_PASSWORD = 'bulla8'
    DB_NAME = 'grupo8e2'

    conn = None
    cursor = None
    error_msg = ["Tabla Comuna:"]


    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME
        )
        cursor = conn.cursor()

        with open('../CSV/comuna2.csv', 'r', encoding = 'mac_roman') as file:
            data = file.read().split('\n')
            df = []
            for line in data[1:]:
                df.append(line.split(';'))
        for row in df:
            try:
                insert_query = """INSERT INTO Comuna (cut,nombre,provincia,region) 
                                    VALUES (%s, %s, %s, %s)"""
                cursor.execute(insert_query, row)
                conn.commit()
            except (Exception, Error) as error:
                error_msg.append([error, row])
                conn.rollback()

        conn.commit()
    except (Exception, Error) as error:
        error_msg.append(error)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    return error_msg