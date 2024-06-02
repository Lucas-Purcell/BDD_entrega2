from django.shortcuts import render
from django.db import connection
from .consultas import consulta1, consulta2, consulta3, consulta4, consulta5, consulta6, consulta7, consulta8, consulta9, consulta10
from django import forms


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
        result1 = None
        column_names1 = []

        if consulta == 1:
            query = consulta1()
            result, column_names = ejecutar_consulta(query, {'nombre': params.get('nombre')})
        elif consulta == 2:
            query, query1 = consulta2()
            result, column_names = ejecutar_consulta(query, {'email': params.get('email')})
            result1, column_names1 = ejecutar_consulta(query1, {'email': params.get('email')})
        elif consulta == 3:
            query = consulta3()
            result, column_names = ejecutar_consulta(query)
        elif consulta == 4:
            query = consulta4()
            result, column_names = ejecutar_consulta(query, {'estilo': params.get('estilo')})
        elif consulta == 5:
            query = consulta5()
            result, column_names = ejecutar_consulta(query, {'estilo': params.get('estilo')})
        elif consulta == 6:
            query = consulta6()
            result, column_names = ejecutar_consulta(query, {'email': params.get('email')})
        elif consulta == 7:
            query = consulta7()
            result, column_names = ejecutar_consulta(query)
        elif consulta == 8:
            query = consulta8()
            result, column_names = ejecutar_consulta(query)
        elif consulta == 9:
            query = consulta9(params.get('tipo'))
            result, column_names = ejecutar_consulta(query, {'numero': params.get('numero')})
        elif consulta == 10:
            query = consulta10()
            result, column_names = ejecutar_consulta(query, {'alergeno': '%{}%'.format(params.get('alergeno'))})

        return render(request, 'consultas_predeterminadas.html', {
            'results': result,
            'column_names': column_names,
            'results1': result1,
            'column_names1': column_names1,
        })
        
    return render(request, 'consultas_predeterminadas.html')

# Consulta Inestructuradas
class QueryForm(forms.Form):
    atributos = forms.CharField(label='Atributos', max_length=255, required=True)
    tablas = forms.CharField(label='Tablas', max_length=255, required=True)
    condiciones = forms.CharField(label='Condiciones', max_length=255, required=False)

def consultas_inestructuradas(request):
    resultados = None
    query = ""
    error_message = None

    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            atributos = form.cleaned_data['atributos']
            tablas = form.cleaned_data['tablas']
            condiciones = form.cleaned_data['condiciones']

            # Verificar formato de atributos y tablas
            if not all(char.isalnum() or char in ('_', ',', ' ') for char in atributos):
                error_message = "Formato de atributos inválido."
            elif not all(char.isalnum() or char in ('_', ' ') for char in tablas):
                error_message = "Formato de tablas inválido."
            else:
                query = f"SELECT DISTINCT {atributos} FROM {tablas}"
                if condiciones:
                    query += f" WHERE {condiciones}"
                
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(query)
                        resultados = cursor.fetchall()
                except Exception as e:
                    error_message = f"Error ejecutando la consulta: {str(e)}"
    else:
        form = QueryForm()

    return render(request, 'consultas_inestructuradas.html', {
        'form': form,
        'resultados': resultados,
        'query': query,
        'error_message': error_message,
    })
