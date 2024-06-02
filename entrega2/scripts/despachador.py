import psycopg2
from psycopg2 import sql
from psycopg2 import Error
import crypt

def despachador():
    DB_HOST = 'pavlov.ing.puc.cl'
    DB_PORT = '5432'
    DB_USER = 'grupo8'
    DB_PASSWORD = 'bulla8'
    DB_NAME = 'grupo8e2'

    conn = None
    cursor = None
    error_msg = ["Tabla Despachador:"]

    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME
        )
        # Crear un cursor para ejecutar consultas
        cursor = conn.cursor()
        
        with open('../CSV/cldeldes.csv', 'r', encoding = 'ISO-8859-1') as file:
            data = file.read().split('\n')
            
            df = []
            for line in data[1:]:
                row = line.split(';')
                if len(row) == 13:
                    df.append(row[-2:])
        exitos = 0
        fallos = 0
        
        for row in df:
            try:
                insert_query = """INSERT INTO Despachador (nombre, telefono) 
                                VALUES (%s, %s)
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