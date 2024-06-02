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

table_name = "ContenidoPedido"

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
                df.append([row[0], id_list])
    

    exitos = 0
    fallos = 0

    for row in df:
        for pid in row[1]:
            try:
                insert_query = """INSERT INTO ContenidoPedido (pedido_id, plato_id)
                                    VALUES (%s, %s);
                                    """
                
                cursor.execute(insert_query, (row[0], pid))  # Passing the list of IDs directly
                exitos += 1

            except (Exception, psycopg2.Error) as error:
                print(error)
                fallos += 1
                pass
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