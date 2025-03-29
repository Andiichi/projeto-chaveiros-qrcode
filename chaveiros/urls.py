from django.contrib import admin
from django.urls import path
from auth_app.views import *

from django.views.generic import TemplateView

app_name = 'chaveiros'  # Definição do namespace para a aplicação de autenticação

urlpatterns = [
    path('pagina-inicial/', TemplateView.as_view(template_name='pagina-inicial.html'), name='pagina_inicial'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard/dashboard.html'), name='dashboard'),
    path('dashboard/listagem', TemplateView.as_view(template_name='dashboard/dashboard_listagem.html'), name='dashboard_listagem')
]