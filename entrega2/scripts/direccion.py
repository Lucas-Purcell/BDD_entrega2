import psycopg2
from psycopg2 import sql
from psycopg2 import Error
import crypt

def direccion():
    DB_HOST = 'pavlov.ing.puc.cl'
    DB_PORT = '5432'
    DB_USER = 'grupo8'
    DB_PASSWORD = 'bulla8'
    DB_NAME = 'grupo8e2'

    conn = None
    cursor = None
    error_msg = ["Tabla Direccion:"]

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
                row = line.split(';')[-2:]
                if len(row) == 2:
                    direccion = [' '.join(row[0].split(',')[0].split()[:-1]), row[0].split(',')[0].split()[-1], row[1]]
                    df.append(direccion)
        
        
        for row in df:
            try:
                insert_query = """INSERT INTO Direccion (calle, numero, comuna_cut)
                                    VALUES (%s, %s, %s)"""
                cursor.execute(insert_query, row)
                conn.commit()
            except (Exception, Error) as error:
                if 'value too long for type character' in str(error):
                    largo_columna = int(str(error).split(' ')[-1].replace('varying(', '').replace(')', ''))
                    if len(row[0]) > largo_columna:
                        try:
                            conn.rollback()
                            cursor.execute("""ALTER TABLE Direccion ALTER COLUMN calle TYPE VARCHAR(%s);""", [len(row[0])])
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