from django.shortcuts import render
from django import forms
from django.db import connection

def home(request):
    return render(request, 'home.html')

def consultas_predeterminadas(request):
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
                query = f"SELECT {atributos} FROM {tablas}"
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
