from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('consultas_predeterminadas/', views.consultas_predeterminadas, name='consultas_predeterminadas'),
    path('consultas_inestructuradas/', views.consultas_inestructuradas, name='consultas_inestructuradas'),
    # Add more app-specific URL patterns for views
]