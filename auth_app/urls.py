from django.contrib import admin
from django.urls import path
from auth_app.views import *

from django.views.generic import TemplateView

app_name = 'auth_app'  # Definição do namespace para a aplicação de autenticação

urlpatterns = [
    path('pagina-inicial/', TemplateView.as_view(template_name='pagina-inicial.html'), name='pagina_inicial'),
    path('register/<str:codigo>/', cadastro, name='cadastro'), # URL para o registro com código
    path('login/', user_login, name='entrar'),
    # path('admin-login/', admin_login, name='admin_entrar'),
    path('logout/', logout_view, name='sair'), # URL para o logout com código
    path('alterar_senha/', alterar_senha, name='alterar_senha'),
    path('dashboard/', dashboard, name='dashboard')
]