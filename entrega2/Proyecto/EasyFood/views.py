from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def consultas_predeterminadas(request):
    return render(request, 'consultas_predeterminadas.html')
