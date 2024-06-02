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

table_name = "DespachadorEmpresa"


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
    

    exitos = 0
    fallos = 0

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
            
            cursor.execute(insert_query, row)  # Passing the list of IDs directly
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