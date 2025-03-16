from django.contrib import admin
from django.urls import path
from auth_app.views import *

urlpatterns = [
    path('pagina-inicial', home, name='pagina-inicial'),  # URL para a página inicial
    # path('cadastro/<str:codigo>/', Register, name='cadastro'),  # URL para o registro com código
    # path('login/', Login, name='entrar'),  # URL para o login com código
    # path('logout/', Logout, name='sair') # URL para o logout com código
]