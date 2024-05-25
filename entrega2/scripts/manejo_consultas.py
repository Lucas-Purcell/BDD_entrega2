import psycopg2
from psycopg2 import sql
from psycopg2 import Error
from consultas import (consulta1, consulta4, consulta5, consulta6, consulta8, consulta9, consulta10)

#para conectarse a la base
DB_HOST = 'pavlov.ing.puc.cl'
DB_PORT = '5432'
DB_USER = 'grupo8'
DB_PASSWORD = 'bulla8'
DB_NAME = 'grupo8e2'

def consultas(numero_consulta, **kwargs):
    conn = None
    cursor = None
    
    try:
        # Conexión con la base de datos
        conn = psycopg2.connect(
            user = DB_USER,
            password = DB_PASSWORD,
            host = DB_HOST,
            port = DB_PORT,
            dbname = DB_NAME
        )
        
        # Crear un cursor para ejecutar consultas
        cursor = conn.cursor()

        if numero_consulta == 1:
            try:
                query = consulta1()
                nombre_plato = kwargs.get('nombre_plato')
                cursor.execute(query, {'nombre': nombre_plato})
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
            except (Exception, Error) as error:
                print("Error al ejecutar query:", error)

        # if numero_consulta == 2:
        #     try:
        #         query, query1 = consulta2()
        #         email = kwargs.get('email')
        #         fecha_inicio = kwargs.get('fecha_inicio')
        #         fecha_fin = kwargs.get('fecha_fin')
        #         cursor.execute(query, {'email': email})
        #         rows = cursor.fetchall()
        #         for row in rows:
        #             print(row)
        #         cursor.execute(query1, {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin})
        #         rows = cursor.fetchall()
        #         print(rows)
        #     except (Exception, Error) as error:
        #         print("Error al ejecutar query:", error)

        # if numero_consulta == 3:
        #     try:
        #         query = consulta3()
        #         cursor.execute(query)
        #         rows = cursor.fetchall()
        #         for row in rows:
        #             print(row)
        #     except (Exception, Error) as error:
        #         print("Error al ejecutar query:", error)

        if numero_consulta == 4:
            try:
                query = consulta4()
                estilo = kwargs.get('estilo')
                cursor.execute(query, {'estilo': estilo})
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
            except (Exception, Error) as error:
                print("Error al ejecutar query:", error)

        if numero_consulta == 5:
            try:
                query = consulta5()
                estilo = kwargs.get('estilo')
                cursor.execute(query, {'estilo': estilo})
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
            except (Exception, Error) as error:
                print("Error al ejecutar query:", error)

        if numero_consulta == 6:
            try:
                query = consulta6()
                email = kwargs.get('email')
                cursor.execute(query, {'email': email})
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
            except (Exception, Error) as error:
                print("Error al ejecutar query:", error)

        # if numero_consulta == 7:
        #     try:
        #         query = consulta7()
        #         cursor.execute(query)
        #         rows = cursor.fetchall()
        #         for row in rows:
        #             print(row)
        #     except (Exception, Error) as error:
        #         print("Error al ejecutar query:", error)

        if numero_consulta == 8:
            try:
                query = consulta8()
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
            except (Exception, Error) as error:
                print("Error al ejecutar query:", error)
        
        if numero_consulta == 9:
            try:
                tipo = kwargs.get('tipo')
                query = consulta9(tipo)
                numero = kwargs.get('numero')
                cursor.execute(query, {'numero': numero})
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
            except (Exception, Error) as error:
                print("Error al ejecutar query:", error)

        if numero_consulta == 10:
            try:
                query = consulta10()
                alergeno = kwargs.get('alergeno')
                cursor.execute(query, {'alergeno': '%{}%'.format(alergeno)}) #revisar si esto funciona
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
            except (Exception, Error) as error:
                print("Error al ejecutar query:", error)

    except (Exception, Error) as error:
        print("Error al conectarse al servidor:", error)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

