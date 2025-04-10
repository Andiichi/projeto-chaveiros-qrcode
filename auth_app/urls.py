from django.urls import path
from auth_app.views import *


app_name = 'auth_app'  # Definição do namespace para a aplicação de autenticação

urlpatterns = [
    path('register/<str:codigo>/', cadastro, name='cadastro'), # URL para o registro com código
    path('login/', user_login, name='entrar'),# Login de usuário comum
    path('logout/', logout_view, name='sair'), # URL para o logout com código
    path('alterar_senha/', alterar_senha, name='alterar_senha')
]
