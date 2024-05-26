from django.shortcuts import render
from django.db import connection
from .consultas import consulta1, consulta4, consulta5, consulta6, consulta8, consulta9, consulta10


def home(request):
    return render(request, 'home.html')

def ejecutar_consulta(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        results = cursor.fetchall()
    return results, columns

def consultas_predeterminadas(request):
    if request.method == 'POST':
        consulta = int(request.POST.get('query'))
        params = request.POST.dict()

        params.pop('csrfmiddlewaretoken', None)
        params.pop('query', None)

        result = None
        column_names = []

        if consulta == 1:
            query = consulta1()
            result, column_names = ejecutar_consulta(query, {'nombre': params.get('nombre')})
        elif consulta == 4:
            query = consulta4()
            result, column_names = ejecutar_consulta(query, {'estilo': params.get('estilo')})
        elif consulta == 5:
            query = consulta5()
            result, column_names = ejecutar_consulta(query, {'estilo': params.get('estilo')})
        elif consulta == 6:
            query = consulta6()
            result, column_names = ejecutar_consulta(query, {'email': params.get('email')})
        elif consulta == 8:
            query = consulta8()
            result, column_names = ejecutar_consulta(query)
        elif consulta == 9:
            query = consulta9(params.get('tipo'))
            result, column_names = ejecutar_consulta(query, {'numero': params.get('numero')})
        elif consulta == 10:
            query = consulta10()
            result, column_names = ejecutar_consulta(query, {'alergeno': params.get('alergeno')})
            print(result)

        return render(request, 'consultas_predeterminadas.html', {'results': result, 'column_names': column_names})

    return render(request, 'consultas_predeterminadas.html')
