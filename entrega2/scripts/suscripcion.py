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

table_name = "Suscripcion"

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
    cursor.execute("SET DateStyle = 'ISO, DMY';")
    with open('../CSV/suscripciones.csv', 'r', encoding = 'ISO-8859-1') as file:
        data = file.read().split('\n')
        
        df = []
        for line in data[1:]:
            row = line.split(';')
            if len(row) == 6:
                df.append(row)
    exitos = 0
    fallos = 0
    
    for row in df:
        try:
            insert_query = """WITH usuario_cte AS (
                                SELECT u.id AS usuario_id
                                FROM usuario as u
                                WHERE u.email = %s
                                ),
                                empresa_cte AS (
                                SELECT e.id AS empresa_id
                                FROM empresa as e
                                WHERE e.nombre = %s
                                )

                               INSERT INTO Suscripcion (usuario_id, empresa_id, estado, ultimo_pago, fecha_ultimo_pago, ciclo)
                               SELECT usuario_cte.usuario_id, empresa_cte.empresa_id, %s, %s, %s, %s
                               FROM usuario_cte, empresa_cte;
                            """
            cursor.execute(insert_query, row)            
            exitos += 1

        except (Exception, Error) as error:
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