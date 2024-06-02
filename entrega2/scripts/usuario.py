import psycopg2
from psycopg2 import sql
from psycopg2 import Error
import crypt

def usuario():
    DB_HOST = 'pavlov.ing.puc.cl'
    DB_PORT = '5432'
    DB_USER = 'grupo8'
    DB_PASSWORD = 'bulla8'
    DB_NAME = 'grupo8e2'

    conn = None
    cursor = None
    error_msg = ["Tabla Usuario:"]

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
            for line in data[1:]:
                row = line.split(';')
                if len(row) == 6:
                    row[3] = crypt.crypt(row[3])
                    df.append(row[:-2])
        
        for row in df:
            try:
                insert_query = """INSERT INTO Usuario (nombre,email,telefono,clave,tipo) 
                                    VALUES (%s, %s, %s, %s, 'cliente')"""
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