import psycopg2
from psycopg2 import sql
from psycopg2 import Error
import crypt
DB_HOST = 'pavlov.ing.puc.cl'
DB_PORT = '5432'
DB_USER = 'grupo8'
DB_PASSWORD = 'bulla8'
DB_NAME = 'grupo8e2'

conn = None
cursor = None

table_name = "Direccion"

try:
    # Conexión con la base de datos
    conn = psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME
    )
    # Crear un cursor para ejecutar consultas
    cursor = conn.cursor()

    # Abrir CSV
    with open('../CSV/clientes.csv', 'r', encoding = 'ISO-8859-1') as file:
        data = file.read().split('\n')
        df = []
        for line in data[1:]:
            row = line.split(';')[-2:]
            if len(row) == 2:
                direccion = [' '.join(row[0].split(',')[0].split()[:-1]), row[0].split(',')[0].split()[-1], row[1]]
                df.append(direccion)
    
    exitos = 0
    fallos = 0
    
    for row in df:
        try:
            insert_query = """INSERT INTO Direccion (calle, numero, comuna_cut)
                                VALUES (%s, %s, %s)"""
            cursor.execute(insert_query, row)
            conn.commit()
            exitos += 1
        except (Exception, Error) as error:
            print(error)
            fallos += 1
            conn.commit()
    conn.commit()

    print("Data loaded successfully for {} rows in table {}.".format(exitos, table_name))
    print("Data loaded unsuccessfully for {} rows".format(fallos))
except (Exception, Error) as error:
    print("Error loading data:", error)
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()