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

table_name = "PlatoRestaurant"

try:
    # Conexión con la base de datos
    conn = psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME
    )
    with open('../CSV/platos.csv', 'r', encoding = 'ISO-8859-1') as file:
        data = file.read().split('\n')
        df = []
        for line in data[1:]:
            row = line.split(';')
            df.append([row[0], row[-3]])

    cursor = conn.cursor()

    exitos = 0
    fallos = 0
    for row in df:
        try:
            insert_query = """WITH plato_cte AS (
                                SELECT p.id AS id
                                FROM plato as p
                                WHERE p.id = %s
                                ),
                                restaurant_cte AS (
                                SELECT r.id AS id
                                FROM restaurant as r
                                WHERE r.nombre = %s
                                )
                                INSERT INTO PlatoRestaurant (plato_id, restaurant_id)
                                SELECT plato_cte.id, restaurant_cte.id
                                FROM plato_cte, restaurant_cte;
                            """
            cursor.execute(insert_query, row)
            conn.commit()
            exitos += 1
        except (Exception, Error) as error:
            print(error)
            fallos += 1
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