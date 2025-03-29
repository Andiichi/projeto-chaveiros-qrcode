from django.contrib import admin
from django.urls import path
from auth_app.views import *

from django.views.generic import TemplateView

app_name = 'auth_app'  # Definição do namespace para a aplicação de autenticação

urlpatterns = [
    path('register/<str:codigo>/', cadastro, name='cadastro'), # URL para o registro com código
    path('login/', user_login, name='entrar'),
    path('logout/', logout_view, name='sair'), # URL para o logout com código
    path('admin-login/', admin_login, name='admin_login'),
    path('admin-logout/', admin_logout, name='admin_logout'),
    path('alterar_senha/', alterar_senha, name='alterar_senha'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard/dashboard.html'), name='dashboard')
]