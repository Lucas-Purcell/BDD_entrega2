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

table_name = "Pedido"

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

    with open('../CSV/pedidos2.csv', 'r', encoding = 'ISO-8859-1') as file:
        data = file.read().split('\n')
        header = data[0].split(';')
        df = []
        for line in data[1:]:
            row = line.split(';')
            if len(row) == 8:
                df.append({h: r for h, r in zip(header, row)})
    exitos= 0
    fallos= 0
    for row in df:
        try:
            insert_query = """WITH usuario_cte AS (
                                SELECT u.id AS usuario_id
                                FROM usuario as u
                                WHERE u.email = %s
                                )

                               INSERT INTO Pedido (usuario_id, id, fecha, hora, estado)
                               SELECT usuario_cte.usuario_id, %s, %s, %s, TRIM(%s)
                               FROM usuario_cte;
                            """
            
            keys_to_extract = ['cliente', 'id','fecha', 'hora', 'estado']
            extracted = [row[key] for key in keys_to_extract]
            cursor.execute("SET DateStyle = 'ISO, DMY';")
            cursor.execute(insert_query, extracted)    
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

    with open('../CSV/calificacion.csv', 'r', encoding = 'ISO-8859-1') as file:
        data = file.read().split('\n')
        cal = []
        for line in data[1:]:
            row = [f"{s}" for s in line.split(';')]
            if len(row) == 3:
                cal.append(row)
    exitos = 0
    fallos = 0
    for row in cal:
        try:
            update_query = """UPDATE Pedido SET evaluacion_cliente = %s, evaluacion_servicio = %s WHERE id = %s"""
            cursor.execute(update_query, row[::-1])
            conn.commit()
            exitos += 1
        except (Exception, Error) as error:
            print(error)
            fallos +=1 
        conn.commit()
    print('Data Updated successfully for {} rows'.format(exitos))
    print('Data Updated unssuccesfully for {} rows'.format(fallos))
except (Exception, Error) as error:
    print("Error updating data:", error)
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()