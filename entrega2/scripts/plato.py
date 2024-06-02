import psycopg2
from psycopg2 import sql
from psycopg2 import Error
import crypt

def plato():
    DB_HOST = 'pavlov.ing.puc.cl'
    DB_PORT = '5432'
    DB_USER = 'grupo8'
    DB_PASSWORD = 'bulla8'
    DB_NAME = 'grupo8e2'

    conn = None
    cursor = None
    error_msg = ["Tabla Plato:"]

    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME
        )
        cursor = conn.cursor()

        with open('../CSV/platos.csv', 'r', encoding = 'ISO-8859-1') as file:
            data = file.read().split('\n')
            df = []
            for line in data[1:]:
                df.append(line.split(';')[:-3])
        for row in df:
            try:
                insert_query = """INSERT INTO Plato (id,nombre,descripcion,disponibilidad,estilo,restriccion,ingredientes,porciones,precio,tiempo) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(insert_query, row)
                conn.commit()
            except (Exception, Error) as error:
                if 'value too long for type character' in str(error):
                    largo_columna = int(str(error).split(' ')[-1].replace('varying(', '').replace(')', ''))
                    if len(row[1]) > largo_columna:
                        try:
                            conn.rollback()
                            cursor.execute("ALTER TABLE Plato ALTER COLUMN nombre TYPE VARCHAR(%s) NOT NULL", [len(row[1])])
                            cursor.execute(insert_query, row)
                            conn.commit()
                        except (Exception, Error) as error:
                            error_msg.append([error, row])
                            conn.rollback()

                    else:
                        error_msg.append([error, row])
                        conn.rollback()
                else:
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