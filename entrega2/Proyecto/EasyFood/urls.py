from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('consultas_predeterminadas/', views.consultas_predeterminadas, name='consultas_predeterminadas'),
    # Add more app-specific URL patterns for views
]